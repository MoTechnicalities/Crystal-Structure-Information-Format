import sys
from pathlib import Path

# Add the starter-kit directory to the Python path
starter_kit_path = Path(__file__).resolve().parent.parent / "starter-kit"
sys.path.insert(0, str(starter_kit_path))

import time
import tracemalloc
from crystal_bank_runtime import CrystalBankManager

def measure_performance():
    """
    Measures processing throughput, memory usage, and latency for RWIF schema operations.
    """
    # Initialize the Crystal Bank Manager
    bank_manager = CrystalBankManager()

    # Path to a large RWIF Crystal V1 file (adjust as needed)
    rwif_file_path = "release/samples/stress_test_rwif_crystal_v1.json"

    # Load the crystal and measure time
    print("Loading crystal...")
    start_time = time.time()
    tracemalloc.start()

    try:
        crystal = bank_manager.load(rwif_file_path)
    except Exception as e:
        print(f"Error loading crystal: {e}")
        return

    load_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Load time: {load_time:.4f} seconds")
    print(f"Memory usage: {current / 10**6:.4f} MB (peak: {peak / 10**6:.4f} MB)")

    # Perform a query and measure time
    print("Querying crystal...")
    start_time = time.time()

    try:
        results = bank_manager.query(crystal, top_k=5)
    except Exception as e:
        print(f"Error querying crystal: {e}")
        return

    query_time = time.time() - start_time
    print(f"Query time: {query_time:.4f} seconds")

    # Perform resonance computation and measure time
    print("Computing resonance...")
    start_time = time.time()

    try:
        resonance_results = bank_manager.compute_resonance(crystal, crystal)
    except Exception as e:
        print(f"Error computing resonance: {e}")
        return

    resonance_time = time.time() - start_time
    print(f"Resonance computation time: {resonance_time:.4f} seconds")

    # Output summary
    print("Performance Summary:")
    print(f"Load time: {load_time:.4f} seconds")
    print(f"Query time: {query_time:.4f} seconds")
    print(f"Resonance computation time: {resonance_time:.4f} seconds")
    print(f"Memory usage: {current / 10**6:.4f} MB (peak: {peak / 10**6:.4f} MB)")

if __name__ == "__main__":
    measure_performance()