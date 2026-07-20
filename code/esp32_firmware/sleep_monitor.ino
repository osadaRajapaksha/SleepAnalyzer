// ESP32 Dual Strain Gauge Data Acquisition
// Reads two analog inputs (simulating left and right strain gauges or HX711 output)
// and streams them via Serial to the laptop monitor.

#define LEFT_SENSOR_PIN 34
#define RIGHT_SENSOR_PIN 35
#define SAMPLE_RATE_HZ 100

unsigned long lastSampleTime = 0;
const unsigned long sampleInterval = 1000 / SAMPLE_RATE_HZ;

void setup() {
  Serial.begin(115200);
  
  // Set ADC attenuation if needed (for 0-3.3V range on ESP32)
  analogReadResolution(12);
  
  // Optional: setup WiFi here if UDP streaming is preferred
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSampleTime >= sampleInterval) {
    lastSampleTime = currentMillis;
    
    // Read raw values from ADCs
    int leftVal = analogRead(LEFT_SENSOR_PIN);
    int rightVal = analogRead(RIGHT_SENSOR_PIN);
    
    // Print data in CSV format: timestamp,left,right
    Serial.print(currentMillis);
    Serial.print(",");
    Serial.print(leftVal);
    Serial.print(",");
    Serial.println(rightVal);
  }
}
