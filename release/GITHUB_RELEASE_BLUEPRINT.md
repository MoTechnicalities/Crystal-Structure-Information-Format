# CIE/CSIF GitHub Release Blueprint

This blueprint packages the current public CSIF release into a practical, trustworthy open-source offering while preserving the original scientific documents as immutable references.

## 1. Release Positioning

CSIF is positioned as an auditable contradiction-detection and knowledge-organization framework based on phase geometry.

Primary promise:
- Measurable contradiction signaling with explicit geometric traces.
- Transparent methodology and reproducibility over opaque model behavior.

Non-promises:
- Not a general-purpose LLM replacement.
- Not yet validated at full external scale across independently sourced corpora.

## 2. What This Public Package Currently Contains

- Core narrative and technical specification documents.
- Two runnable reference scripts:
  - `crystal-information-engine/scripts/csif_crystal_phase_demo.py`
  - `crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py`
- Python dependency lock via `requirements.txt`.

## 3. Claim Discipline for Public Readme/Release Notes

Use this wording pattern for external communication:

1. Mechanism-level claims: "implemented and reproducible in this repo".
2. Benchmark claims: "validated on curated or pilot datasets".
3. External validity claims: "in progress until independently sourced scale targets are met".

Do not collapse these categories in one sentence.

## 4. Suggested GitHub Release Structure

Release title:
- `CIE/CSIF v2.0 - Auditable Phase-Geometry Contradiction Engine`

Release body sections:
1. What is new
2. Reproducible commands
3. Honest limitations
4. Roadmap milestones
5. How to contribute

## 5. Minimum Trust Signals

Before broad announcement:
1. Ensure license file is present and explicit.
2. Keep reproducibility commands tested on a clean environment.
3. Keep a changelog or versioned release notes.
4. Keep issue templates and security disclosure policy available.

## 6. One-Sentence Strategic Identity

"CIE/CSIF turns contradiction into measurable geometry and makes knowledge organization auditable by design."
