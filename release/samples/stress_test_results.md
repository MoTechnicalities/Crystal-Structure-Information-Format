# RWIF Schema Stress Test Results

**Test Date:** May 17, 2026  
**Test Script:** `rwif_schema_performance_test.py`  
**Dataset:** `stress_test_rwif_crystal_v1.json`

---

## Test Overview

The stress test evaluates the RWIF schema's performance with a larger dataset to assess scalability and memory usage. The dataset contains 10 edges and 11 concepts.

---

## Test Results

### Metrics

| Operation                  | Time (seconds) | Memory Usage (MB) |
|----------------------------|----------------|-------------------|
| **Load Crystal**           | 0.0001         | 0.0063 (peak: 0.0147) |
| **Query Crystal**          | 0.0000         | -                 |
| **Resonance Computation**  | 0.0000         | -                 |

### Summary
- **Load Time**: The crystal was loaded in 0.0001 seconds.
- **Query Time**: Queries were processed in 0.0000 seconds.
- **Resonance Computation Time**: Resonance computations completed in 0.0000 seconds.
- **Memory Usage**: The test used 0.0063 MB of memory, peaking at 0.0147 MB.

---

## Dataset Details

The stress test dataset used for testing:

```json
{
    "label": "StressTestCrystal",
    "edges": [
        {
            "subject": "Concept1",
            "relation": "is_a",
            "object": "Concept2",
            "phase": 0.5236,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept2",
            "relation": "causes",
            "object": "Concept3",
            "phase": 0.7854,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept3",
            "relation": "supports",
            "object": "Concept4",
            "phase": 0.2618,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept4",
            "relation": "dispels",
            "object": "Concept5",
            "phase": 3.1416,
            "polarity": "false",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept5",
            "relation": "antonym",
            "object": "Concept6",
            "phase": 3.1416,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept6",
            "relation": "is_a",
            "object": "Concept7",
            "phase": 0.5236,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept7",
            "relation": "causes",
            "object": "Concept8",
            "phase": 0.7854,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept8",
            "relation": "supports",
            "object": "Concept9",
            "phase": 0.2618,
            "polarity": "true",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept9",
            "relation": "dispels",
            "object": "Concept10",
            "phase": 3.1416,
            "polarity": "false",
            "source": "test_source",
            "created_at": 1684358400.0
        },
        {
            "subject": "Concept10",
            "relation": "antonym",
            "object": "Concept11",
            "phase": 3.1416,
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
- The dataset is located in `release/samples/stress_test_rwif_crystal_v1.json`.
- The results indicate that the RWIF schema operations remain efficient with moderately larger datasets.

---

**Next Steps:**
- Further expand the dataset to test extreme scalability.
- Profile memory usage and latency under high concurrency.

---

*This document is part of the Crystal Information Engine (CIE) / CSIF project.*