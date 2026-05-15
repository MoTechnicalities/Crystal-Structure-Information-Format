# CIE/CSIF v2.0 - Auditable Phase-Geometry Contradiction Engine

## What this release includes

This public release provides a transparent, auditable contradiction-detection framework based on phase geometry.

Included now:
- Technical and milestone documentation.
- Replication scripts for core mechanism behavior.
- A minimal release showcase sample with explicit pass/fail checks.

## Try it in 10 seconds

Run from repository root:

python3 release/samples/csif_release_showcase.py

Expected ending line:

RESULT: PASS

## What the sample demonstrates

1. Coherent vs contradictory crystal separation.
2. Path-level auditable contradiction traces.
3. Tiny cross-language bridge alignment (English to Spanish).

## Scale snapshot

To show that the runtime scales without shipping large data blobs, the starter kit now includes an on-demand synthetic benchmark with three tiers:

- Small: 500 crystals, 1,500 edges, about 5,004 QPS.
- Medium: 2,000 crystals, 6,000 edges, about 1,256 QPS.
- Large: 5,000 crystals, 15,000 edges, about 459 QPS.

The benchmark report is generated locally at:

release/starter-kit/reports/scale_benchmark_report.json

## Reproducible core scripts

python3 crystal-information-engine/scripts/csif_crystal_phase_demo.py
python3 crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py

## Honest limitations

1. This release emphasizes mechanism transparency and reproducibility.
2. External-validity scale claims require larger independently sourced evaluation sets.
3. Full multilingual world-scale federation remains an active roadmap direction.

## Roadmap direction

The long-term target is a federated crystal lobe cluster across world languages: auditable language banks with bridge mappings, phase offsets, and traceable contradiction analysis across languages.

See:
- release/ROADMAP.md
- release/WORLD_LANGUAGE_CRYSTAL_LOBE_VISION.md

## Contributing

Please review:
- CONTRIBUTING.md
- SECURITY.md
