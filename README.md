# Crystal Information Engine (CIE) & CSIF: Auditable Knowledge via Geometric Phase Logic

The Crystal Information Engine (CIE) and Crystal Structure Information Format (CSIF) represent a breakthrough in knowledge representation: a system where knowledge is not only stored, but made auditable, classifiable, and transparently organized using geometric phase logic. Unlike LLMs, which provide fluent but opaque answers, CIE/CSIF enables:

- **Falsifiable contradiction detection**: Contradictions are detected and explained using explicit geometric criteria, not heuristics.
- **Auditable provenance**: Every knowledge claim and contradiction is traceable to its source and logical path.
- **Extreme organizability**: Knowledge is organized into "crystals" and "banks"—modular, composable, and federated units that can be independently audited and extended.

## Mission Statement

CSIF exists to establish a universal, transparent, and substrate-independent geometry of meaning.

Modern AI systems often operate as black boxes, and biological cognition is bound by physical limits. CSIF provides an open, auditable alternative: a phase-geometric framework for representing knowledge, detecting contradictions, and building coherent reasoning systems across languages, species, and computational architectures.

Read the full mission: [MISSION.md](MISSION.md).

## What's Included

### Documentation
- **Full CIE/CSIF format specification**: [crystal-information-engine/docs/csif_crystal_phase_milestone.md](crystal-information-engine/docs/csif_crystal_phase_milestone.md)—complete mathematical definitions, phase logic, usage protocols, and experiment logs.
- **Release materials**: Multiple audience variants (general, technical, investor, media, researcher) in [release/](release/).
- **Technical specification**: [crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md](crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md).
- **LLM calibration surface contribution**: [CIE_LLM_CALIBRATION_SURFACE.md](CIE_LLM_CALIBRATION_SURFACE.md)—defines CSIF as the inspectable geometric calibration layer between frozen LLM inference and verifiable outcomes.
- **Temporal phase evolution**: [TEMPORAL_PHASE_EVOLUTION.md](TEMPORAL_PHASE_EVOLUTION.md)—extends CSIF with time-dependent phase trajectories, confidence bands, and lightweight online learning for knowledge that evolves with evidence.
- **Temporal phase validation**: [TEMPORAL_PHASE_EVOLUTION_VALIDATION.md](TEMPORAL_PHASE_EVOLUTION_VALIDATION.md)—comprehensive test results validating the temporal phase model across 7 core scenarios (phase reduction, drift, bounding, adaptive thresholds, resonance, nudging, reproducibility).

### Runnable Code & Experiments
- **Phase geometry demo**: [crystal-information-engine/scripts/csif_crystal_phase_demo.py](crystal-information-engine/scripts/csif_crystal_phase_demo.py)—minimal example showing phase geometry and resonance.
- **Whale contradiction experiment**: [crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py](crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py)—validates core claim that phase geometry separates coherent from contradictory knowledge.
- **Crystal Bank Starter Kit**: Full-featured CPU-only prototype in [release/starter-kit/](release/starter-kit/) with CLI tools for create, ingest, query, trace, and benchmark workflows.
- **Release showcase sample**: [release/samples/csif_release_showcase.py](release/samples/csif_release_showcase.py)—demonstrates multi-path contradiction tracing and cross-language bridging.

### Governance
- [CONTRIBUTING.md](CONTRIBUTING.md)—contribution guidelines emphasizing reproducibility and auditability.
- [SECURITY.md](SECURITY.md)—security vulnerability reporting policy.
- [MISSION.md](MISSION.md)-project mission and long-term commitment.

## Quick Start

### Prerequisites
- Python 3.8 or higher (no external dependencies beyond Python standard library)

### Run the Core Experiments
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 crystal-information-engine/scripts/csif_crystal_phase_demo.py
python3 crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py
```

Expected output from the whale experiment:
- Coherent transitivity residual near 0
- Contradictory transitivity residual near π
- Query resonance lower with coherent crystal than contradictory crystal
- Final result: `PASS`

### Run the Starter Kit Demo
```bash
python3 release/starter-kit/run_demo.py
```

Expected output ends with: `RESULT: PASS`

### Interactive exploration
```bash
python3 release/starter-kit/interactive_menu.py
```

For more details, see [release/QUICKSTART_AND_VALIDATION.md](release/QUICKSTART_AND_VALIDATION.md).

## How This Is Organized

1. **Understand the mechanism**: Read [crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md](crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md) for mathematical definitions.
2. **See it work**: Run the validation scripts above to confirm the phase-geometry contradiction detection works locally.
3. **Study the process**: Review [crystal-information-engine/docs/csif_crystal_phase_milestone.md](crystal-information-engine/docs/csif_crystal_phase_milestone.md) for complete experiment logs and rediscoverability protocols.
4. **Build with it**: Use the Crystal Bank Starter Kit to create, query, and audit knowledge banks on your own data.

## Why This Matters

CIE/CSIF is the first system to:
- Provide **geometric, falsifiable contradiction detection** in knowledge graphs.
- Enable **full auditability and provenance tracing** for every knowledge claim.
- Organize knowledge in a way that is both **modular and federated**, supporting trust, transparency, and composability.

## Honest Limitations

- **Concept extraction**: The format assumes clean input; real-world extraction pipelines from unstructured text are open research areas.
- **Scale validation**: Current validation is on curated datasets. External-scale validation against independently sourced corpora is in progress.
- **Deployment**: This release focuses on transparency and reproducibility. Production deployment patterns are still being developed.

See [release/ROADMAP.md](release/ROADMAP.md) for the public development roadmap.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reproducibility, claim discipline, and review criteria.

## License

Licensed under Apache 2.0. See [LICENSE](LICENSE) for details.

## Learn More

- **For technical details**: [crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md](crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md)
- **For full disclosure**: [crystal-information-engine/docs/csif_crystal_phase_milestone.md](crystal-information-engine/docs/csif_crystal_phase_milestone.md)
- **For LLM calibration architecture**: [CIE_LLM_CALIBRATION_SURFACE.md](CIE_LLM_CALIBRATION_SURFACE.md)
- **For temporal phase evolution**: [TEMPORAL_PHASE_EVOLUTION.md](TEMPORAL_PHASE_EVOLUTION.md)
- **For temporal phase validation**: [TEMPORAL_PHASE_EVOLUTION_VALIDATION.md](TEMPORAL_PHASE_EVOLUTION_VALIDATION.md)
- **For release planning**: [release/ROADMAP.md](release/ROADMAP.md)
- **For questions or collaboration**: Open an issue or contact the maintainer.

---

**CIE/CSIF: Auditable, geometric, and radically organizable knowledge.**
