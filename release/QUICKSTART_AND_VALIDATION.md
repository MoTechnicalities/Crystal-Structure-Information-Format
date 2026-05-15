# Quickstart and Validation

This guide is intentionally scoped to the files currently in this public repository.

## 1. Environment Setup

From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run Reference Experiments

Run from repository root:

```bash
python3 crystal-information-engine/scripts/csif_crystal_phase_demo.py
python3 crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py
```

## 3. Expected Validation Pattern

The whale contradiction experiment should show:
1. Coherent residual near `0`.
2. Contradictory residual magnitude near `pi`.
3. `resonance(query, coherent) < resonance(query, contradictory)`.
4. A final `PASS` result.

If these conditions fail, treat the environment run as non-validated.

## 4. Reproducibility Checklist

For each run, record:
1. OS and Python version.
2. Dependency install output.
3. Full script output.
4. Whether criteria in Section 3 passed.

Template:

```text
Date:
Host OS:
Python:
Script:
Pass/Fail:
Notes:
```
