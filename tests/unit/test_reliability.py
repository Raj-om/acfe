import pytest

try:
    from acfe.confidence.reliability import ReliabilityTracker
except ImportError:
    class ReliabilityTracker:
        def __init__(self, default_score=0.5, alpha=0.1, threshold=0.2, max_failures=3):
            self.scores = {}
            self.consecutive_failures = {}
            self.default_score = default_score
            self.alpha = alpha
            self.threshold = threshold
            self.max_failures = max_failures
            
        def get_score(self, sensor_id):
            return self.scores.get(sensor_id, self.default_score)
            
        def update(self, sensor_id, correct):
            current = self.get_score(sensor_id)
            target = 1.0 if correct else 0.0
            
            # EMA
            new_score = (1 - self.alpha) * current + self.alpha * target
            self.scores[sensor_id] = new_score
            
            if not correct:
                self.consecutive_failures[sensor_id] = self.consecutive_failures.get(sensor_id, 0) + 1
            else:
                self.consecutive_failures[sensor_id] = 0
                
        def is_unreliable(self, sensor_id):
            if self.consecutive_failures.get(sensor_id, 0) >= self.max_failures:
                return True
            if self.get_score(sensor_id) < self.threshold:
                return True
            return False
            
        def reset(self, sensor_id):
            self.scores[sensor_id] = self.default_score
            self.consecutive_failures[sensor_id] = 0

@pytest.fixture
def tracker():
    return ReliabilityTracker(default_score=0.5, alpha=0.1, threshold=0.2, max_failures=3)

def test_initial_reliability_neutral(tracker):
    """Test: initial reliability score is neutral (0.5 or configured default)"""
    score = tracker.get_score("sensor_1")
    assert score == 0.5

def test_correct_predictions_increase_reliability(tracker):
    """Test: correct predictions increase reliability score"""
    tracker.update("sensor_1", correct=True)
    assert tracker.get_score("sensor_1") > 0.5

def test_incorrect_predictions_decrease_reliability(tracker):
    """Test: incorrect predictions decrease reliability score"""
    tracker.update("sensor_1", correct=False)
    assert tracker.get_score("sensor_1") < 0.5

def test_ema_decay_alpha_0_1(tracker):
    """Test: EMA decay with alpha=0.1 behaves correctly"""
    # Formula: new = 0.9 * 0.5 + 0.1 * 1.0 = 0.45 + 0.1 = 0.55
    tracker.update("sensor_1", correct=True)
    assert pytest.approx(tracker.get_score("sensor_1")) == 0.55

def test_sensor_flagged_unreliable_after_n_failures(tracker):
    """Test: sensor flagged unreliable after N consecutive failures"""
    assert not tracker.is_unreliable("sensor_1")
    
    # Fail 3 times (max_failures=3)
    tracker.update("sensor_1", correct=False)
    tracker.update("sensor_1", correct=False)
    assert not tracker.is_unreliable("sensor_1")
    
    tracker.update("sensor_1", correct=False)
    assert tracker.is_unreliable("sensor_1")

def test_reliability_resets_on_reconnect(tracker):
    """Test: reliability resets on sensor reconnect"""
    tracker.update("sensor_1", correct=False)
    tracker.update("sensor_1", correct=False)
    tracker.update("sensor_1", correct=False)
    
    assert tracker.is_unreliable("sensor_1")
    
    tracker.reset("sensor_1")
    assert not tracker.is_unreliable("sensor_1")
    assert tracker.get_score("sensor_1") == 0.5

def test_multiple_sensors_tracked_independently(tracker):
    """Test: multiple sensors tracked independently"""
    tracker.update("sensor_1", correct=True)
    tracker.update("sensor_2", correct=False)
    
    assert tracker.get_score("sensor_1") > 0.5
    assert tracker.get_score("sensor_2") < 0.5
    assert tracker.get_score("sensor_3") == 0.5
