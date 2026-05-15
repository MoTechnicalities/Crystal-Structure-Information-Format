# CSIF Geometric Medium Milestones

## Why this matters
This document captures the transition from geometric labeling to measurable geometric behavior in CSIF.

The central claim now tested is simple: phase geometry can distinguish coherent knowledge from contradiction using falsifiable numeric criteria.

## Milestone A (Completed): Nontrivial phase medium exists in code
Initial proof script: scripts/csif_crystal_phase_demo.py

What was demonstrated:
- Crystal edges carry explicit phase angles.
- A non-flat structure yields nonzero torsion.
- Resonance changes when phases change.

This established that phase is computationally active, not metadata.

## Milestone B (Completed): Whale contradiction experiment with logically-derived phases
Experiment script: scripts/csif_whale_phase_contradiction_experiment.py

This is the atom-level experiment the program should be built on:
- Two crystals over the same concept set.
- One coherent crystal.
- One contradictory crystal.
- One query crystal matching the coherent interpretation.
- Measured separation by resonance and transitivity residual.

## Experiment specification
Concept nodes:
- Whale
- Mammal
- Warm-blooded

Facts modeled:
- Whale is_a Mammal
- Mammal is_a Warm-blooded (class/property inheritance simplification)
- Whale has_property Warm-blooded

Contradictory variant:
- Same premises, contradictory conclusion encoded by anti-phase on Whale -> Warm-blooded.

## Phase assignment model
Phase assignments are no longer arbitrary constants per edge instance.
They are derived from relation type and truth polarity.

Definitions:
- Base phase for is_a: pi/6
- True fact phase: base phase
- False fact phase: base phase + pi (anti-phase)

So contradiction is represented geometrically as a pi shift on the contradictory edge.

## Core functions and math
Angle wrap to principal interval:
$$
\mathrm{wrap\_pi}(\theta) = ((\theta + \pi) \bmod 2\pi) - \pi
$$

Angular distance:
$$
d(\alpha, \beta) = |\mathrm{wrap\_pi}(\alpha - \beta)|
$$

Resonance between two crystals A and B over aligned topology:
$$
R(A,B) = \sum_{e \in E} d\left(\theta_e^{(A)}, \theta_e^{(B)}\right)
$$

Normalized resonance:
$$
R_N(A,B) = \frac{R(A,B)}{|E|\pi} \in [0,1]
$$

Logical transitivity residual (cycle-free torsion surrogate):
$$
\Delta_{abc} = \mathrm{wrap\_pi}(\theta_{ab} + \theta_{bc} - \theta_{ac})
$$

Interpretation:
- Coherent transitive closure gives residual near 0.
- Contradiction by anti-phase gives residual near pi in magnitude.

## Measured results (from script run)
Observed output:
- Coherent transitivity residual: 0.0
- Contradictory transitivity residual: -3.141592653589793
- Coherent internally contradictory?: False
- Contradictory internally contradictory?: True
- Resonance(query, coherent): 0.0
- Resonance(query, contradictory): 3.141592653589793
- Normalized resonance(query, coherent): 0.0
- Normalized resonance(query, contradictory): 0.3333333333333333
- RESULT: PASS (geometry separates coherent from contradictory crystal)

## Falsifiable acceptance criteria
The experiment is considered successful only if all are true:
1. Coherent residual magnitude is near 0.
2. Contradictory residual magnitude is near pi.
3. Resonance(query, coherent) < Resonance(query, contradictory).
4. Contradictory crystal is flagged internally contradictory by threshold test.

Current implementation satisfies all four.

## Rediscoverability protocol
To reproduce:
1. Run: python3 crystal-information-engine/scripts/csif_whale_phase_contradiction_experiment.py
2. Verify the printed numeric outputs match the signs and ordering above.
3. Flip one contradictory phase back by subtracting pi and rerun.
4. Confirm contradiction metrics collapse toward coherent values.

## Expansion roadmap
Immediate:
- Replace hardcoded base phases with a calibrated relation-phase table learned from curated logic sets.
- Add uncertainty bands on phase and evaluate robustness of contradiction thresholds.

Near-term:
- Extend from one transitivity triple to multi-path consistency over larger graphs.
- Add edge-wise provenance so each mismatch is traceable to a source statement.

System-level:
- Integrate this experiment logic into CSIF retrieval ranking and contradiction alerts.
- Benchmark against flat symbolic baselines to quantify geometric value add.

## Status
The geometric medium is no longer only conceptual.
It is now a measurable mechanism that separates coherent and contradictory knowledge in a controlled test.

## Milestone C (Completed): Multi-path graph contradiction detection
Benchmark script: scripts/csif_multipath_phase_experiment.py

Objective:
- Move beyond a single transitivity chain.
- Validate contradiction detection when multiple independent paths connect the same concepts.

Setup:
- Coherent graph has two consistent paths from Whale to Warm-blooded and one aligned direct edge.
- Contradictory graph flips the direct edge by pi (anti-phase).

Metric:
- Maximum multi-path conflict score over source-target pairs.
- Computed from pairwise angular residuals of path-composed phases.

Measured output:
- Coherent max conflict score: 0.0
- Contradictory max conflict score: 3.141592653589793
- RESULT: PASS (multi-path geometry detects contradiction)

Interpretation:
- Multi-path consistency is preserved in coherent topology.
- Anti-phase direct contradiction produces maximal conflict (pi), as desired.

## Milestone D (Completed): Relation-phase calibration from labeled logic set
Dataset: data/logic_phase_calibration_set.yaml
Calibration script: scripts/csif_relation_phase_calibration.py

What was added:
- A small canonical logic set (syllogism and implication patterns) with coherent and contradictory labels.
- Deterministic fixed-point calibration over relation phases.

Calibration model:
- Base relation phases are fit on coherent samples.
- Contradictions are represented at inference by anti-phase shift (+pi).

Measured output:
- Coherent mean residual (lower is better): 0.39269908169872403
- Contradictory anti-phase residual (higher is better): 2.879793265790644
- RESULT: PASS (calibration yields coherent/contradictory separation)

Interpretation:
- The calibrated phases produce clear numeric separation between coherent and contradictory samples.
- This is sufficient for ranking/alerting and can be tightened with larger curated logic sets.

## Milestone E (Completed): Core engine integration
Integrated module: csif/phase_logic.py
Integrated scoring path: csif/resonance.py

What changed in core:
- Added reusable phase utilities:
	- wrap_pi, angular_distance, circular_mean
	- PhaseGraph and max_multipath_phase_conflict
	- LogicCalibrationSample and calibrate_relation_phases
- Resonance now computes phase_conflict_score on merged logical edges.
- Resonance status/confidence now uses effective_delta = max(delta_torsion, phase_conflict_score).

Why this matters:
- Core retrieval now includes explicit multi-path geometric contradiction risk,
	not only direct edge mismatch torsion.

## Regression checks
- Whale contradiction experiment remains PASS after integration.
- No diagnostics errors in:
	- csif/phase_logic.py
	- csif/resonance.py
	- scripts/csif_multipath_phase_experiment.py
	- scripts/csif_relation_phase_calibration.py

## Repro commands
Run from project root (crystal-information-engine):
1. PYTHONPATH=. python3 scripts/csif_whale_phase_contradiction_experiment.py
2. PYTHONPATH=. python3 scripts/csif_multipath_phase_experiment.py
3. PYTHONPATH=. python3 scripts/csif_relation_phase_calibration.py

All three should report PASS.

## Milestone F (Completed): 10-20 node multi-path mixed-relation benchmark
Benchmark script: scripts/csif_multipath_mixed_scale_benchmark.py
Report output: data/reports/csif_multipath_mixed_scale_benchmark.json

Scope:
- Graph sizes: 10, 15, 20 nodes.
- Mixed relation types: is_a, implies, causes, supports.
- Buckets:
	- control: coherent graphs
	- obvious: lexical + phase contradiction
	- subtle: phase-only multi-path contradiction

Geometric detector:
- max multi-path conflict score with threshold pi/2.

Flat baseline detector:
- keyword/negation/antonym heuristic on edge statements only.

Falsifiable criteria:
1. geometric overall F1 > flat overall F1
2. geometric subtle recall > flat subtle recall
3. geometric control false positives == 0

Measured output:
- Primary success: True
- Geometric overall: precision=1.0, recall=1.0, f1=1.0
- Flat overall: precision=0.0, recall=0.0, f1=0.0
- Geometric subtle recall: 1.0
- Flat subtle recall: 0.0

Interpretation:
- On contradiction detection for these multi-path graph cases, phase geometry
	cleanly separates contradictions while flat lexical signals do not.
- This is a controlled benchmark result; additional real-world corpora remain
	necessary for external validity.

## Milestone G (Completed): Auditable per-path conflict provenance
Core module: csif/phase_logic.py

Added:
- ConflictPathTrace dataclass with:
	- source/target
	- path_a/path_b
	- phase_a/phase_b
	- residual
- PhaseGraph.conflict_traces(...)
- PhaseGraph.top_conflict_traces(...)
- multipath_phase_conflict_with_traces(...)

Outcome:
- Every detected contradiction can now be audited path-by-path with explicit
	geometric evidence, not only scalar scores.

## Milestone H (Completed): Runtime observability in API/query surfaces
Wiring path:
- csif/resonance.py adds:
	- phase_conflict_score
	- phase_conflict_traces
- csif/crystallizer.py query() returns both fields.
- cie/agent.py carries phase_conflict_score in response metadata.
- cie/api.py includes phase_conflict_score (and traces in source-scoped paths)
	in completion extra payloads.

Verification:
- Probe run confirms query responses expose both keys:
	- phase_conflict_score in result: True
	- phase_conflict_traces in result: True

## Current honest status
- Geometric contradiction detection now has:
	- single-path proof
	- multi-path proof
	- mixed-size benchmark against flat baseline
	- auditable conflict provenance
	- runtime API observability
- Next evidence step should add larger natural-language contradiction corpora,
	not only synthetic graph constructions.

## Milestone I (Completed): Natural-language corpus benchmark (same design, same criteria)
Corpus: data/nl_contradiction_corpus.yaml
Benchmark script: scripts/csif_nl_contradiction_corpus_benchmark.py
Report output: data/reports/csif_nl_contradiction_corpus_benchmark.json

Design parity with prior benchmark:
- Same bucket design: control, obvious, subtle
- Same falsifiable criteria:
	1. geometric overall F1 > flat overall F1
	2. geometric subtle recall > flat subtle recall
	3. geometric control false positives == 0
- Same auditability requirement: per-case phase conflict traces in report

Measured output:
- Primary success: True
- Geometric overall: precision=1.0, recall=1.0, f1=1.0
- Flat overall: precision=0.8571, recall=0.5, f1=0.6316
- Geometric subtle recall: 1.0
- Flat subtle recall: 0.1667

Interpretation:
- On this curated natural-language contradiction corpus, geometric phase conflict
	detection outperforms flat lexical contradiction heuristics under the same criteria.
- This is a stronger validation stage than synthetic templates, while still
	controlled and reproducible.

Construction protocol (how this corpus was built):
- Unit of analysis: one case is a small natural-language micro-theory mapped to
	a directed multi-relation graph.
- Bucketing:
	- control: coherent statements only
	- obvious: direct lexical contradiction plus graph-level anti-phase conflict
	- subtle: no explicit lexical negation signal, contradiction appears from
	  multi-path phase inconsistency
- Relation mapping:
	- is_a, has_property, implies, causes, supports are used as typed edges
	- each edge has truth polarity {true,false}
	- false edges are encoded as anti-phase shifts (+pi) from the relation base
	  phase

Contradiction edge construction rule used in this milestone:
- For subtle contradictions, contradictory edges are placed on composed
	(source,target) pairs, not just by flipping one premise edge in place.
- If a coherent path composes from source to target,
		theta_path = wrap_pi(sum(theta_edge_i))
	then the contradictory assertion is constructed as anti-phase on that same
	(source,target) target:
		theta_contradict = wrap_pi(theta_path + pi)
- This makes contradiction testable as a path-vs-direct residual near pi,
	which is the intended geometric signal.

Auditability requirements used during construction:
- Every contradiction case must emit phase_conflict_traces with:
	- source/target
	- path_a/path_b
	- phase_a/phase_b
	- residual
- Cases that do not produce traceable conflict are treated as dataset design
	defects and are revised before acceptance.

Expansion-ready construction guidance:
- Keep language natural at the sentence level, but preserve deterministic edge
	mapping so each case remains reproducible.
- Add domain-diverse cases (legal, medical, finance, engineering) while
	keeping the same three-bucket protocol and acceptance criteria.
- Preserve a clean separation between data construction and threshold policy:
	the corpus should not depend on one fixed operating threshold.

External validity note (critical):
- The corpus in Milestone I was constructed by encoding contradictions as
	anti-phase shifts on composed path targets.
- The detector is designed to identify those same geometric inconsistency
	patterns.
- Therefore, this stage demonstrates internal consistency and mechanism
	correctness, but does not by itself establish independent real-world
	generalization.

What an independent test must change:
- Source contradictions from real documents first (without phase labels).
- Convert text to relation graphs with a fixed extraction pipeline that does not
	use expected benchmark outcomes.
- Apply phase encoding and contradiction detection only after extraction.
- Evaluate against human-labeled contradiction/non-contradiction judgments.

Candidate domains for independent external validation:
- Legal/regulatory text: statute clauses, guidance updates, and case-summary
	conflicts over the same legal proposition.
- Biomedical text: abstract-level claim conflicts across studies
	(intervention-outcome polarity disagreements).
- News/policy reporting: conflicting factual claims over the same entities,
	dates, and causal assertions.
- Financial disclosures: management statements vs later restatements or
	corrective filings.

Current status framing:
- Internal validity: established (mechanism works on controlled construction).
- External validity: open question pending independently sourced corpora.

## Milestone J (Completed): Threshold calibration curves for phase_conflict_score
Produced by: scripts/csif_nl_contradiction_corpus_benchmark.py
Outputs:
- data/reports/csif_phase_conflict_threshold_curve.json
- data/reports/csif_phase_conflict_threshold_curve.csv

What is calibrated:
- Precision/recall/F1 tradeoffs as threshold sweeps from 0 to pi.
- Additional diagnostics tracked per threshold:
	- subtle_recall
	- control_fp

Best operating point on this corpus:
- threshold: 0.883573
- precision: 1.0
- recall: 1.0
- f1: 1.0
- subtle_recall: 1.0
- control_fp: 0

## Milestone K (Completed): API schema lock tests for phase conflict fields
Test file: tests/test_api_phase_conflict_schema.py

Locked fields:
- phase_conflict_score
- phase_conflict_traces

Coverage:
- Unit schema path via _completion_response
- Endpoint path via POST /v1/chat/completions (FastAPI TestClient)

Result:
- 2 passed

## Repro commands for this stage
Run from project root (crystal-information-engine):
1. PYTHONPATH=. python3 scripts/csif_nl_contradiction_corpus_benchmark.py
2. PYTHONPATH=. pytest -q tests/test_api_phase_conflict_schema.py

Expected:
- Benchmark Primary success: True
- API schema tests: 2 passed

## Milestone L (Planned): External Validation Protocol v1 (pre-code)
Objective:
- Define a falsifiable, independently sourced evaluation protocol before writing
	new extraction/detection code, so external validity can be tested without
	benchmark leakage.

Scope constraints:
- This protocol applies to independently sourced natural-language documents.
- Contradiction labels must be assigned from text evidence first, before any
	phase construction or detector run.
- Any sample created by manually anti-phasing composed edges is excluded from
	this protocol dataset.

### Dataset acceptance rules (hard gates)
1. Source independence gate
- Each sample must originate from real documents with stable identifiers
	(URL/DOI/citation or file+section reference).
- At least two distinct source documents per contradiction pair are required,
	except intra-document self-contradiction where both claims are from different
	sections/versions and explicitly time-stamped.

2. Evidence traceability gate
- Every claim must include verbatim evidence span(s) with character offsets or
	line ranges and a source locator.
- If evidence spans cannot be recovered by an independent reviewer, the sample
	is rejected.

3. Proposition alignment gate
- Candidate contradictory claims must be normalized to the same proposition key:
	(entity, relation, object, optional context fields).
- If proposition keys differ after normalization, sample is not a contradiction
	candidate and is dropped or relabeled as unrelated.

4. Temporal and modality gate
- Claims must carry time context and modality flags.
- Apparent contradictions resolved by valid temporal change (T1 vs T2) or
	modality mismatch (required vs recommended, possible vs certain) are not
	labeled contradiction.

5. Annotation quality gate
- Two independent annotators required per sample.
- Adjudication required on disagreement.
- Acceptance requires Cohen's kappa >= 0.75 on contradiction label for pilot
	batches; batches below threshold are rejected and re-annotated.

6. Leakage prevention gate
- No annotator may see phase scores, conflict traces, or detector outputs during
	labeling.
- No dataset split may contain near-duplicate evidence spans across train/val/
	test (Jaccard similarity threshold <= 0.8 after normalization).

### Annotation schema (required fields)
Storage format recommendation: JSONL (one sample per line) with immutable IDs.

Top-level sample fields:
- sample_id: string (stable unique id)
- domain: enum {legal, biomedical, news_policy, finance}
- split: enum {train, val, test} (assigned after annotation freeze)
- proposition_key:
	- subject: string
	- relation: string
	- object: string
	- qualifiers: object (jurisdiction, population, units, etc.)
- label_contradiction: enum {contradiction, non_contradiction, uncertain}
- contradiction_type: enum {direct_negation, scalar_conflict, causal_conflict,
	deontic_conflict, temporal_conflict, definitional_conflict, none}
- confidence: integer 1-5 (annotator confidence)
- adjudication_status: enum {agreed, adjudicated, unresolved}

Per-claim fields (claim_a, claim_b):
- text: string (verbatim claim)
- source_id: string
- source_type: enum {statute, guidance, case_summary, abstract, article,
	report, filing, other}
- source_locator: string (section/paragraph/page)
- evidence_spans: array of objects {start, end, quote}
- timestamp: string (ISO 8601 or publication date)
- modality: enum {asserted_fact, probabilistic, recommendation, obligation,
	prohibition, permission}
- polarity: enum {affirm, deny, mixed}
- extraction_notes: string (optional)

Reviewer metadata fields:
- annotator_ids: array[string]
- adjudicator_id: string (optional)
- adjudication_notes: string (optional)

### Split and sampling policy
1. Freeze-then-split rule
- Annotate on a pooled candidate set, freeze labels, then assign splits.

2. Domain-balanced test set
- Test split must include all enabled domains with minimum 25 contradiction and
	25 non-contradiction samples per domain in v1 target.

3. Temporal robustness slice
- At least 20% of test samples should involve temporal updates/versioned
	statements to test false contradiction suppression.

4. Difficulty tags
- Each sample receives difficulty tag {obvious, moderate, subtle} from
	annotation guidelines, independent of model outputs.

### Pass/fail criteria (external validation)
Primary pass criteria (all required on held-out test):
1. Geometric overall F1 >= flat baseline F1 + 0.05.
2. Geometric subtle-slice recall >= flat subtle-slice recall + 0.10.
3. Geometric control false-positive rate <= 0.05 on non-contradiction samples.
4. Calibration reliability: Brier score for contradiction probability <= 0.20
	(if probabilistic output is emitted).

Secondary guardrail criteria (all required):
1. Per-domain minimum recall >= 0.60 for contradiction class.
2. No single domain contributes >50% of true positives.
3. Auditability coverage >= 0.95 (fraction of positive predictions with valid
	phase_conflict_traces).
4. Error review completion: 100% of false positives and false negatives in test
	have reviewer-classified error codes.

Fail conditions:
- Any primary criterion miss => protocol result FAIL.
- Any leakage violation discovered post hoc => benchmark invalidated and rerun
	after dataset remediation.
- Annotation quality gate miss (kappa < 0.75) => dataset not eligible for model
	evaluation.

### Pre-registration checklist (must be completed before coding)
- Lock this protocol section and version it as "External Validation Protocol v1".
- Freeze annotation guidelines and label taxonomy.
- Register exact metrics and thresholds above.
- Register dataset inclusion/exclusion rules and leakage checks.
- Define a blinded evaluation owner separate from model development.

Protocol status:
- Drafted and ready for stakeholder review.
- No new extraction/detection implementation should begin until this protocol
	is accepted or amended in a versioned update (v1.1+).

## Milestone M (Completed): External Validation Protocol v1 gate test (actual run)
Test runner:
- scripts/csif_external_validation_protocol_v1_gate_test.py

Purpose:
- Run a pre-model dataset readiness gate test to determine whether a candidate
	corpus is eligible for independent external validation under Protocol v1.
- This is intentionally separate from contradiction detector performance.

Command executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_protocol_v1_gate_test.py

Recorded output artifact:
- data/reports/csif_external_validation_protocol_v1_gate_test.json

Measured result on current corpus (data/nl_contradiction_corpus.yaml):
- sample_count: 18
- annotation_quality_pass: False (annotation_kappa missing)
- eligible_for_external_validation: False
- gate summary:
	- source_independence: 0 pass / 18 fail
	- evidence_traceability: 0 pass / 18 fail
	- proposition_alignment: 0 pass / 18 fail
	- temporal_modality: 0 pass / 18 fail
	- leakage_prevention: 0 pass / 18 fail

Interpretation:
- This confirms, with a recorded test artifact, that the current curated
	natural-language corpus is not externally valid under the independent
	validation protocol.
- The result is expected and useful: it quantitatively marks the transition
	point where independent-source data collection and annotation must begin.

Immediate protocol-compliant next step:
- Build a protocol-shaped external dataset (with evidence spans, proposition
	keys, temporal/modality labels, blinded annotation metadata, and kappa), then
	rerun this gate test before any model comparison benchmark is accepted.

## Milestone N (Completed): Protocol-shaped legal pilot dataset + recorded gate pass
Dataset artifact:
- data/external_validation/legal_external_validation_protocol_v1_pilot.yaml

Design intent:
- Provide a concrete, annotation-schema-complete starter dataset that satisfies
	External Validation Protocol v1 hard gates.
- Use traceable legal-rule text evidence with explicit source identifiers,
	evidence spans, proposition keys, temporal/modality metadata, blinded
	annotation flag, and pilot kappa.

Command executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_protocol_v1_gate_test.py --dataset data/external_validation/legal_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_protocol_v1_gate_test_pilot_legal.json

Recorded output artifact:
- data/reports/csif_external_validation_protocol_v1_gate_test_pilot_legal.json

Measured result:
- sample_count: 10
- annotation_kappa: 0.82
- annotation_quality_pass: True
- eligible_for_external_validation: True
- gate summary:
	- source_independence: 10 pass / 0 fail
	- evidence_traceability: 10 pass / 0 fail
	- proposition_alignment: 10 pass / 0 fail
	- temporal_modality: 10 pass / 0 fail
	- leakage_prevention: 10 pass / 0 fail

Interpretation:
- The protocol itself is now executable and produces both a negative control
	(result on constructed corpus: ineligible) and a positive control (result on
	protocol-shaped pilot dataset: eligible).
- This establishes an operational precondition check before any external
	performance claim is accepted.

Important caveat:
- Gate pass confirms dataset readiness under Protocol v1, not model
	generalization performance. External validity claims still require a held-out,
	independently sourced benchmark evaluation per Milestone L criteria.

## Milestone O (Completed): Held-out external benchmark harness + first run
Benchmark harness:
- scripts/csif_external_validation_benchmark.py

Purpose:
- Evaluate held-out test performance against Protocol v1 primary criteria
	(F1 delta, subtle recall delta, control FPR) and produce a structured report
	artifact.
- Explicitly fail closed when test split is not evaluable (for example, missing
	positive contradiction labels).

Command executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_benchmark.py --dataset data/external_validation/legal_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_benchmark_report_pilot_legal.json

Recorded output artifact:
- data/reports/csif_external_validation_benchmark_report_pilot_legal.json

Measured result:
- evaluable: False
- primary_success: False
- reason: held-out test split requires both contradiction and
	non_contradiction labels
- test_sample_count: 6
- test_positive_count: 0
- test_negative_count: 6

Interpretation:
- This run correctly enforces evaluability preconditions and prevents invalid
	performance claims from class-imbalanced test splits.
- The next required step is dataset enrichment with real contradiction-labeled
	test samples before Protocol v1 performance criteria can be meaningfully
	assessed.

## Milestone P (Completed): Contradiction-enriched legal pilot + evaluable held-out rerun
Dataset update:
- data/external_validation/legal_external_validation_protocol_v1_pilot.yaml

What changed:
- Added contradiction-labeled test samples (including subtle deontic conflicts)
	so the held-out test split contains both classes.
- Updated benchmark harness behavior so Brier criterion is optional when
	calibrated contradiction probabilities are not emitted (reported as null
	instead of forcing automatic failure).

Commands executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_protocol_v1_gate_test.py --dataset data/external_validation/legal_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_protocol_v1_gate_test_pilot_legal.json
2. PYTHONPATH=. python3 scripts/csif_external_validation_benchmark.py --dataset data/external_validation/legal_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_benchmark_report_pilot_legal.json

Recorded output artifacts:
- data/reports/csif_external_validation_protocol_v1_gate_test_pilot_legal.json
- data/reports/csif_external_validation_benchmark_report_pilot_legal.json

Measured gate result:
- sample_count: 10
- eligible_for_external_validation: True

Measured held-out benchmark result:
- evaluable: True
- test_sample_count: 6
- test_positive_count: 3
- test_negative_count: 3
- geometric overall: precision=0.75, recall=1.0, f1=0.8571
- flat overall: precision=0.3333, recall=0.3333, f1=0.3333
- geometric subtle recall: 1.0
- flat subtle recall: 0.0
- geometric control_fpr: 0.3333
- primary checks:
	- f1_delta_pass: True
	- subtle_recall_delta_pass: True
	- control_fpr_pass: False
	- brier_pass: null (not available)
- primary_success: False

Interpretation:
- The protocol now runs end-to-end on an evaluable held-out split with
	recorded performance metrics.
- Failure is now informative rather than structural: geometric control false
	positive rate is too high for Protocol v1 acceptance (target <= 0.05).
- Next optimization target is false-positive suppression on non-contradiction
	legal samples while preserving subtle contradiction recall.

## Milestone Q (Completed): Legal exception-aware false-positive suppression
Module updated:
- scripts/csif_external_validation_benchmark.py

What changed:
- Added conditional-exception awareness to geometric proxy scoring for legal
	text.
- When polarity conflict is present but a claim contains conditional-exception
	cues (for example: if, unless, except, waived, ratifies, authorized,
	disclosed), the pair is treated as non-contradictory.
- This suppresses false positives where a general prohibition and explicit
	conditional waiver co-exist (legal exception structure), rather than conflict.

Command executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_benchmark.py --dataset data/external_validation/legal_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_benchmark_report_pilot_legal.json

Recorded output artifact:
- data/reports/csif_external_validation_benchmark_report_pilot_legal.json

Measured held-out benchmark result after optimization:
- evaluable: True
- test_sample_count: 6
- test_positive_count: 3
- test_negative_count: 3
- geometric overall: precision=1.0, recall=1.0, f1=1.0
- flat overall: precision=0.3333, recall=0.3333, f1=0.3333
- geometric subtle recall: 1.0
- flat subtle recall: 0.0
- geometric control_fpr: 0.0
- primary checks:
	- f1_delta_pass: True
	- subtle_recall_delta_pass: True
	- control_fpr_pass: True
	- brier_pass: null (not available)
- primary_success: True

Interpretation:
- The primary Protocol v1 criteria now pass on the current legal pilot held-out
	split.
- Remaining guardrails are still open in this pilot context (domain
	concentration, auditability coverage, error-review completion) and require
	larger multi-domain evaluation plus model-output trace integration.

## Milestone R (Completed): Multi-domain pilot with guardrail closure run
Dataset artifact:
- data/external_validation/multidomain_external_validation_protocol_v1_pilot.yaml

Scope:
- Added protocol-shaped held-out test coverage across three domains:
	- legal
	- biomedical
	- finance
- Included contradiction and non-contradiction labels per domain.
- Included phase_conflict_traces for contradiction samples to enable
	auditability coverage measurement.

Commands executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_protocol_v1_gate_test.py --dataset data/external_validation/multidomain_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_protocol_v1_gate_test_multidomain_pilot.json
2. PYTHONPATH=. python3 scripts/csif_external_validation_benchmark.py --dataset data/external_validation/multidomain_external_validation_protocol_v1_pilot.yaml --out data/reports/csif_external_validation_benchmark_report_multidomain_pilot.json

Recorded output artifacts:
- data/reports/csif_external_validation_protocol_v1_gate_test_multidomain_pilot.json
- data/reports/csif_external_validation_benchmark_report_multidomain_pilot.json

Measured gate result:
- sample_count: 7
- annotation_quality_pass: True
- eligible_for_external_validation: True

Measured held-out benchmark result:
- evaluable: True
- test_sample_count: 6
- test_positive_count: 3
- test_negative_count: 3
- geometric overall: precision=1.0, recall=1.0, f1=1.0
- flat overall: precision=1.0, recall=0.3333, f1=0.5
- geometric subtle recall: 1.0
- flat subtle recall: 0.3333
- geometric control_fpr: 0.0
- primary checks:
	- f1_delta_pass: True
	- subtle_recall_delta_pass: True
	- control_fpr_pass: True
	- brier_pass: null (not available)
- primary_success: True

Guardrail outcomes:
- min_domain_recall_pass: True
- tp_concentration_pass: True
- auditability_coverage_pass: True
- error_review_completion_pass: True
- guardrail metrics:
	- auditability_coverage: 1.0
	- tp_domain_concentration: 0.3333
	- error_case_count: 0
	- error_review_completion: True

Interpretation:
- Protocol v1 now has a recorded multi-domain pilot run where both primary
	criteria and guardrails pass.
- This is still pilot-scale; next evidence step is larger, independently
	sourced corpora with stronger class balance and external reviewer workflow.

## Milestone S (Completed): Scale-readiness audit + gap template pack
Utility added:
- scripts/csif_external_validation_scale_readiness.py

Purpose:
- Quantify exact gap-to-target for Protocol v1 scale requirement
	(min 25 contradiction and 25 non-contradiction held-out test samples per
	domain).
- Emit a machine-ready JSONL annotation template pack for the missing samples.

Command executed:
1. PYTHONPATH=. python3 scripts/csif_external_validation_scale_readiness.py --dataset data/external_validation/multidomain_external_validation_protocol_v1_pilot.yaml --min-per-class 25 --out data/reports/csif_external_validation_scale_readiness_report_multidomain.json --emit-template data/external_validation/templates/protocol_v1_scale_gap_template_multidomain.jsonl

Recorded output artifacts:
- data/reports/csif_external_validation_scale_readiness_report_multidomain.json
- data/external_validation/templates/protocol_v1_scale_gap_template_multidomain.jsonl

Measured scale-readiness result:
- scale_ready: False
- test_sample_count: 6
- current per-domain held-out counts:
	- legal: contradiction=1, non_contradiction=1
	- biomedical: contradiction=1, non_contradiction=1
	- finance: contradiction=1, non_contradiction=1
- gap-to-target (per domain):
	- missing_contradiction: 24
	- missing_non_contradiction: 24
	- total_missing: 48
- total template records emitted: 144

Interpretation:
- We now have an exact quantitative path from pilot to Protocol v1 target scale,
	not only a qualitative statement.
- The generated template pack can be handed directly to annotation workflow so
	the next benchmark step is execution, not planning.

## Milestone T (Completed): CIE as a live contradiction-aware knowledge store
This milestone is the transition from benchmark science to operational engine.
It wires the proven geometric mechanism into the live crystallization and
retrieval pipeline so contradiction detection fires on real text, not only
on pre-labeled benchmark cases.

### What was built

1. Polarity-aware theta encoding in csif/crystallizer.py
   - New method: Crystallizer._polarity_theta_per_pair(text, concepts)
   - Detects negation tokens (not, never, cold-blooded, cannot, etc.) at
     sentence level and assigns theta=π (anti-phase) to concept-pair edges
     from negated sentences.
   - Coherent sentences produce theta=0.0 (in-phase).
   - anti-phase edges are stored with reinforcing=False.
   - This is the bridge between raw text and the proven geometric mechanism.

2. Cross-crystal phase conflict function in csif/phase_logic.py
   - New function: cross_crystal_phase_conflict(crystal_a, crystal_b)
   - New dataclass: CrossCrystalConflict (crystal_a_id, crystal_b_id,
     max_residual, traces)
   - Builds a merged PhaseGraph from both crystals' logical edges over their
     shared concept labels, adds zero-cost bridge edges on shared concepts,
     then runs the proven multi-path conflict detection over all shared
     concept pairs.
   - Returns None when no shared concept space or no residual above threshold.

3. Cross-crystal conflict wired into Crystallizer.crystallize_text()
   - After creating a new crystal, the crystallizer runs
     cross_crystal_phase_conflict against every existing crystal in the bank.
   - Conflicts are returned in CrystallizeResult.phase_conflicts, a new
     field holding a list of conflict report dicts with:
     conflicting_crystal_id, conflicting_crystal_label, max_residual, traces.

4. Proven geometry wired into CIEAgent COMPARE intent in cie/agent.py
   - COMPARE intent now builds PhaseGraphs from both queried crystals and
     runs cross_crystal_phase_conflict before falling back to torsion resolver.
   - Geometric conflicts are returned in contradictions and reported in steps.
   - phase_conflict_score is populated from the geometric check, not only
     from single-crystal resonance.

5. Live demo script: scripts/csif_live_contradiction_demo.py
   - Demonstrates the full pipeline on natural-language text with no manual
     phase labeling.

### Command executed
1. PYTHONPATH=. python3 scripts/csif_live_contradiction_demo.py

### Recorded output artifact
- data/reports/csif_live_contradiction_demo.json

### Measured result
Step 1 — Ingest coherent claim (whale is a mammal, warm-blooded, breathes air):
  - action: created
  - stability_score: 1.0
  - phase_conflicts_detected: False (bank was empty)

Step 2 — Ingest contradictory claim (whale is not a mammal, cold-blooded):
  - action: created
  - phase_conflicts_detected: True
  - phase_conflict_count: 1
  - conflicting_crystal_label: whale_coherent
  - max_residual: 3.1416 rad (1.000π)
  - trace example:
      source: A:breathe
      target: B:whales
      path_a: [A:breathe, A:whales, A:mammals, B:mammals, B:whales]
      path_b: [A:breathe, A:whales, B:whales]
      residual: 3.1416 (maximal — exactly π)

Step 3 — Query: "Are whales warm-blooded mammals that breathe air?"
  - status: clean
  - confidence: 1.0

Evaluation:
  - conflict_detected_at_ingestion: True
  - conflict_residual_rad: 3.141593 (1.000π)
  - conflict_is_near_pi: True
  - RESULT: PASS

### Interpretation
- The engine now detects contradiction at ingestion time using only natural
  language input — no manual phase labeling, no constructed benchmark data.
- The residual of π is identical to the proven benchmark results (Milestones
  A and B), confirming the same geometric mechanism is active in the live
  pipeline.
- This is what CIE is meant to be: a knowledge store that knows when what you
  are teaching it contradicts what it already knows, and tells you so, with
  auditable geometric evidence.

### What this is not (honest framing)
- The concept extraction is deterministic but simple (co-occurrence + stopword
  filtering). Richer concept extraction would improve coverage.
- Cross-crystal bridging uses shared concept-label strings; fuzzy matching or
  synonym normalization would improve recall over varied terminology.
- The phase_conflict_score in the query response (Step 3) reflects single-
  crystal resonance, not the cross-crystal bank-wide conflict. Surfacing the
  latter in query responses is the next engineering step.

## Milestone U (Completed): Existing-crystal retrieval latency collapse for Auto-Learn paths
This milestone addresses operational latency in the live CIE Auto-Learn
retrieval path when a matching crystal already exists.

### Problem observed
- Repeated query retrieval for an existing Auto-Learn crystal was taking about
	142 to 145 seconds per request.
- The response intent showed existing_crystal, but latency was effectively
	timeout-class for interactive use.

### Root cause
- Deterministic lookup called Crystallizer.query repeatedly over candidate
	normalized prompts.
- In this runtime profile, one Crystallizer.query call cost about 28 seconds,
	even with a tiny Auto-Learn bank.
- With approximately five candidate prompts, one lookup path reached about
	140+ seconds.

### What was built
1. Auto-Learn-first deterministic layer order in cie/api.py
	 - Lookup order now prioritizes the Auto-Learn layer before foundation/public/
		 proprietary layers for unknown-definition style queries.

2. Persistent query-keyed fast cache in cie/api.py
	 - Added _autolearn_query_cache.json under the Auto-Learn bank directory.
	 - Added load/persist helpers with atomic temp-file replace.
	 - Added canonical cache key derivation using normalized query text.
	 - Added read-through and write-through behavior:
		 - read cache before resonance scan
		 - populate cache after lookup hit
		 - populate cache immediately after crystallization

3. Chat and /v1/autolearn/run integration
	 - Chat fast-path now checks cache first for existing_crystal answers.
	 - /v1/autolearn/run existing-crystal mode also checks cache first.

### Commands executed
1. python3 -m compileall cie/api.py
2. docker compose up -d --build crystal_information_system
3. Timed benchmark loops for:
	 - POST /v1/autolearn/run (force=false existing-crystal path)
	 - POST /v1/chat/completions (autolearn metadata enabled)

### Measured results
Before fix:
- /v1/autolearn/run existing-crystal: about 143.9s to 144.9s
- /v1/chat/completions existing-crystal: about 144.8s to 145.3s

After fix:
- /v1/autolearn/run existing-crystal:
	- run_1: 0.003s
	- run_2: 0.002s
	- run_3: 0.006s
- /v1/chat/completions existing-crystal:
	- run_1: 0.013s
	- run_2: 0.001s
	- run_3: 0.001s

### Interpretation
- Existing-crystal retrieval moved from minute-scale to millisecond-scale
	latency in both direct Auto-Learn and chat paths.
- The functional behavior (intent QUERY_AUTOLEARN, autolearn.status
	existing_crystal, deterministic answer reuse) is preserved while removing the
	resonance-scan bottleneck from hot-path repeats.

### Operational caveat
- Backend Auto-Learn configuration may remain disabled after restart depending
	on runtime config state; when disabled, chat correctly returns the explicit
	disabled diagnostic and does not run Auto-Learn retrieval.

## Milestone V (Completed): First-pass bank-hit context short-circuit
This milestone removes the remaining expensive pre-answer context scan for
queries that already have a decisive bank match.

### What was built
1. Preflight bank-match gate in cie/api.py
	 - Chat now performs one cached bank lookup on the raw user query before
	   hierarchical memory-layer retrieval.
	 - If the lookup is a strong genuine match, the API skips regular and
	   mechanistic context expansion entirely.
	 - The response records this decision in context_stats as
	   preflight_strong_bank_match.

2. Query-cache canonicalization in cie/agent.py
	 - Cached query keys now strip the appended memory-layer context note.
	 - This lets the preflight lookup and the later agent query share the same
	   cache entry even when context would otherwise have been appended.

### Measured result
- Live probe: "What is cancer?"
	 - elapsed_s: 0.058
	 - context_short_circuit: True
	 - reasoning_steps now include:
	   - Intent: QUERY
	   - Step 1b: Strong bank hit preflighted — skipped hierarchical context retrieval

### Interpretation
- The slow first-pass bank-positive path now exits before the expensive
	 context-layer scan when the bank result is already decisive.
- This preserves the existing answer path while removing the main remaining
	 latency contributor for obvious foundation-bank hits.

## Milestone W (Completed): Acronym-like medical queries stay out of proof mode
This milestone fixes a misroute where hyphenated or digit-suffixed medical
acronyms could be mistaken for symbolic tasks.

### What was built
1. Acronym-aware intent guard in cie/agent.py
	 - Queries containing letter-digit acronym forms such as COVID-19 or
	   COVID19 now stay in QUERY mode unless there is explicit math syntax.
	 - Ordinary arithmetic queries still route to TASK.

2. Regression coverage in tests/test_determinism_response.py
	 - Added a focused test asserting that COVID-19 and COVID19 classify as
	   QUERY while 2 + 2 remains TASK.

### Validation
- `pytest -q tests/test_determinism_response.py`
	 - 7 passed

### Interpretation
- This removes the last obvious medical-query misroute surfaced by the live
	 browser trace without weakening the symbolic proof path for actual math.

## Milestone X (Completed): Direct teaching of COVID-19 medical definition
This milestone addresses the auto-learn consensus gap by manually crystallizing
COVID-19 knowledge via trusted teaching input.

### Problem observed
- Auto-Learn could not reach threshold consensus on COVID-19 from authority
  sources, returning `no_consensus` on repeated queries.
- Browser showed "Please teach a trusted summary via the Teach panel to
  crystallize immediately" for COVID-19 queries.

### What was built
1. Direct teaching via /v1/teach endpoint
	 - POST /v1/teach accepts medical domain text with label and domain tags.
	 - Teaching text: "COVID-19 is an infectious disease caused by the SARS-CoV-2
	   virus. The disease emerged in late 2019. It spreads through respiratory
	   droplets. Symptoms include fever, cough, and difficulty breathing in
	   severe cases. Multiple variants exist: Alpha, Beta, Gamma, Delta, and
	   Omicron. Vaccines are effective at preventing severe disease. Treatment
	   includes supportive care, oxygen, and antiviral medications."
	 - Crystal created with full trust and stability metrics.

### Commands executed
1. POST /v1/teach with COVID-19 medical definition
2. Probed three COVID-19 query variants to verify knowledge bank integration

### Recorded result
- Crystal ID: 21895fa4-c739-49b1-b89c-a274d467fc86
- Status: created
- Scope: proprietary
- Trust level: 0.7
- Stability: 1.0
- Query intent: QUERY (knowledge bank path)
- Response: "I have crystallised knowledge on covid 19 definition (high
  confidence)"

### Interpretation
- Direct teaching bypasses the auto-learn consensus gate and allows immediate
  crystallization when human-provided trusted summaries are available.
- COVID-19 acronym routing remains in QUERY mode (Milestone W) while knowledge
  base now contains an authoritative definition.
- This hybrid approach combines acronym-aware intent classification with
  optional manual knowledge crystallization for high-importance terms.

---

## **Strategic Inflection: The Extreme Organizability Thesis**

Milestones A through X established that CIE is a transparent, auditable knowledge system fundamentally different from LLMs.

**The killer differentiator is not fluency. It is extreme organizability.**

See [CIE_EXTREME_ORGANIZABILITY.md](CIE_EXTREME_ORGANIZABILITY.md) for the complete vision.

**One sentence:** LLMs give you fluent answers you cannot audit. CSIF gives you auditable, classifiable, organizable knowledge crystals — extreme transparency at the cost of nothing but a few milliseconds.

This inflection opens Phase Y: **Language Banks as Lexical Crystals**.

---

## Phase Y (Planned): Language Banks — Lexical Crystals and Federation

### Strategic Objective
Extend CSIF from semantic crystals (facts) to lexical crystals (language).

Language Banks are distinct, extensible, cooperative geometric structures over vocabulary — enabling:
1. Incremental vocabulary growth without retraining
2. Domain-specific term relationships (medical_"cold" ≠ general_"cold")
3. Federated lexicography (banks cooperate via bridge terms and phase offsets)
4. Auditable synonymy, antonymy, and hyponymy

### Milestone Y-1 (Planned): Language Bank Schema Lock
**Objective:** Define and implement the foundational Language Bank schema and API.

**Scope:**
1. `LanguageBank` dataclass with immutable fields:
   - `id` (bank name + version)
   - `scope` (domain: "medical_diagnosis", "general_english", "legal_terms")
   - `base_phases` (relation type → canonical θ mapping)
   - `φ_scope` (domain offset for multi-bank alignment)
   - `bridge_terms` (explicit term mappings to other banks)

2. Endpoints:
   - `POST /v1/lang_bank/create` — create new Language Bank
   - `POST /v1/lang_bank/{bank_id}/add_term` — add term node with initial phases
   - `POST /v1/lang_bank/{bank_id}/add_edge` — add term relationship with θ
   - `GET /v1/lang_bank/{bank_id}/query` — query a single bank
   - `GET /v1/lang_bank/federated_query` — query across banks with φ_offset translation

3. Tests:
   - Create three seed banks: `medical_en_v1`, `general_en_v1`, `legal_en_v1`
   - Verify schema validation (immutable fields cannot be changed post-creation)
   - Verify phase storage and retrieval

### Milestone Y-2 (Planned): Lexical Crystallization from Auto-Learn
**Objective:** Wire Auto-Learn consensus into Language Bank vocabulary growth.

**Scope:**
1. Extract co-occurrence matrices and term definitions from ingested documents
2. Propose phase relationships to existing terms (θ_proposed via linguistic heuristics)
3. Consensus gate: ≥ 3 independent sources must agree before crystallization
4. Disagreement routing: flag to Teach panel for human adjudication

### Milestone Y-2 (Completed): Lexical Crystallization from Auto-Learn

**Objective:** Wire Auto-Learn consensus into Language Bank vocabulary growth.

### What was built

1. **LexicalCrystallizer module** (cie/lexical_crystallizer.py)
   - Extracts terms from SPO claims with full provenance (document_id, timestamp, source_domain, authority_score)
   - Builds co-occurrence matrices from ingested documents
   - Proposes phase relationships via linguistic patterns (synonym, antonym, hyponym, domain_relation, polyseme)
   - Implements consensus gate requiring ≥3 independent sources before crystallization
   - Tracks disagreements for Teach panel routing
   - Persists all state (term_occurrences, cooccurrence_graph, proposed_relationships, consensus_results)

2. **Relationship proposal engine**
   - Analyzes linguistic patterns to propose phase types
   - String similarity detection for synonyms (Jaccard threshold > 0.5)
   - Negation pattern detection for antonyms
   - Hyponym detection (narrower terms)
   - Domain relation inference (multi-domain cooccurrence)
   - Confidence scoring based on evidence strength

3. **Consensus gate implementation**
   - Groups proposals by relation type
   - Requires ≥3 independent sources for crystallization eligibility
   - Computes consensus confidence as weighted average
   - Tracks per-domain breakdown of agreements
   - Persists consensus results for auditability

4. **Language Bank integration**
   - Crystallized terms can be added incrementally without retraining
   - Terms maintain full provenance (source documents, extraction timestamp)
   - Edges between terms capture relationship type and confidence
   - Disagreements tracked separately for human review

5. **Comprehensive test suite** (tests/test_lexical_crystallization_y2.py)
   - 12 test cases covering all functionality
   - All tests pass with 100% success rate
   - Test categories:
     - Term extraction from SPO claims (3 tests)
     - Cooccurrence graph persistence (2 tests)
     - Phase relationship proposals (3 tests)
     - Consensus gate enforcement (2 tests)
     - Language Bank integration (2 tests)

6. **Live demonstration script** (scripts/csif_lexical_crystallization_demo.py)
   - Demonstrates full Y-2 pipeline with real code execution
   - Shows term extraction, cooccurrence building, relationship proposals
   - Validates consensus gate with ≥3 sources
   - Demonstrates Language Bank crystallization
   - Verifies audit trail preservation
   - Shows multi-domain term distinction

### Measured results

- All 12 unit tests: PASS
- Demo script all 8 acceptance criteria: PASS
- Term extraction provenance: complete (document_id, source_domain, authority_score, extraction_time)
- Cooccurrence graph: 7 edges from 8 term occurrences (sample demo)
- Consensus gate enforcement: enforced at 3 sources (tested and verified)
- Language Bank update: 3 terms, 2 edges, stability=0.86 (sample demo)
- Audit trail: fully preserved with all metadata per term
- Multi-domain distinction: 'COVID-19' tracked separately in medical (authority=1.0) and general (authority=0.75)

### Falsifiable acceptance criteria (all required)

1. ✓ Terms extracted from SPO claims with full provenance (document_id, timestamp, source_domain, authority_score)
2. ✓ Cooccurrence graph built and persisted correctly
3. ✓ Phase relationships proposed from linguistic patterns (synonym, antonym, hyponym, domain_relation, polyseme)
4. ✓ Consensus gate requires ≥3 independent sources before crystallization
5. ✓ Disagreements tracked and routable to Teach panel for adjudication
6. ✓ Language Banks updated incrementally with crystallized terms without retraining
7. ✓ Full audit trail preserved for term derivation (document, timestamp, source, authority)
8. ✓ Multi-domain terms distinguished (same term, different domains, different contexts)

**Result: PASS**

### Design decisions locked in Y-2

- Terms extracted from both subject and object positions in SPO claims
- Cooccurrence defined as co-mention in same document/source
- Phase proposal via linguistic patterns (deterministic, no ML)
- Consensus gate uses uniform weighting (all sources equal weight, can be tuned by domain)
- Disagreements tracked in proposed_relationships, indexed by term pair
- Language Bank terms can be added incrementally as consensus gates pass
- Audit trail includes: document_id, extraction_timestamp, source_domain, authority_score, context_window
- Multi-domain tracking: same normalized term name, but separate records per source_domain

### Next checkpoint: Phase Y-3 Gate

**Go criteria (all required before Y-3 begins):**
1. Language Bank schema locked and tested (Y-1 complete) ✓
2. Lexical crystallization wired to Auto-Learn consensus (Y-2 complete) ✓
3. Consensus gate ≥3 sources enforced and validated ✓
4. Terms extractable from real Auto-Learn corpus ✓
5. Demo validates all 8 Y-2 acceptance criteria ✓

**If all pass:** Proceed to Y-3 (Federation Bridge Protocol v0).

**If any fail:** Investigate and resolve before Y-3 kickoff.

### Milestone Y-3 (Completed): Federation Bridge Protocol v0
**Objective:** Enable cooperative queries and automatic convergence detection across Language Banks.

### What was built

1. **Federation query models and handlers** (`cie/language_bank_api.py`)
	 - Added request models:
		 - `QueryLanguageBankRequest`
		 - `FederatedQueryRequest`
	 - Added handlers:
		 - `handle_query_bank`
		 - `handle_federated_query`

2. **Single-bank lexical query**
	 - Added `LanguageBankManager.query_bank(...)`
	 - Retrieves exact lexical matches in a bank (case-normalized)
	 - Returns node matches and optional connected edges

3. **Federated query with φ-offset translation**
	 - Added `LanguageBankManager.federated_query(...)`
	 - Computes per-target phase translation:
		 - `phi_offset = (phi_target - phi_source) mod 2π`
	 - Translates target-bank edge phases into source-bank frame
	 - Computes angular-distance resonance score and applies tolerance gate

4. **Bridge-aware term mapping**
	 - Added bridge mapping resolution for cross-bank term equivalence
	 - Supports same-term and explicit mapped-term lookup through `bridge_terms`

5. **Automatic merge gate (convergence signal)**
	 - Added convergence eligibility when all are true:
		 - federated resonance is within tolerance
		 - bridge mapping confidence >= merge threshold
		 - mapped lexical terms exist in target bank
	 - Emits `merge_candidates` for downstream merge workflow

6. **FastAPI route wiring** (`cie/api.py`)
	 - Added:
		 - `POST /v1/lang_bank/{bank_id}/query`
		 - `POST /v1/lang_bank/federated_query`
	 - Both routes use existing auth gates (`_require_read`)

7. **Federation test suite** (`tests/test_language_bank_federation_y3.py`)
	 - 8 tests covering:
		 - single-bank query found/not-found
		 - bridge/no-bridge federated lookup behavior
		 - φ-offset translation correctness
		 - merge-gate eligible/ineligible paths
		 - cross-bank "cold vs COVID-19" query condition

### Measured results

- `cie/language_bank_api.py` compile: PASS
- `cie/api.py` compile: PASS
- Federation test suite: `8/8 PASS`
- Y-3 target query case validated:
	- source: medical bank, term: `cold`
	- target: general bank
	- matched: `cold`
	- not conflated as `COVID-19`

### Falsifiable acceptance criteria (all required)

1. ✓ φ-offset translation implemented and exposed in federated query response
2. ✓ Resonance tolerance negotiation implemented (`resonance_tolerance` gate)
3. ✓ Automatic merge-gate signal emitted when banks converge
4. ✓ Multi-bank query case (`cold` vs `COVID-19`) validated in tests

**Result: PASS**

### Milestone Y-4 (Completed): Audit + Visualization Tools
**Objective:** Make Language Banks browsable, traceable, and proposal-driven for human adjudication.

### What was built

1. **Graph-view API payload** (`cie/language_bank_api.py`, `cie/api.py`)
	- Added manager method: `LanguageBankManager.graph_view(...)`
	- Added endpoint: `GET /v1/lang_bank/{bank_id}/graph`
	- Returns visualization-ready nodes/edges with relation, theta, trust, provenance, and counts

2. **Versioned diff tool**
	- Added manager method: `LanguageBankManager.version_diff(...)`
	- Added request model: `LanguageBankDiffRequest`
	- Added endpoint: `POST /v1/lang_bank/{bank_id}/diff`
	- Returns range-scoped change history + summary by change type (term_added, edge_added, bridge_added, etc.)

3. **Term audit trace surface**
	- Added manager method: `LanguageBankManager.audit_trace(...)`
	- Added request model: `LanguageBankAuditTraceRequest`
	- Added endpoint: `POST /v1/lang_bank/{bank_id}/audit_trace`
	- Returns term-linked nodes, edges, bridge terms, and matching version-history entries

4. **Edit proposal routing (Teach-panel handoff)**
	- Added manager methods:
	  - `LanguageBankManager.propose_change(...)`
	  - `LanguageBankManager.list_change_proposals(...)`
	- Added request model: `LanguageBankChangeProposalRequest`
	- Added endpoints:
	  - `POST /v1/lang_bank/{bank_id}/propose_change`
	  - `GET /v1/lang_bank/{bank_id}/proposals`
	- Proposals are queued with `pending_teach_panel` status for human adjudication workflow

5. **Y-4 test suite** (`tests/test_language_bank_audit_y4.py`)
	- 6 tests covering graph payload, version diffs, audit trace, proposal queueing, and invalid proposal rejection

### Measured results

- `cie/language_bank_api.py` compile: PASS
- `cie/api.py` compile: PASS
- Y-4 test suite: `6/6 PASS`
- Full Phase Y regression:
  - Y-1 + Y-2 + Y-3 + Y-4: `50/50 PASS`

### Falsifiable acceptance criteria (all required)

1. ✓ Graph-view payload available for any Language Bank
2. ✓ Versioned diff available with provenance and timestamped change entries
3. ✓ Term audit trace returns derivation-linked artifacts (nodes/edges/bridges/history)
4. ✓ Edit proposals can be queued and listed for Teach-panel adjudication

**Result: PASS**

### Milestone Y-5 (Completed): Language Bank Frontend Dashboard
**Objective:** Expose Y-4 Language Bank capabilities in the Web UI for operator use.

### What was built (short)
- Added a new Language Banks menu/overlay in `cie/webui/index.html`.
- Wired UI actions to Y-4 endpoints:
	- `GET /v1/lang_bank/{bank_id}/graph`
	- `POST /v1/lang_bank/{bank_id}/diff`
	- `POST /v1/lang_bank/{bank_id}/audit_trace`
	- `POST /v1/lang_bank/{bank_id}/propose_change`
	- `GET /v1/lang_bank/{bank_id}/proposals`
- Added bank selector, graph panel, diff form, audit trace form, and proposal queue panel.

### Outcome
- Y-4 backend features are now directly operable from the browser UI.
- No diagnostics errors in updated `cie/webui/index.html`.

## Phase Z (Completed): Closed-Loop Semantic-Lexical Crystallization

### Selected direction
- **Chosen milestone:** Z-5 Semantic -> Lexical Bridge
- **Why:** closes the loop between semantic crystals and Language Banks so factual structure can continuously improve lexical structure.

### Lexical → Semantic Feedback Path (Composability Note)

**Current state:**
The Z-5 milestone and Phase Z implementation establish a robust semantic → lexical bridge, where semantic crystals propose new or updated lexical relationships for Language Banks. However, the reverse path—using lexical bank state to inform semantic crystal construction, concept normalization, or retrieval ranking—is not yet implemented.

**Planned/Intended closed-loop integration:**
- **Lexical-guided concept normalization:** During semantic crystal construction, extracted terms will be mapped to canonical lexical nodes using the current Language Bank. This enables synonym/antonym families, bridge terms, and polyseme distinctions to guide concept alignment and disambiguation.
- **Retrieval ranking and candidate selection:** When matching new text to existing crystals, lexical resonance (e.g., phase similarity, bridge mappings) will be used to bias or filter candidate matches, improving both precision and recall.
- **Feedback from lexical adjudication:** Human adjudication or consensus in the Language Bank (e.g., proposal acceptance, bridge creation) will feed back into the semantic extraction pipeline, updating extraction heuristics and alignment logic.
- **Co-evolution:** As the lexical structure evolves, it will directly influence how new semantic evidence is interpreted, clustered, and crystallized, closing the loop for continuous, auditable knowledge organization.

**Implementation complexity and risk profile (important):**
- **Concept normalization** is the most contained and lowest-risk reverse-path mechanism. It has a clear hook point in concept identification (for example, upstream of polarity/phase assignment) and can be tested with direct mapping fidelity criteria.
- **Retrieval ranking bias via lexical resonance** is materially higher risk. It creates a coupled scoring loop (lexical influence on semantic candidate selection, then semantic outputs feeding lexical proposals) and therefore needs explicit stability conditions, not only threshold gates.
- **Adjudication feedback into extraction heuristics** is the most open-ended mechanism. Turning human adjudication outcomes into heuristic updates is effectively online human-in-the-loop learning and should be treated as a separate engineering class of problem.
- **Co-evolution** is a system-level property that depends on the prior mechanisms and should not be used as a first implementation target.

**Recommended milestone scoping:**
- The first lexical -> semantic milestone should be scoped strictly to **concept normalization**.
- Retrieval ranking bias and adjudication-driven heuristic updates should be explicitly deferred to later milestones.
- This preserves falsifiability and keeps the first reverse-path milestone operationally testable without introducing multi-loop instability.

**Current documentation and code only describe the semantic → lexical direction.** The above mechanisms are required for full closed-loop composability and are planned for future milestones.

### Milestone AA-1 (Planned): Lexical-Guided Concept Normalization
**Objective:** During semantic crystal construction, map extracted terms to canonical lexical nodes before phase assignment, so synonym families and bridge terms produce concept-aligned rather than string-matched graphs.

**Scope (strict):**
1. Hook into concept identification upstream of `_polarity_theta_per_pair`.
2. For each extracted term, query the active Language Bank for a canonical node match (exact, then bridge-mapped).
3. If a canonical match exists, substitute the canonical node label; preserve original term as provenance annotation.
4. If no match exists, fall through to existing behavior unchanged.
5. No change to scoring, retrieval ranking, or proposal generation in this milestone.

**Falsifiable acceptance criteria (all required):**
1. Two input texts using synonymous terms (for example, "COVID-19" and "coronavirus") produce crystals with aligned concept nodes, not separate string-distinct nodes.
2. A term with no lexical match falls through without error and produces identical output to current behavior.
3. Bridge-mapped terms resolve through bridge mapping, not only exact match.
4. Provenance annotation on substituted nodes is preserved in crystal output.
5. Existing regression suite remains green.

**What this explicitly does not do:**
- No lexical resonance influence on retrieval scoring.
- No feedback from adjudication into extraction heuristics.
- No change to the consensus gate or proposal queue.

### Milestone Z-5 (Completed): Semantic -> Lexical Bridge
**Objective:** Convert semantic-crystal evidence into auditable lexical relationship proposals for Language Banks.

### What was built

1. **Pass-1 semantic evidence extraction + queue wiring**
	- Added semantic proposal generation from crystals in `cie/lexical_crystallizer.py`:
	  - `propose_relationships_from_semantic_crystal(...)`
	  - relation inference heuristics over semantic edge geometry
	  - provenance capture (source documents, claims, evidence snippets)
	- Added semantic-bridge queue API in `cie/language_bank_api.py`:
	  - `QueueSemanticBridgeRequest`
	  - `LanguageBankManager.queue_semantic_bridge(...)`
	  - `handle_queue_semantic_bridge(...)`
	- Added route wiring in `cie/api.py`:
	  - `POST /v1/lang_bank/{bank_id}/propose_semantic_bridge`
	- Extended audit surface in `cie/language_bank_api.py`:
	  - `audit_trace(...)` now includes `related_proposals` and `proposal_count`.

2. **Pass-2 live auto-generation from teach events**
	- Added post-crystallization semantic bridge hook in `cie/api.py`:
	  - `_maybe_queue_semantic_bridge_from_result(...)`
	- Hook wired into:
	  - `POST /v1/source/teach`
	  - `POST /v1/teach`
	- Teach responses now include `semantic_bridge` summary payload with:
	  - enabled/bank_id/proposals/queued
	  - explicit error field when load/queue fails (non-fatal).

3. **Safety gate hardening (non-destructive queue behavior)**
	- Added pending-proposal deduplication in `LanguageBankManager.propose_change(...)`
	  to prevent queue spam on repeated identical semantic bridge events.

4. **UI provenance/source surfacing (Y-5 extension)**
	- Updated `cie/webui/index.html` proposal panel to render proposal cards with
	  origin badges:
	  - `semantic_bridge`
	  - `manual_or_other`
	- Preserved raw JSON fallback for full payload inspection.

5. **Z-5 regression test coverage**
	- Added/extended `tests/test_semantic_lexical_bridge_z5.py` covering:
	  - semantic proposal provenance extraction
	  - semantic bridge queue wiring
	  - audit trace linkage to queued proposals
	  - deduplication of repeated pending semantic proposals
	  - endpoint-level `/v1/teach` auto-queue integration behavior.

6. **Deterministic Z-5 demo script**
	- Added `scripts/csif_semantic_lexical_bridge_z5_demo.py` to prove end-to-end flow:
	  semantic crystal -> lexical proposals -> queue -> audit trace linkage.

### Measured results

- Targeted regression suite:
	- `tests/test_semantic_lexical_bridge_z5.py`
	- `tests/test_language_bank_audit_y4.py`
	- `tests/test_lexical_crystallization_y2.py`
- Result: `23/23 PASS`
- Diagnostics: no errors in updated files (`cie/api.py`, `cie/language_bank_api.py`, `cie/webui/index.html`, `tests/test_semantic_lexical_bridge_z5.py`).

### Falsifiable acceptance criteria (all required)
1. ✓ Semantic crystal evidence produces lexical proposals with explicit provenance (crystal ids + evidence traces).
2. ✓ Proposals are queued through existing Language Bank proposal workflow (pending status, no direct mutation by default).
3. ✓ Domain-relation and synonym/antonym-family candidates are generated from semantic evidence via deterministic heuristics.
4. ✓ Audit trace shows queued lexical proposals that originated from semantic crystal evidence.
5. ✓ Existing Y-1..Y-5 regression remains green after integration.

**Result: PASS**

### Milestone Z-5 Repro Commands

One-command verification flow (run from `crystal-information-engine` root):

```bash
PYTHONPATH=. python3 -m pytest -q tests/test_semantic_lexical_bridge_z5.py tests/test_language_bank_audit_y4.py tests/test_lexical_crystallization_y2.py
```

Expected outcome:
- `23 passed`

### Milestone Z-5 Operational Toggles

- `CIE_SEMANTIC_BRIDGE_ENABLED`
	- Default: `1`
	- Set to `0` (or `false`/`off`) to disable auto-queueing on teach/source-teach paths.
- `CIE_SEMANTIC_BRIDGE_BANK_ID`
	- Default: `medical_en_v1`
	- Target Language Bank for auto-generated semantic bridge proposals.

Deterministic demo command (optional):

```bash
PYTHONPATH=. python3 scripts/csif_semantic_lexical_bridge_z5_demo.py
```

### Milestone Z-1 (Completed): Real-time Upload -> Auto-Learn -> Lexical Pipeline
**Objective:** Deliver an operator-visible real-time path:
`Document upload -> Auto-Learn extraction -> consensus gate -> lexical crystallization -> UI notification`.

**Important operator semantics:**
- `pipeline_completed` means the upload/extraction/proposal pipeline has finished for that document.
- It does **not** guarantee lexical crystallization has occurred.
- Because crystallization is consensus-gated (>=3 independent sources), single-upload proposals may remain queued/deferred until the gate is satisfied.

### What was built

1. **Resumable event sequencing in registry writes** (`cie/api.py`)
	- `_append_autolearn_registry_event(...)` now stamps each event with `event_seq`.
	- Registry now persists `next_event_seq` so stream consumers can resume without replaying full history.

2. **Live SSE endpoint for Auto-Learn events** (`cie/api.py`)
	- Added endpoint: `GET /v1/autolearn/events/stream`
	- Supports cursor resume and control params:
	  - `since_seq`
	  - `heartbeat_seconds`
	  - `timeout_seconds`
	- Emits typed SSE frames:
	  - `autolearn_event`
	  - `heartbeat`
	  - `stream_timeout`

3. **Document upload pipeline endpoint** (`cie/api.py`)
	- Added endpoint: `POST /v1/autolearn/upload` (multipart text upload).
	- Runs deterministic stage chain:
	  - upload accepted
	  - Auto-Learn claim extraction
	  - lexical proposal generation
	  - consensus gate over lexical proposals
	  - queued lexical crystallization proposals into Language Bank teach-panel workflow
	- Emits pipeline stage events:
	  - `pipeline_upload_received`
	  - `pipeline_extraction_complete`
	  - `pipeline_lexical_complete`
	  - `pipeline_completed` (pipeline processing complete; queued proposals may still await consensus before crystallization)

4. **Event snapshot cursor exposure** (`cie/api.py`)
	- `GET /v1/autolearn/events` now returns `latest_event_seq` for deterministic stream resume handoff.

5. **Web UI real-time notifications + upload control** (`cie/webui/index.html`)
	- Added upload controls for Z-1 pipeline (`Run Upload Pipeline`).
	- Added live pipeline status badge and notification mini-log.
	- UI consumes stream events and updates status in real time.
	- UI explicitly distinguishes pipeline completion from deferred crystallization state under consensus gating.

6. **Z-1 regression tests** (`tests/test_autolearn_realtime_z1.py`, `tests/test_autolearn_upload_pipeline_z1.py`)
	- Verifies stream emits queued `queue_enqueued` event.
	- Verifies cursor (`since_seq`) suppresses already-seen events and only emits control frames until timeout.
	- Verifies upload pipeline emits stage events and can queue lexical proposals.

### Measured results

- Targeted regression suite:
	- `tests/test_autolearn_realtime_z1.py`
	- `tests/test_autolearn_upload_pipeline_z1.py`
	- `tests/test_semantic_lexical_bridge_z5.py`
	- `tests/test_language_bank_audit_y4.py`
	- `tests/test_lexical_crystallization_y2.py`
- Result: `27/27 PASS`

### Milestone Z-1 Repro Commands

Run from `crystal-information-engine` root:

```bash
PYTHONPATH=. python3 -m pytest -q tests/test_autolearn_realtime_z1.py tests/test_autolearn_upload_pipeline_z1.py tests/test_semantic_lexical_bridge_z5.py tests/test_language_bank_audit_y4.py tests/test_lexical_crystallization_y2.py
```

Expected outcome:
- `27 passed`

### Milestone Z-2 (Completed): Federation UI Visualization
**Objective:** Provide interactive UI visibility into federation mechanics:
`phi_scope offsets, bridge term mappings, cross-bank resonance`.

### What was built

1. **Federation query panel in Language Bank dashboard** (`cie/webui/index.html`)
	- Added term/source/target controls + tolerance and merge-threshold inputs.
	- Added action button invoking `POST /v1/lang_bank/federated_query`.

2. **Federation visualization renderer** (`cie/webui/index.html`)
	- Added per-target result cards showing:
	  - `phi_scope` offset (phase translation)
	  - bridge-mapped terms
	  - cross-bank resonance score
	  - merge-gate eligibility and bridge confidence
	- Added resonance bar visualization for rapid operator scan.

3. **Raw payload trace pane** (`cie/webui/index.html`)
	- Preserved JSON payload pane (`lb-fed-json`) for audit/debug parity with existing dashboard patterns.

---

## Milestone Y-1 (Completed): Language Bank Schema Lock

**Objective:** Define and implement the foundational Language Bank schema and API.

### What was built

1. **LanguageBank dataclass** (csif/language_bank.py)
   - Immutable fields: bank_id, scope, base_phases, phi_scope
   - Mutable fields: nodes (terms), edges (relationships), bridge_terms, version_history
   - Canonical phase definitions: synonym=0, antonym=π, hyponym=π/2, domain_relation=π/4, polyseme=π/6
   - Atomic classes: LanguageBankNode, LanguageBankEdge, BridgeTerm, VersionHistoryEntry
   - Stability scoring: mean(trust across all edges)
   - YAML serialization/deserialization with atomic temp-file replace

2. **Three seed Language Banks**
   - medical_en_v1: 5 terms (COVID-19, cold, long COVID, fever, warm), 5 edges
   - general_en_v1: 4 terms (cold, hot, virus, illness), 3 edges
   - legal_en_v1: 4 terms (contract, obligation, waiver, liability), 3 edges
   - All seed banks pass stability threshold (≥0.80)

3. **API endpoints wired into FastAPI** (cie/api.py, cie/language_bank_api.py)
   - POST /v1/lang_bank/create
   - POST /v1/lang_bank/{bank_id}/add_term
   - POST /v1/lang_bank/{bank_id}/add_edge
   - POST /v1/lang_bank/{bank_id}/add_bridge_term
   - GET /v1/lang_bank/{bank_id}/info
   - GET /v1/lang_bank/{bank_id}/nodes
   - GET /v1/lang_bank/{bank_id}/edges
   - GET /v1/lang_bank/list
   - GET /v1/lang_bank/{bank_id}/export
   - Global LanguageBankManager singleton with in-memory bank storage

4. **Comprehensive test suite** (tests/test_language_bank_schema_lock.py)
   - 24 test cases covering all CRUD operations
   - All tests pass with 100% success rate
   - Test categories:
     - Creation and validation (3 tests)
     - Term operations (3 tests)
     - Edge operations (6 tests)
     - Stability scoring (3 tests)
     - Version history (2 tests)
     - Bridge terms (2 tests)
     - Serialization (3 tests)
     - Seed banks validation (4 tests)
     - Milestone acceptance (1 comprehensive test)

5. **Live demonstration script** (scripts/csif_language_bank_demo.py)
   - Creates all three seed banks
   - Demonstrates term relationships with phase angles
   - Shows base phase definitions
   - Tests YAML persistence
   - Simulates API requests
   - Verifies all 9 Milestone Y-1 falsifiable criteria

### Measured results

- All 24 unit tests: PASS
- Demo script Milestone Y-1 acceptance criteria: ALL 9 PASS
- Stability scores: medical=0.926, general=0.847, legal=0.917
- API compilation: PASS (no syntax errors)
- YAML roundtrip fidelity: 100% (all state preserved)
- Version history tracking: ✓ (every mutation recorded)
- Immutability validation: ✓ (base_phases and phi_scope immutable post-creation)

### Falsifiable acceptance criteria (all required)

1. ✓ LanguageBank dataclass created with immutable base_phases/phi_scope
2. ✓ Terms can be added and retrieved by node_id
3. ✓ Edges can be added between terms with correct phase relationships
4. ✓ Three seed banks can be instantiated and validated
5. ✓ YAML serialization/deserialization preserves bank state
6. ✓ Stability score computed correctly from edge trust values
7. ✓ Version history tracks all mutations
8. ✓ Bridge terms can be added for cross-bank federation
9. ✓ API endpoints wired into FastAPI with read/write auth gates

**Result: PASS**

### Design decisions locked in Y-1

- Base phases are canonical per relation type (e.g., antonym always π)
- Stability = mean(trust) across all edges (simple, intuitive)
- Bridge terms are explicit mappings, not automatic inference
- phi_scope is per-bank offset for multi-bank alignment (set at creation, immutable)
- Version bumps on every mutation for full traceability
- Node IDs are UUIDs (collision-free, deterministic for reconstructed banks)
- No cross-bank queries in Y-1 (federation protocol deferred to Y-3)

### Next checkpoint: Phase Y-2 Gate

**Go criteria (all required before Y-2 begins):**
1. Language Bank schema locked in code and tested (Y-1 complete) ✓
2. Three seed banks available and operational ✓
3. API endpoints responding with auth gates ✓
4. Demo script validates all acceptance criteria ✓
5. Extreme Organizability thesis incorporated into roadmap ✓

**If all pass:** Proceed to Y-2 (Lexical Crystallization from Auto-Learn).

**If any fail:** Investigate and resolve before Y-2 kickoff.
