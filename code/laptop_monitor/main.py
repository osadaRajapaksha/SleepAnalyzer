import os
import time
import serial
import numpy as np
from dotenv import load_dotenv
from engines import SourceRecoveryEngine, OccupantAttributionEngine, IdentityPersistenceEngine, SleepStagingEngine

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")
BAUD_RATE = int(os.getenv("BAUD_RATE", 115200))
SAMPLE_RATE_HZ = int(os.getenv("SAMPLE_RATE_HZ", 100))
BUFFER_WINDOW_SEC = int(os.getenv("BUFFER_WINDOW_SEC", 10))

def main():
    buffer_size = SAMPLE_RATE_HZ * BUFFER_WINDOW_SEC
    data_buffer = []
    
    # Initialize Engines
    recovery_engine = SourceRecoveryEngine(sample_rate=SAMPLE_RATE_HZ)
    attribution_engine = OccupantAttributionEngine()
    persistence_engine = IdentityPersistenceEngine()
    sleep_staging_engine = SleepStagingEngine(sample_rate=SAMPLE_RATE_HZ)

    print(f"Connecting to ESP32 on {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Connected. Collecting data...")
    except Exception as e:
        print(f"Failed to connect to Serial: {e}")
        print("Running in simulation mode with random data for demonstration...")
        ser = None

    while True:
        try:
            if ser:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 3:
                        # timestamp, left_val, right_val
                        data_buffer.append([float(parts[1]), float(parts[2])])
            else:
                # Simulation mode: generate overlapping sine waves
                t = time.time()
                left_sim = np.sin(2 * np.pi * 1.0 * t) + 0.5 * np.sin(2 * np.pi * 1.2 * t) + np.random.normal(0, 0.1)
                right_sim = 0.5 * np.sin(2 * np.pi * 1.0 * t) + np.sin(2 * np.pi * 1.2 * t) + np.random.normal(0, 0.1)
                data_buffer.append([left_sim, right_sim])
                time.sleep(1.0 / SAMPLE_RATE_HZ)

            # Once buffer is full, process it
            if len(data_buffer) >= buffer_size:
                mixed_signals = np.array(data_buffer)
                
                # Engine 1: Recover Sources
                separated_sources = recovery_engine.process(mixed_signals)
                
                # Engine 2: Attribute Occupants
                mapping, attr_conf = attribution_engine.assign(mixed_signals, separated_sources)
                
                # Engine 3: Persist Identity
                final_mapping, persist_conf = persistence_engine.update_identity(mapping, attr_conf)
                
                # Engine 4: Sleep Staging
                left_source_id = final_mapping['Left']
                right_source_id = final_mapping['Right']
                
                left_stage = sleep_staging_engine.analyze(separated_sources[:, left_source_id])
                right_stage = sleep_staging_engine.analyze(separated_sources[:, right_source_id])
                
                print(f"--- Buffer Processed ({BUFFER_WINDOW_SEC}s) ---")
                print(f"Attribution Confidence: {attr_conf:.2f}%")
                print(f"Persistence Tracking Confidence: {persist_conf:.2f}%")
                print(f"Left Occupant assigned to Source ID: {left_source_id} (Stage: {left_stage})")
                print(f"Right Occupant assigned to Source ID: {right_source_id} (Stage: {right_stage})")
                print("-" * 40)
                
                # Clear buffer (or slide window)
                # Here we just clear it for a non-overlapping window approach
                data_buffer = []

        except KeyboardInterrupt:
            print("Stopping monitor...")
            break
        except Exception as e:
            print(f"Error processing: {e}")
            
    if ser:
        ser.close()

if __name__ == "__main__":
    main()
