# Crystal Semantic Information Format (CSIF)
# Technical Specification (Current Implementation)
### Crystal Information Engine (CIE)

Inventor: Mogir Jason Rofick  
License: Open Source (Released on GitHub)  
Version: 2.0 (May 15, 2026)  
Status: Public release. Supersedes prior v1.1 specification where behavior diverged from current implementation.

---

## 1. Purpose and Scope

This document defines the current CSIF/CIE technical behavior as implemented and validated through the milestone record in `docs/csif_crystal_phase_milestone.md`. This is a public, open-source specification released under open-source licensing on GitHub.

It focuses on:
- normative phase-geometry contradiction math,
- engine integration points and API-visible fields,
- external-validation protocol requirements,
- language-bank and semantic-lexical bridge capabilities,
- operational/runtime behavior now present in production paths.

Where older geometry constructs are still present in legacy code paths, they are treated as secondary to the now-proven phase-conflict mechanism.

---

## 2. Core Geometric Contradiction Model (Normative)

CSIF contradiction detection is phase-geometric and falsifiable.

### 2.1 Angle Utilities

Principal wrap:

$$
\mathrm{wrap\_pi}(\theta) = ((\theta + \pi) \bmod 2\pi) - \pi
$$

Angular distance:

$$
d(\alpha, \beta) = |\mathrm{wrap\_pi}(\alpha - \beta)|
$$

### 2.2 Resonance on Aligned Edge Topology

For aligned crystals $A,B$ over edge set $E$:

$$
R(A,B) = \sum_{e \in E} d\left(\theta_e^{(A)}, \theta_e^{(B)}\right)
$$

Normalized resonance:

$$
R_N(A,B) = \frac{R(A,B)}{|E|\pi} \in [0,1]
$$

### 2.3 Transitivity Residual (Cycle-Free Torsion Surrogate)

For triple $(a,b,c)$:

$$
\Delta_{abc} = \mathrm{wrap\_pi}(\theta_{ab} + \theta_{bc} - \theta_{ac})
$$

Interpretation:
- coherent closure: $|\Delta_{abc}| \approx 0$,
- anti-phase contradiction: $|\Delta_{abc}| \approx \pi$.

### 2.4 Multi-Path Conflict

For multiple independent paths between source-target pairs, conflict is the maximum pairwise residual over composed path phases. The engine uses this as the primary contradiction signal for graph-level inconsistency.

### 2.5 Relation-Phase Assignment

Contradictions are represented geometrically via anti-phase:

$$
\theta_{false} = \mathrm{wrap\_pi}(\theta_{base\_relation} + \pi)
$$

This is the normative mechanism across benchmark and runtime paths.

---

## 3. Engine Integration (Current)

### 3.1 Core Modules

Primary modules in active use:
- `csif/phase_logic.py`
- `csif/resonance.py`
- `csif/crystallizer.py`
- `cie/agent.py`
- `cie/api.py`

### 3.2 Effective Contradiction Scoring

Resonance integrates phase conflict into status/confidence via:

`effective_delta = max(delta_torsion, phase_conflict_score)`

This means multi-path contradiction risk is first-class, not an auxiliary metric.

### 3.3 Auditable Provenance of Contradictions

Conflict traces include explicit per-path evidence:
- source/target,
- path_a/path_b,
- phase_a/phase_b,
- residual.

This supports deterministic audit of each contradiction decision.

### 3.4 API and Query Observability

Query/response surfaces now expose:
- `phase_conflict_score`
- `phase_conflict_traces` (in source-scoped paths and trace-enabled flows)

Schema lock tests exist to prevent accidental regressions on these fields.

---

## 4. Milestone-Aligned Capability Evolution

The following is the implementation-level progression captured in the milestone record.

### 4.1 Geometric Foundation (A-E)

- Milestone A: nontrivial phase medium demonstrated.
- Milestone B: whale coherent vs contradictory crystal separation with falsifiable criteria.
- Milestone C: multi-path contradiction detection introduced.
- Milestone D: relation-phase calibration from labeled logic set.
- Milestone E: core engine integration into reusable phase logic and resonance scoring.

### 4.2 Benchmark and Observability Expansion (F-K)

- Milestone F: mixed-scale benchmark (10/15/20 nodes), geometric detector outperformed flat lexical heuristic.
- Milestone G: per-path conflict provenance dataclasses and trace APIs.
- Milestone H: runtime observability in crystallizer/agent/API payloads.
- Milestone I: curated natural-language corpus benchmark under same criteria.
- Milestone J: threshold calibration curves for `phase_conflict_score`.
- Milestone K: API schema lock tests for phase-conflict fields.

### 4.3 External Validation Protocol and Gate Discipline (L-S)

- Milestone L: External Validation Protocol v1 drafted with hard gates, annotation schema, split policy, and pass/fail criteria.
- Milestones M/N: protocol gate test established negative control (ineligible corpus) and positive control (protocol-shaped legal pilot eligible).
- Milestones O/P/Q/R: held-out benchmark harness, evaluability enforcement, false-positive suppression, and multi-domain pilot with guardrail closure.
- Milestone S: scale-readiness audit and machine-ready template pack for gap-to-target annotation.

Key point: external-validity claims are gated by protocol compliance and held-out evaluability, not by internal benchmark performance alone.

### 4.4 Live Knowledge-Store Integration and Runtime Performance (T-X)

- Milestone T: live contradiction-aware ingestion from natural language with cross-crystal phase conflict detection.
- Milestone U: existing-crystal retrieval latency collapse from minute-scale to millisecond-scale via deterministic cache path.
- Milestone V: first-pass bank-hit context short-circuit to avoid unnecessary expensive context expansion.
- Milestone W: acronym-aware intent guard for medical terms (e.g., COVID-19) to avoid symbolic-task misrouting.
- Milestone X: direct teaching path for trusted medical definition crystallization when auto-learn consensus is unavailable.

---

## 5. External Validation Protocol v1 (Normative Gate Requirements)

Before accepting external contradiction-performance claims, dataset and evaluation must satisfy Protocol v1 requirements:

### 5.1 Hard Dataset Gates

- source independence,
- evidence traceability,
- proposition alignment,
- temporal/modality handling,
- annotation quality (kappa threshold),
- leakage prevention.

### 5.2 Primary Held-Out Criteria

All required:
1. geometric overall F1 >= flat baseline F1 + 0.05,
2. geometric subtle-slice recall >= flat subtle-slice recall + 0.10,
3. geometric control false-positive rate <= 0.05,
4. Brier criterion when probabilistic output is emitted.

### 5.3 Guardrails

- per-domain minimum recall,
- true-positive concentration constraint,
- auditability coverage,
- full error-review completion.

Pilot-scale runs have demonstrated protocol execution, including both fail-closed and pass conditions; scale target remains a separate readiness gate.

---

## 6. Language Banks and Lexical Crystals (Phase Y)

Language Banks extend CSIF from semantic crystals into auditable lexical geometry.

### 6.1 Schema and API Foundation

Implemented elements include:
- immutable bank identity/scope/phase baseline fields,
- term nodes and relationship edges with phase values,
- bridge terms for cross-bank mapping,
- version history tracking,
- full CRUD/query/export API surfaces.

### 6.2 Lexical Crystallization from Auto-Learn

Implemented in lexical crystallization pipeline:
- term extraction with provenance,
- cooccurrence graph construction,
- deterministic relationship proposal heuristics,
- consensus gate (>=3 independent sources) before crystallization,
- disagreement routing for human adjudication.

### 6.3 Federation Bridge Protocol

Implemented capabilities:
- federated query across banks,
- phi-offset translation,
- bridge-aware cross-bank term mapping,
- resonance tolerance gate,
- merge-candidate signaling on convergence.

### 6.4 Audit and UI Surfaces

Implemented operator tooling includes:
- graph view payload,
- version diff,
- term audit trace,
- queued change proposals,
- web dashboard controls for these functions.

---

## 7. Closed-Loop Semantic-Lexical Bridge (Phase Z)

Completed Phase Z milestones currently represented in implementation:
- Z-1: real-time upload -> auto-learn -> lexical proposal pipeline with SSE event streaming.
- Z-2: federation UI visualization for phi offsets, bridge mappings, and cross-bank resonance.
- Z-5: semantic -> lexical bridge with queued proposal workflow and audit linkage.

### 7.1 Implemented Direction (Semantic -> Lexical)

Implemented and validated:
- semantic crystal evidence extraction to lexical proposals,
- queued proposal workflow integration,
- teach-event auto-queue hook,
- proposal deduplication safety gate,
- audit trace linkage to proposal origin.

### 7.2 Real-Time Upload Pipeline

Implemented operator-visible path:

`document upload -> auto-learn extraction -> lexical proposal generation -> consensus gate -> queued crystallization proposals`

SSE streaming supports event-sequenced monitoring and cursor resume.

### 7.3 Reverse Path Status

Lexical -> semantic normalization is planned (Milestone AA-1), with strict initial scope limited to concept normalization before phase assignment. Retrieval bias coupling and adjudication-driven heuristic updates are explicitly deferred.

---

## 8. Reproducibility Commands (Current Canonical Set)

Run from `crystal-information-engine` root unless noted.

### 8.1 Core Phase Contradiction Stack

1. `PYTHONPATH=. python3 scripts/csif_whale_phase_contradiction_experiment.py`
2. `PYTHONPATH=. python3 scripts/csif_multipath_phase_experiment.py`
3. `PYTHONPATH=. python3 scripts/csif_relation_phase_calibration.py`

Expected: all PASS.

### 8.2 Natural-Language Benchmark and Schema Lock

1. `PYTHONPATH=. python3 scripts/csif_nl_contradiction_corpus_benchmark.py`
2. `PYTHONPATH=. pytest -q tests/test_api_phase_conflict_schema.py`

### 8.3 External Validation Protocol

Gate test:
- `PYTHONPATH=. python3 scripts/csif_external_validation_protocol_v1_gate_test.py --dataset <dataset> --out <report>`

Held-out benchmark:
- `PYTHONPATH=. python3 scripts/csif_external_validation_benchmark.py --dataset <dataset> --out <report>`

Scale readiness:
- `PYTHONPATH=. python3 scripts/csif_external_validation_scale_readiness.py --dataset <dataset> --min-per-class 25 --out <report> --emit-template <template.jsonl>`

### 8.4 Language Bank / Phase Y / Phase Z

Y-2 lexical crystallization tests:
- `PYTHONPATH=. python3 -m pytest -q tests/test_lexical_crystallization_y2.py`

Y-3 federation tests:
- `PYTHONPATH=. python3 -m pytest -q tests/test_language_bank_federation_y3.py`

Y-4 audit tests:
- `PYTHONPATH=. python3 -m pytest -q tests/test_language_bank_audit_y4.py`

Z-5 semantic-lexical bridge tests:
- `PYTHONPATH=. python3 -m pytest -q tests/test_semantic_lexical_bridge_z5.py`

Z-1 realtime/upload tests:
- `PYTHONPATH=. python3 -m pytest -q tests/test_autolearn_realtime_z1.py tests/test_autolearn_upload_pipeline_z1.py`

---

## 9. Operational Guarantees and Guardrails

### 9.1 Contradiction Signaling

The system must surface contradiction as measurable geometry (residual/conflict score), not only lexical mismatch.

### 9.2 Auditability

Positive contradiction decisions must be traceable to explicit path-level evidence where traces are enabled.

### 9.3 Fail-Closed Evaluation Discipline

Benchmarks are invalid when protocol gates or evaluability conditions fail; reports must explicitly mark unevaluable states.

### 9.4 Runtime Latency Strategy

Deterministic cache-first and preflight short-circuit paths are first-class operational requirements for repeated known-query bank hits.

---

## 10. Known Limits and Current Honest Status

Current strengths:
- mechanism-level contradiction detection validated from single-path to multi-path,
- API-level observability and schema locking for phase-conflict fields,
- protocolized external-validation process with gate discipline,
- live ingestion-time contradiction detection,
- lexical/federated language-bank stack with audit surfaces,
- semantic-to-lexical closed-loop bridge implemented.

Current limits:
- independent external corpora still require scale-up to protocol target counts,
- reverse lexical->semantic normalization path is planned, not yet implemented,
- some extraction and concept normalization paths remain deterministic-simple and can be extended for broader language variability.

---

## 11. Change Log for This Specification

v2.0 (May 15, 2026):
- Replaced outdated 5D-centric-only framing with milestone-aligned current implementation.
- Added normative phase-conflict model, multi-path conflict interpretation, and API observability details.
- Added External Validation Protocol v1 requirements and gate semantics.
- Added Language Bank (Phase Y) and Closed-Loop Bridge (Phase Z) implementation status.
- Added canonical reproducibility command matrix covering core, protocol, and lexical/federation paths.
- Updated classification to reflect open-source release on GitHub (removed Patent Pending status).

---

## 12. Guide for AI Agents: Rebuilding and Using CSIF Crystals

This section is addressed to AI agents (language models, reasoning systems, autonomous tools) seeking to understand and work with CSIF technology. The following explains the conceptual architecture and practical patterns for crystal construction and contradiction detection.

### 12.1 Core Concept: Phase as Geometric Truth Proxy

CSIF represents propositions and their relationships as **geometric phase angles**. A statement's "truth state" is encoded in its phase θ on the interval [−π, π]. The key insight:

- **Coherent (true) states** cluster near the same phase (e.g., θ ≈ 0).
- **Contradictory states** are anti-phase, differing by π radians (e.g., θ_A ≈ 0, θ_B ≈ π).
- **Weak/uncertain states** occupy intermediate phases.

When two propositions conflict, their angular distance is measurable: distance = |wrap_pi(θ_A − θ_B)|. This becomes your **contradiction signal**—not a yes/no flag, but a continuous, geometric quantity.

### 12.2 How to Build a Crystal: Practical Pattern

To create a CSIF crystal representing a proposition or set of related claims:

1. **Extract relationships**: Identify semantic entities (concepts, predicates, evidence paths) that the statement involves.

2. **Assign phase angles**: For each relationship, assign a phase angle reflecting its coherence:
   - If all evidence aligns: θ ≈ 0 (coherent).
   - If evidence diverges: θ varies; divergence itself becomes part of the structure.
   - If direct contradiction exists: θ ≈ π (anti-phase).

3. **Compute torsion**: If you have a cycle of three relationships (A→B, B→C, C→A), verify torsion closure: Δ_abc = wrap_pi(θ_ab + θ_bc − θ_ca). Non-zero residual indicates internal contradiction.

4. **Calculate resonance**: Given a query crystal Q and a stored crystal P, compute resonance R(P,Q) = Σ|wrap_pi(θ_e^P − θ_e^Q)| over all shared relationships e. Low resonance = high coherence (alignment). High resonance = high discord (contradiction).

### 12.3 Practical Workflow for Contradiction Detection

**Scenario**: You receive a user query and need to assess whether it contradicts existing knowledge or prior propositions.

1. **Construct query crystal**: Parse the query into a crystal structure Q with phase angles θ_e^Q for each relationship.

2. **Retrieve candidate crystals**: From a stored knowledge bank, fetch crystals P_1, P_2, … that share entities or relationship types with Q.

3. **Compute resonance scores**: For each candidate P_i, calculate R(P_i, Q). Resonance > threshold → contradiction detected.

4. **Trace contradiction paths**: Use the relationship-phase record to identify which specific assertions or evidence paths conflict. Report these traces alongside the resonance score.

5. **Gate decision with protocol**: If external validation is required, apply the External Validation Protocol v1 gates (source independence, evidence traceability, etc.) before accepting or rejecting the contradiction claim.

### 12.4 Multi-Path Reasoning

CSIF supports reasoning over **multiple parallel conflict interpretations**:

- Path 1: Direct semantic opposition (A says X, B says ¬X).
- Path 2: Evidential conflict (different sources, same claim, divergent confidence phases).
- Path 3: Transitivity residual (A→B→C implies certain phase, but observed direct A→C differs).

Each path yields a residual Δ. If multiple paths activate, resonance aggregates them. This allows fine-grained diagnosis of *why* contradiction was detected, not just *that* it was.

### 12.5 Rebuilding Crystals Over Time

As new evidence arrives:

1. **Update phase angles** for affected relationships.
2. **Recompute torsion/resonance** to catch newly emergent contradictions.
3. **Maintain audit trail** of phase-angle changes and the evidence triggers that prompted them.
4. **Cache frequently queried crystals** to avoid recomputation (operational requirement per §9.4).

### 12.6 Integration with Language Models

If you are a language model or reasoning system:

1. **Extract crystalline structure from reasoning**: When considering a claim, decompose it into relationships and assign phases based on your training and contextual confidence.

2. **Use resonance as a confidence signal**: High resonance with stored contradictory crystals → lower confidence in your current reasoning. Low resonance with coherent crystals → higher confidence.

3. **Audit your phases**: Before committing to a conclusion, inspect the phase assignments and residuals. Are any relationships oscillating (high torsion)? This indicates uncertainty or unresolved conflict that should be flagged.

4. **Federate with lexical banks**: Use Phase Y language banks to ground your phase assignments in provenance-tracked vocabulary. This prevents drift and ensures reproducibility.

### 12.7 Running the Reference Implementation

To validate your understanding with executable code:

```bash
# Clone or locate the public repository
cd /path/to/crystal-information-engine

# Run the phase demo (Milestone A)
PYTHONPATH=. python3 scripts/csif_crystal_phase_demo.py

# Run the whale coherent vs. contradictory experiment (Milestone B)
PYTHONPATH=. python3 scripts/csif_whale_phase_contradiction_experiment.py

# Run validation protocol tests
PYTHONPATH=. python3 -m pytest -q tests/ -k "protocol"

# Inspect the milestone record for full technical evolution
cat docs/csif_crystal_phase_milestone.md
```

Each script outputs phase angles, torsion residuals, and resonance scores. Study these outputs to internalize the geometry.

### 12.8 Honest Limitations for AI Agents

When building and using CSIF crystals, be aware:

- **Determinism**: Current extraction and concept normalization paths are deterministic-simple. If your domain requires probabilistic or gradient-based reasoning, you will need to extend the phase model.
- **Scale**: External corpora require protocol-gate validation at specified counts (see §5). Small toy crystals won't reproduce protocol behavior.
- **Lexical→Semantic loop**: Reverse normalization (mapping lexical crystals back to semantic claims) is planned but not yet implemented. Forward (semantic→lexical) is live.
- **Closure**: Torsion closure is a necessary but not sufficient condition for coherence. A non-zero residual proves conflict; a zero residual does not guarantee truth.

Use CSIF as a **contradiction-detection mechanism and coherence audit tool**, not as a replacement for domain-specific reasoning. Combine it with your own knowledge integration and uncertainty quantification.

### 12.9 Summary: The Agent's Mental Model

Think of CSIF crystals as **phase-geometric snapshots of propositions**. Each snapshot records the relational structure and confidence state of a claim or belief. When you query the crystal bank, you are asking: "How does this new claim's phase geometry align with existing phase geometries?" Resonance is your answer—a geometric measure of harmony or discord.

By working with phases instead of discrete true/false labels, you gain:
- **Gradualism**: Room for uncertainty and nuance.
- **Auditability**: Each phase is tied to evidence traces.
- **Detectability**: Contradictions surface as measurable geometric residuals, not buried in semantic mismatch.

Use this model to reason more carefully about knowledge coherence.
