# CSIF Temporal Phase Evolution: Knowledge That Learns

## Overview

Static phase assignments work well for immutable logical relationships. But most real knowledge evolves: legal standards shift, medical consensus changes, empirical evidence accumulates or contradicts earlier beliefs. A temporally-evolving phase model captures this without abandoning auditability or the core geometric contradiction-detection mechanism.

## Core Extension

### Static Edge (Baseline)

A crystallized edge in standard CSIF holds a single phase value:

$$\theta_{ij} \in [-\pi, \pi]$$

### Temporal Edge

A temporally-evolving edge becomes:

$$\theta_{ij}(t) = \theta_0 + \delta(t) + \sigma \cdot \eta(t)$$

Where:

- **$\theta_0$**: The base phase value from initial LLM encoding (fixed once crystallized)
- **$\delta(t)$**: A deterministic drift term—scheduled phase updates from new evidence or consensus shifts
- **$\sigma$**: A confidence-weighted uncertainty band (width reflects evidence density)
- **$\eta(t)$**: A stochastic fluctuation term, bounded by evidence weight, representing minor transient variations

### Resonance Under Temporal Evolution

When edges evolve over time, resonance becomes an expectation over the time horizon:

$$R_N(A,B,t) = \mathbb{E}_t\left[\frac{\sum_{e \in E} d(\theta_e^{(A)}(t), \theta_e^{(B)}(t))}{|E|\pi}\right]$$

Where $d(\cdot, \cdot)$ is the circular distance between two phase values, and the expectation is taken over the stochastic variations and any scheduled drifts active at time $t$.

## Confidence Interpretation

The uncertainty band $\sigma$ encodes how certain the system is about a relationship:

| $\sigma$ Range | Interpretation | Example |
|---|---|---|
| ~0 | Fully crystallized, high confidence | Light illuminates Darkness (well-tested, broad consensus) |
| Small | Well-supported, minor variance | Medical treatment efficacy (strong evidence, stable protocol) |
| Medium | Contested, needs more evidence | Emerging technology adoption rate (multiple perspectives, ongoing) |
| Large | Speculative, pre-consensus | Novel hypothesis (few LLM encodings agree, sparse empirical data) |
| ~π | Contradictory encodings present | Conflicting expert opinions not yet resolved geometrically |

This creates a **continuous confidence spectrum** rather than a binary crystallized/not-crystallized distinction. The same edge can hold a phase value and also hold uncertainty about that value—both are part of the auditable record.

## Lightweight Online Learning

Temporal phase evolution unlocks a new capability: **gradient-like updates at the crystal level without retraining the LLM**.

### Update Mechanism

1. An outcome mismatch is observed (e.g., a query result contradicts expected behavior).
2. The mismatch is traced to a specific edge and its current phase value $\theta_e(t)$.
3. An error signal $\epsilon$ is computed (e.g., the circular distance between observed and expected phase).
4. The edge's phase trajectory is nudged:
   $$\delta(t+\Delta t) \leftarrow \delta(t) + \alpha \cdot \epsilon \cdot w(E)$$
   where $\alpha$ is a step size and $w(E)$ is an evidence-strength weighting factor.
5. Over multiple feedback cycles, the phase converges toward empirically-validated positions.
6. The converged phase becomes the new $\theta_0$ candidate for the next LLM retraining cycle.

This is **not backpropagation through the LLM**. It is local geometric correction—low-cost, auditable, and highly specific. Each correction carries full provenance: which outcome triggered it, which evidence was weighted, which edge changed and by how much.

## Honest Cautions

### Stochastic Bounding

The fluctuation term $\eta(t)$ must be carefully constrained. If $\eta(t)$ is unbounded, phase values can wander arbitrarily, destroying the contradiction detection mechanism. The π-residual signal becomes unreliable.

**Constraint**: The fluctuation must be bounded by evidence weight. Edges with sparse evidence (high $\sigma$) should experience proportionally larger fluctuations; edges with strong evidence (low $\sigma$) should be nearly stable.

### Adaptive Contradiction Threshold

In static CSIF, contradiction is detected near $\pi$ residual with a fixed threshold (e.g., residual > $\pi/2$).

In temporal CSIF, the contradiction threshold should adapt with $\sigma$:

$$\text{Contradiction threshold} = \frac{\pi}{2} + c \cdot \sigma$$

where $c$ is a proportionality constant. Relationships with high uncertainty are given more "phase wiggle room" before being flagged as contradictory, because their uncertainty already signals possible conflict.

### Version-Stamped Snapshots

Temporal evolution means crystal identity becomes **time-dependent**. Two queries at $t_1$ and $t_2$ against the same crystal pair may produce different resonance scores.

**This is correct behavior**, but it requires reproducibility discipline:

- Every query result must be tagged with the timestamp $t$ at which it was computed.
- The full phase trajectory $(\theta_0, \delta(t), \sigma, \eta(t))$ must be logged alongside the query.
- For full audit trail reconstruction, crystal snapshots must be version-stamped: CrystalBank-v[timestamp] contains a frozen view of all phase states at that moment.

Without version stamping, the audit trail becomes ambiguous: "Which phase values were used for this decision?" becomes impossible to answer reliably.

## Relationship to LLM Calibration

This temporal model directly supports the LLM calibration feedback loop described in [CIE_LLM_CALIBRATION_SURFACE.md](CIE_LLM_CALIBRATION_SURFACE.md):

1. LLM produces frozen phase encoding → crystallized $\theta_0$ with initial $\sigma$.
2. CSIF computes outcomes geometrically.
3. Outcome observation produces error signals.
4. Temporal nudging converts diffuse errors into phase corrections ($\delta(t)$ updates).
5. After evidence accumulates, the corrected phase becomes the target for targeted LLM retraining.

The temporal layer makes the LLM→CSIF→outcome→retraining cycle tighter and more specific. Instead of "the model was wrong about semantic proximity," the signal becomes "Edge (X, Y) should have phase 0.2, not 0.4; confidence band is now ±0.08."

## Implementation Checklist

- [ ] Phase trajectory representation: store $(\theta_0, \delta_history, \sigma, \eta_bounds)$ in crystal edge data structures
- [ ] Deterministic drift scheduling: specify syntax for $\delta(t)$ (e.g., piecewise linear, discrete step updates)
- [ ] Stochastic bounding: implement evidence-weight-dependent $\eta(t)$ bounds
- [ ] Adaptive contradiction detection: compute threshold as $\pi/2 + c \cdot \sigma$ per edge
- [ ] Version-stamped snapshots: add `[timestamp]` metadata to crystal bank snapshots
- [ ] Query result tagging: attach $t$ and full phase trajectory to every query outcome
- [ ] Temporal resonance computation: implement expectation over $\eta(t)$ and scheduled $\delta(t)$
- [ ] Audit trail extension: log all phase corrections with provenance, evidence weight, outcome trigger

## Selective Stochasticity via Time: Deterministic and Probabilistic Control

Absolute determinism is usually preferred for most operations. However, when a random or probabilistic response is required, the time dimension provides a principled mechanism for controlled stochasticity:

- By tying the stochastic term $\eta(t)$ to a specific timestamp or event seed, any "random" outcome becomes reproducible by replaying the same time/seed.
- This enables full auditability and traceability for every probabilistic decision.
- The system can switch between strict determinism (fixed $t$ or $\eta$) and controlled stochasticity (varying $t$ or $\eta$) as needed.

**Result:** You get the best of both worlds—LLM-like generativity and full auditability—within the same geometric/temporal framework. This approach allows for:

- Reproducible sampling: Every probabilistic response can be regenerated exactly by specifying the same time/seed.
- Auditable randomness: All stochastic outcomes are logged and can be traced to their origin.
- Selective operability: The system can be run in deterministic mode for validation, or in stochastic mode for creative or exploratory tasks, simply by controlling the time/seed input.

## Philosophical Note

The quantum-like framing is honest in a specific sense: CSIF is not becoming quantum computing. Rather, the mathematical structure—superposition of phase states, probability amplitudes (via $\sigma$), interference patterns (via temporal resonance)—maps naturally onto what knowledge systems need to model: uncertainty, evidence accumulation, and consensus formation. The formalism is already there in the geometry; this extension makes it explicit and tractable.
