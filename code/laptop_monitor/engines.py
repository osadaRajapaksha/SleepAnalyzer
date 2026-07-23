import numpy as np
from sklearn.decomposition import FastICA
from scipy.signal import butter, filtfilt

class SourceRecoveryEngine:
    def __init__(self, sample_rate=100):
        self.sample_rate = sample_rate
        self.ica = FastICA(n_components=2, random_state=42, max_iter=1000)

    def _bandpass_filter(self, data, lowcut, highcut, order=3):
        nyq = 0.5 * self.sample_rate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, data)

    def process(self, mixed_signals):
        """
        Takes mixed_signals of shape (n_samples, 2)
        Returns separated sources of shape (n_samples, 2)
        """
        # Step 1: Pre-filtering (e.g., isolating heart rate frequencies: 0.8 Hz to 3.0 Hz)
        filtered_mixed = np.zeros_like(mixed_signals)
        for i in range(mixed_signals.shape[1]):
            filtered_mixed[:, i] = self._bandpass_filter(mixed_signals[:, i], 0.8, 3.0)

        # Step 2: Blind Source Separation (FastICA)
        # Handle cases where ICA might fail on flat data
        if np.std(filtered_mixed[:, 0]) < 1e-5 and np.std(filtered_mixed[:, 1]) < 1e-5:
            return filtered_mixed 
            
        separated_sources = self.ica.fit_transform(filtered_mixed)
        return separated_sources


class OccupantAttributionEngine:
    def __init__(self):
        pass

    def assign(self, original_mixed, separated_sources):
        """
        Assigns each separated source to Left (Occupant A) or Right (Occupant B).
        Returns a dictionary mapping 'Left' and 'Right' to the separated array indices
        and a confidence score.
        """
        # Calculate the correlation or energy contribution of each source to the original sensors
        # This is a simplified spatial fingerprinting approach.
        
        energy_L = np.var(original_mixed[:, 0])
        energy_R = np.var(original_mixed[:, 1])
        
        # Determine mapping based on checking correlation of source to original sensor.
        corr_matrix = np.corrcoef(separated_sources.T, original_mixed.T)
        
        # corr_matrix[0:2, 2:4] contains correlations between sources and original sensors
        source0_to_L = abs(corr_matrix[0, 2])
        source0_to_R = abs(corr_matrix[0, 3])
        source1_to_L = abs(corr_matrix[1, 2])
        source1_to_R = abs(corr_matrix[1, 3])
        
        if source0_to_L > source0_to_R:
            mapping = {'Left': 0, 'Right': 1}
            confidence = (source0_to_L - source0_to_R) / (source0_to_L + 1e-9)
        else:
            mapping = {'Left': 1, 'Right': 0}
            confidence = (source0_to_R - source0_to_L) / (source0_to_R + 1e-9)
            
        # Bound confidence
        confidence = min(max(confidence * 100, 0), 100)
        
        return mapping, confidence


class IdentityPersistenceEngine:
    def __init__(self):
        self.last_mapping = None
        self.tracking_confidence = 100.0

    def update_identity(self, new_mapping, attribution_confidence):
        """
        Maintains identity across frames, preventing swapping if attribution confidence is low.
        """
        if self.last_mapping is None:
            self.last_mapping = new_mapping
            return new_mapping, attribution_confidence
            
        # If the new attribution wants to swap identities, we require high confidence
        if new_mapping['Left'] != self.last_mapping['Left']:
            if attribution_confidence > 80.0:
                # Confident swap (e.g. they actually rolled over into each other's spaces)
                self.last_mapping = new_mapping
                self.tracking_confidence = attribution_confidence
            else:
                # Reject swap, maintain previous identity
                new_mapping = self.last_mapping
                self.tracking_confidence = max(0, self.tracking_confidence - 5.0)
        else:
            # Consistent identity
            self.tracking_confidence = min(100.0, self.tracking_confidence + 5.0)
            
        return new_mapping, self.tracking_confidence


class SleepStagingEngine:
    def __init__(self, sample_rate=100):
        self.sample_rate = sample_rate

    def analyze(self, source_signal):
        """
        Heuristic sleep staging based on signal variance and frequency stability.
        Returns one of: "Wake", "Light Sleep", "Deep Sleep", "REM"
        """
        # Calculate variance to estimate motion
        variance = np.var(source_signal)
        
        # Calculate zero-crossing rate to estimate frequency stability
        # A simple proxy for heart/respiration rate variability
        zero_crossings = np.where(np.diff(np.sign(source_signal)))[0]
        if len(zero_crossings) > 1:
            intervals = np.diff(zero_crossings)
            interval_variance = np.var(intervals)
        else:
            interval_variance = 0
            
        # Heuristics
        # Note: These thresholds are completely arbitrary for demonstration purposes.
        if variance > 1.5:  # High movement (assuming FastICA normalizes to var ~1, anything >1.5 is extra)
            return "Wake"
        elif interval_variance < 10:  # Very stable intervals (low HRV)
            return "Deep Sleep"
        elif interval_variance > 30: # Highly variable intervals (high HRV)
            return "REM"
        else:
            return "Light Sleep"
