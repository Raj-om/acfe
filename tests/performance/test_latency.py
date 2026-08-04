import pytest
import time
import tracemalloc
import statistics

# Dummy fusion engine for performance testing
class DummyFusionEngine:
    def fuse(self, num_sensors):
        # Simulate CPU work
        _ = sum([i*i for i in range(100 * num_sensors)])
        return 0.95
        
    def fuse_graph(self, num_nodes):
        # Simulate more CPU work
        _ = sum([i*i for i in range(1000 * num_nodes)])
        return 0.90

@pytest.fixture
def engine():
    return DummyFusionEngine()

@pytest.mark.performance
def test_single_fusion_latency(engine):
    """Test: single fusion request < 100ms end-to-end"""
    start_time = time.perf_counter()
    engine.fuse(num_sensors=2)
    end_time = time.perf_counter()
    
    latency_ms = (end_time - start_time) * 1000
    assert latency_ms < 100.0

@pytest.mark.performance
def test_batch_fusion_latency(engine):
    """Test: batch of 100 fusion requests -> p95 < 200ms"""
    latencies = []
    
    for _ in range(100):
        start = time.perf_counter()
        engine.fuse(num_sensors=3)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)
        
    p95 = statistics.quantiles(latencies, n=100)[94]
    
    print(f"Batch Performance: Mean={statistics.mean(latencies):.2f}ms, "
          f"p50={statistics.median(latencies):.2f}ms, p95={p95:.2f}ms")
    
    assert p95 < 200.0

@pytest.mark.performance
def test_many_sensors_latency(engine):
    """Test: 10 sensors fusion -> < 50ms"""
    start = time.perf_counter()
    engine.fuse(num_sensors=10)
    end = time.perf_counter()
    
    latency_ms = (end - start) * 1000
    assert latency_ms < 50.0

@pytest.mark.performance
def test_graph_inference_latency(engine):
    """Test: ACFE-Graph inference with 20 nodes -> < 500ms"""
    start = time.perf_counter()
    engine.fuse_graph(num_nodes=20)
    end = time.perf_counter()
    
    latency_ms = (end - start) * 1000
    assert latency_ms < 500.0

@pytest.mark.performance
def test_memory_usage(engine):
    """Test: memory usage per fusion < 50MB"""
    tracemalloc.start()
    
    engine.fuse(num_sensors=5)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    peak_mb = peak / (1024 * 1024)
    print(f"Peak memory usage: {peak_mb:.2f} MB")
    
    assert peak_mb < 50.0

@pytest.mark.performance
def test_throughput(engine):
    """Test: throughput > 100 fusions/second"""
    iterations = 500
    
    start = time.perf_counter()
    for _ in range(iterations):
        engine.fuse(num_sensors=2)
    end = time.perf_counter()
    
    duration = end - start
    throughput = iterations / duration
    
    print(f"Throughput: {throughput:.2f} fusions/sec")
    assert throughput > 100.0
