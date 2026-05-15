# CIE/CSIF v2.0 - Researcher Release Notes

## Scope

This release packages a phase-geometric contradiction mechanism with auditable traces, milestone-level reproducibility documentation, and a compact runnable showcase artifact.

## Mechanism Summary

Core representation:
1. Principal wrap: wrap_pi(theta) = ((theta + pi) mod 2pi) - pi.
2. Angular distance over edges: d(alpha, beta) = |wrap_pi(alpha - beta)|.
3. Resonance over aligned topology: R(A,B) = sum over shared edges of angular distance.
4. Transitivity residual surrogate: Delta_abc = wrap_pi(theta_ab + theta_bc - theta_ac).
5. Anti-phase contradiction encoding: theta_false = wrap_pi(theta_base + pi).

Interpretation:
1. Coherent closure yields residual near 0.
2. Contradictory closure yields residual magnitude near pi.
3. Path disagreement is exposed as auditable residual traces.

## Included Artifacts in This Public Package

1. Technical specification and milestone record:
   - crystal-information-engine/docs/CSIF_TECHNICAL_SPECIFICATION.md
   - crystal-information-engine/docs/csif_crystal_phase_milestone.md
2. Core runnable scripts:
   - crystal-information-engine/scripts/csif_crystal_phase_demo.py
   - crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py
3. Release showcase sample:
   - release/samples/csif_release_showcase.py

## Reproducibility Entry Points

From repository root:

python3 crystal-information-engine/scripts/csif_crystal_phase_demo.py
python3 crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py
python3 release/samples/csif_release_showcase.py

Expected indicators:
1. coherent residual approximately 0,
2. contradictory residual magnitude approximately pi,
3. resonance(query, coherent) < resonance(query, contradictory),
4. showcase final line RESULT: PASS.

## Evaluation Discipline

Recommended reporting separation:
1. Mechanism validity (script-level reproducibility).
2. Curated/pilot benchmark behavior.
3. External validity claims only after protocol-gated independent datasets at scale.

For protocol and gate framing, see the milestone and technical specification documents listed above.

## Current Limits (Explicit)

1. This package is intentionally minimal and script-centered.
2. Independent external-scale corpora remain an active execution target.
3. Full multilingual federation is roadmap-directed, not presented as complete in this release.

## Forward Research Direction

The long-term agenda is a federated world-language crystal lobe cluster with:
1. language-local lexical banks,
2. bridge mappings and phase-offset translation,
3. auditable cross-language contradiction analysis.

See:
- release/ROADMAP.md
- release/WORLD_LANGUAGE_CRYSTAL_LOBE_VISION.md

## Contribution and Security

- CONTRIBUTING.md
- SECURITY.md
