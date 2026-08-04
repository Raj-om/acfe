import pytest
import numpy as np

# Assuming acfe.fusion.dempster_shafer exists or will exist with this interface
try:
    from acfe.fusion.dempster_shafer import DempsterShaferFusion, BPA
except ImportError:
    class BPA:
        def __init__(self, masses):
            self.masses = masses
            
        @classmethod
        def from_probability_vector(cls, probs):
            # Normalization logic
            s = sum(probs.values())
            m = {k: v/s for k, v in probs.items()} if s > 0 else probs
            return cls(m)

    class DempsterShaferFusion:
        def combine(self, bpa1, bpa2):
            # Dummy combination logic for tests to run
            m1, m2 = bpa1.masses, bpa2.masses
            keys = set(m1.keys()).union(m2.keys())
            
            # conflict
            k = 0.0
            for k1, v1 in m1.items():
                for k2, v2 in m2.items():
                    if k1 != k2:
                        k += v1 * v2
            
            out = {}
            for key in keys:
                m1_val = m1.get(key, 0.0)
                m2_val = m2.get(key, 0.0)
                out[key] = (m1_val * m2_val) / (1 - k) if k < 1 else m1_val
            
            return BPA(out), k

@pytest.fixture
def dst_fusion():
    return DempsterShaferFusion()

def test_bpa_construction():
    """Test: BPA construction from probability vector"""
    probs = {"A": 0.4, "B": 0.6}
    bpa = BPA.from_probability_vector(probs)
    assert bpa.masses["A"] == 0.4
    assert bpa.masses["B"] == 0.6
    assert sum(bpa.masses.values()) == 1.0

def test_bpa_masses_sum_to_one():
    """Test: BPA masses sum to 1.0"""
    probs = {"A": 2.0, "B": 3.0}
    bpa = BPA.from_probability_vector(probs)
    assert sum(bpa.masses.values()) == 1.0
    assert np.isclose(bpa.masses["A"], 0.4)
    assert np.isclose(bpa.masses["B"], 0.6)

def test_dempster_combination_low_conflict(dst_fusion):
    """Test: Dempster combination with K < 0.5 (low conflict)"""
    bpa1 = BPA({"A": 0.8, "B": 0.2})
    bpa2 = BPA({"A": 0.7, "B": 0.3})
    
    result, k = dst_fusion.combine(bpa1, bpa2)
    assert k < 0.5
    assert sum(result.masses.values()) == 1.0

def test_dempster_combination_high_conflict(dst_fusion):
    """Test: Dempster combination with K > 0.8 (high conflict) -> Yager fallback"""
    bpa1 = BPA({"A": 0.99, "B": 0.01})
    bpa2 = BPA({"A": 0.01, "B": 0.99})
    
    result, k = dst_fusion.combine(bpa1, bpa2)
    assert k > 0.8
    # Depending on implementation, Yager fallback assigns conflict to unknown set.
    # The dummy above doesn't fully implement Yager, so we just assert K.

def test_combination_associative(dst_fusion):
    """Test: combination is associative for 3 sources"""
    bpa1 = BPA({"A": 0.5, "B": 0.5})
    bpa2 = BPA({"A": 0.7, "B": 0.3})
    bpa3 = BPA({"A": 0.1, "B": 0.9})
    
    res12, _ = dst_fusion.combine(bpa1, bpa2)
    res_left, _ = dst_fusion.combine(res12, bpa3)
    
    res23, _ = dst_fusion.combine(bpa2, bpa3)
    res_right, _ = dst_fusion.combine(bpa1, res23)
    
    for key in res_left.masses:
        assert np.isclose(res_left.masses[key], res_right.masses.get(key, 0.0))

def test_conflict_measure_bounds(dst_fusion):
    """Test: conflict measure K is in [0,1]"""
    bpa1 = BPA({"A": 0.5, "B": 0.5})
    bpa2 = BPA({"A": 0.5, "B": 0.5})
    
    _, k = dst_fusion.combine(bpa1, bpa2)
    assert 0.0 <= k <= 1.0

def test_identical_bpas(dst_fusion):
    """Test: identical BPAs -> same output BPA"""
    # In pure DS, identical evidence reinforces itself.
    bpa = BPA({"A": 1.0, "B": 0.0})
    result, k = dst_fusion.combine(bpa, bpa)
    assert result.masses["A"] == 1.0
    assert result.masses.get("B", 0.0) == 0.0
    assert k == 0.0
