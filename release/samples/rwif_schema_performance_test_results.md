# RWIF Schema Performance Test Results

**Test Date:** May 17, 2026  
**Test Script:** `rwif_schema_performance_test.py`  
**Sample File:** `sample_rwif_crystal_v1.json`

---

## Test Overview

The RWIF schema performance test evaluates the following metrics:
- **Processing throughput**: Time taken to load, query, and compute resonance for a crystal.
- **Memory usage**: Peak and current memory usage during operations.

The test was conducted using a sample RWIF Crystal V1 file containing two edges and three concepts.

---

## Test Results

### Metrics

| Operation                  | Time (seconds) | Memory Usage (MB) |
|----------------------------|----------------|-------------------|
| **Load Crystal**           | 0.0001         | 0.0017 (peak: 0.0085) |
| **Query Crystal**          | 0.0000         | -                 |
| **Resonance Computation**  | 0.0000         | -                 |

### Summary
- **Load Time**: The crystal was loaded in 0.0001 seconds.
- **Query Time**: Queries were processed in 0.0000 seconds.
- **Resonance Computation Time**: Resonance computations completed in 0.0000 seconds.
- **Memory Usage**: The test used 0.0017 MB of memory, peaking at 0.0085 MB.

---

## Sample File Details

The sample RWIF Crystal V1 file used for testing:

```json
{
    "label": "SampleCrystal",
    "edges": [
        {
            "subject": "ConceptA",
            "relation": "is_a",
            "object": "ConceptB",
            "phase": 0.5236,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "ConceptB",
            "relation": "causes",
            "object": "ConceptC",
            "phase": 0.7854,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        }
    ]
}
```

---

## Notes
- The test script is located in `release/samples/rwif_schema_performance_test.py`.
- The sample file is located in `release/samples/sample_rwif_crystal_v1.json`.
- The test results indicate that the RWIF schema operations are highly efficient for small datasets.

---

**Next Steps:**
- Test with larger datasets to evaluate scalability.
- Optimize memory usage for larger crystal banks.

---

*This document is part of the Crystal Information Engine (CIE) / CSIF project.*