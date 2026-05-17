# RWIF Crystal Schema V1

**Document type:** Format Specification  
**Author:** Mogir Jason Rofick (Mo)  
**Date:** May 17, 2026  
**Status:** Draft v1.0  
**Semantic version:** `crystal-1.0.0`  
**Audience:** AI Systems, Engineers, Implementers

---

## Purpose

This document defines the crystal-native storage schema for RWIF (Real-World Intelligence
Format) as used by the Crystal Information Engine (CSIF).

This schema is distinct from RWIF4 and RWIF5, which store transformer model activation
lattices (spherical harmonic coefficient payloads extracted from LLM layers). Those formats
are a research thread concerned with *how an LLM represents concepts internally*.

This schema is concerned with *what is known* - storing semantic relationships as
phase-geometric crystal structures that CSIF can instantiate, query, and evolve.

The two formats are related in spirit and may eventually be bridged (see Part 6), but
they are not interchangeable. Readers must check the magic prefix before parsing.

---

## Part 1: Conceptual Model

### 1.1 What a Crystal Is

A crystal is a directed semantic graph. Its nodes are concepts. Its edges are typed
relationships between concepts. Every edge carries a phase angle that encodes the
geometric alignment of that relationship.

A collection of crystals sharing a common concept space forms a crystal bank. The bank
is the runtime knowledge store that CSIF operates on.

### 1.2 The Four Dimensions

Every edge in a crystal exists as a trajectory through four-dimensional space:

| Dimension | Name | Range | Meaning |
|---|---|---|---|
| 1 | Phase angle | `[-pi, pi]` | Semantic alignment direction |
| 2 | Lobe | discrete string | Language or domain context |
| 3 | Time | ISO 8601 timestamps | Deterministic temporal evolution |
| 4 | Confidence band | `[0, pi]` (sigma) | Certainty width |

**Phase angle semantics:**
- `0` - perfect coherence, concepts reinforce each other
- `pi/2` - orthogonal, concepts are independent
- `pi` - direct opposition, contradiction

**Lobe semantics:**  
The same relationship can exist in multiple lobes (English, Spanish, Medical, Legal,
Robotics, etc.) with independent phase values. Cross-lobe resonance is computed
geometrically. If two lobes encode the same relationship at the same phase angle,
they are semantically aligned across domains.

**Time semantics:**  
Phase values evolve deterministically along the time axis. The full trajectory is
preserved as an append-only history. Any historical state of a crystal is
reconstructable from its trajectory record.

**Confidence band semantics:**  
Sigma controls the width of the uncertainty envelope around the base phase. A wide
sigma indicates a speculative or contested relationship. A narrow sigma indicates
a well-attested, stable relationship. The contradiction detection threshold adapts
with sigma: `threshold = pi/2 + c * sigma`.

---

## Part 2: File Format

### 2.1 Magic Bytes and Versioning

RWIF crystal files use the following magic prefixes:

| Container | Magic | Meaning |
|---|---|---|
| Single crystal | `RWIFC1` (6 bytes + 2 padding) | One crystal |
| Crystal bank | `RWIFB1` (6 bytes + 2 padding) | Many crystals |

Wire prefix structure (identical for both):

```text
<8sII
```

| Offset | Size | Type | Field |
|---|---:|---|---|
| `0x00` | 8 | `char[8]` | magic bytes |
| `0x08` | 4 | `uint32` | wire version = `1` |
| `0x0C` | 4 | `uint32` | JSON header length in bytes |

After the fixed prefix: UTF-8 JSON header, then binary payload sections.

### 2.2 Semantic Versioning Rule

Following the same policy as RWIF4/5:

1. Header-only additions that preserve binary framing -> minor version increment
2. Clarifications and validator-only changes -> patch version increment
3. Any change to binary prefix layout, section ordering, or index width -> **major version increment**

---

## Part 3: JSON Header Schema

### 3.1 Required Fields (All Crystal Containers)

| Field | Type | Meaning |
|---|---|---|
| `schema` | `string` | Always `rwif_crystal` |
| `schema_version` | `string` | Semantic version, currently `crystal-1.0.0` |
| `checksum_algorithm` | `string` | Currently `sha256` |
| `header_checksum` | `string` | SHA-256 of canonical header (checksum fields omitted) |
| `layout_checksum` | `string` | SHA-256 of all payload blocks in layout order |
| `created` | `string` | ISO 8601 creation timestamp |
| `crystal_count` | `uint32` | Number of crystals in this file (1 for RWIFC1) |

### 3.2 Required Fields (Single Crystal, RWIFC1)

| Field | Type | Meaning |
|---|---|---|
| `crystal_id` | `string` | UUID v4, stable unique identifier |
| `crystal_label` | `string` | Human-readable name |
| `domain` | `string` | Primary domain (e.g., `medical`, `legal`, `general`) |
| `lobe` | `string` | Primary lobe identifier |
| `node_count` | `uint32` | Number of concept nodes |
| `edge_count` | `uint32` | Number of typed relationship edges |
| `stability_score` | `float` | Mean edge trust across all edges, `[0, 1]` |
| `frozen` | `bool` | If true, base phases are immutable; only trajectory appends are allowed |

### 3.3 Optional Fields

| Field | Type | Meaning |
|---|---|---|
| `source_model_id` | `string` | LLM that performed the initial phase encoding |
| `source_corpus` | `string` | Source document set identifier |
| `encoding_run_id` | `string` | Unique identifier for the LLM encoding run |
| `tags` | `array[string]` | Freeform classification tags |
| `related_crystals` | `array[string]` | UUIDs of semantically related crystals |
| `anti_crystal_id` | `string` | UUID of the anti-phase counterpart crystal, if it exists |

---

## Part 4: Payload Structure

### 4.1 Node Block

Each node represents a concept. Nodes are the vertices of the semantic graph.

JSON array, one entry per node:

```json
{
  "node_id": "uuid-v4",
  "label": "canonical concept label",
  "aliases": ["synonym1", "synonym2"],
  "lobe": "English",
  "provenance": {
    "source_document": "document identifier or URL",
    "extraction_timestamp": "ISO 8601",
    "extractor": "co_occurrence_v1 | llm_encoder | manual"
  }
}
```

| Field | Required | Meaning |
|---|---|---|
| `node_id` | yes | UUID v4, stable |
| `label` | yes | Canonical string label for this concept |
| `aliases` | no | Synonym labels (used for cross-lobe normalization) |
| `lobe` | yes | Lobe this node belongs to |
| `provenance` | yes | How this node was identified |

### 4.2 Edge Block

Each edge represents a typed semantic relationship between two nodes. This is the
primary carrier of phase-geometric information.

JSON array, one entry per edge:

```json
{
  "edge_id": "uuid-v4",
  "source_node": "node-uuid",
  "relation": "is_a | has_property | implies | causes | supports | dispels | custom",
  "target_node": "node-uuid",
  "lobe": "English",
  "reinforcing": true,

  "base_phase": 0.0,
  "confidence_band": 0.1,

  "phase_trajectory": [
    {
      "timestamp": "ISO 8601",
      "phase": 0.02,
      "confidence_band": 0.12,
      "drift_delta": 0.0,
      "event_type": "initial_encoding",
      "source": {
        "type": "llm_encoding",
        "model_id": "model-identifier",
        "run_id": "encoding-run-uuid",
        "input_text_hash": "sha256-of-source-text",
        "timestamp": "ISO 8601"
      }
    },
    {
      "timestamp": "ISO 8601",
      "phase": 0.01,
      "confidence_band": 0.08,
      "drift_delta": -0.01,
      "event_type": "outcome_nudge",
      "source": {
        "type": "outcome_observation",
        "outcome": "validated",
        "error_signal": -0.01,
        "evidence_weight": 0.8,
        "nudge_alpha": 0.1,
        "timestamp": "ISO 8601"
      }
    },
    {
      "timestamp": "ISO 8601",
      "phase": 0.00,
      "confidence_band": 0.04,
      "drift_delta": -0.01,
      "event_type": "crystallization",
      "source": {
        "type": "consensus_gate",
        "source_count": 3,
        "sources": ["doc-id-1", "doc-id-2", "doc-id-3"],
        "timestamp": "ISO 8601"
      }
    }
  ],

  "provenance": {
    "encoding_model": "model-identifier",
    "encoding_run": "run-uuid",
    "source_documents": ["doc-id-1", "doc-id-2"],
    "feedback_events": 2,
    "last_updated": "ISO 8601"
  }
}
```

#### Edge Field Reference

| Field | Required | Meaning |
|---|---|---|
| `edge_id` | yes | UUID v4, stable |
| `source_node` | yes | UUID of source concept node |
| `relation` | yes | Typed relation label |
| `target_node` | yes | UUID of target concept node |
| `lobe` | yes | Lobe this edge belongs to |
| `reinforcing` | yes | `true` if coherent, `false` if anti-phase (negation) |
| `base_phase` | yes | Initial crystallized phase `theta_0` in `[-pi, pi]` |
| `confidence_band` | yes | Current sigma value `[0, pi]` |
| `phase_trajectory` | yes | Append-only history of all phase events |

#### Phase Trajectory Entry Fields

| Field | Required | Meaning |
|---|---|---|
| `timestamp` | yes | ISO 8601 timestamp of this event |
| `phase` | yes | Phase value `theta(t)` at this event |
| `confidence_band` | yes | Sigma value at this event |
| `drift_delta` | yes | Change in phase from prior event (`0.0` for initial) |
| `event_type` | yes | One of: `initial_encoding`, `outcome_nudge`, `adjudication`, `consensus_gate`, `retraining`, `crystallization` |
| `source` | yes | Provenance object (structure varies by event_type, see below) |

#### Source Object by Event Type

**`initial_encoding`:**
```json
{
  "type": "llm_encoding",
  "model_id": "string",
  "run_id": "uuid",
  "input_text_hash": "sha256",
  "timestamp": "ISO 8601"
}
```

**`outcome_nudge`:**
```json
{
  "type": "outcome_observation",
  "outcome": "validated | invalidated",
  "error_signal": 0.0,
  "evidence_weight": 0.0,
  "nudge_alpha": 0.0,
  "timestamp": "ISO 8601"
}
```

Nudge rule: `delta = alpha * error_signal * evidence_weight`  
New phase: `wrap_pi(theta + delta)`  
New sigma: `sigma * (1 - evidence_weight * 0.1)` (tightens with evidence)

**`adjudication`:**
```json
{
  "type": "human_adjudication",
  "adjudicator_id": "string",
  "decision": "confirmed | corrected | rejected",
  "corrected_phase": 0.0,
  "notes": "string",
  "timestamp": "ISO 8601"
}
```

**`consensus_gate`:**
```json
{
  "type": "consensus_gate",
  "source_count": 3,
  "sources": ["doc-id-1", "doc-id-2", "doc-id-3"],
  "timestamp": "ISO 8601"
}
```

**`retraining`:**
```json
{
  "type": "llm_retraining",
  "prior_model_id": "string",
  "new_model_id": "string",
  "retraining_target": "edge-uuid",
  "prior_phase": 0.0,
  "new_phase": 0.0,
  "timestamp": "ISO 8601"
}
```

**`crystallization`:**
```json
{
  "type": "crystallization",
  "frozen": true,
  "final_phase": 0.0,
  "final_sigma": 0.0,
  "timestamp": "ISO 8601"
}
```

### 4.3 Version History Block

Append-only log of every structural mutation to the crystal (node additions, edge
additions, freezes, schema migrations). Separate from the per-edge phase trajectory.

```json
[
  {
    "version": 1,
    "timestamp": "ISO 8601",
    "change_type": "node_added | edge_added | crystal_frozen | schema_migrated",
    "change_summary": "human-readable description",
    "actor": "llm_encoder | human | consensus_gate | retraining"
  }
]
```

---

## Part 5: Crystal Bank Format (RWIFB1)

A crystal bank file stores multiple crystals with a shared index for O(1) lookup.

### 5.1 Additional Required Header Fields

| Field | Type | Meaning |
|---|---|---|
| `bank_id` | `string` | UUID v4, stable bank identifier |
| `bank_label` | `string` | Human-readable bank name |
| `lobe` | `string` | Primary lobe for this bank |
| `crystal_count` | `uint32` | Number of crystals in bank |
| `index_nbytes` | `uint32` | Byte length of the crystal index block |

### 5.2 Crystal Index Block

Immediately after the JSON header. Fixed-width entries for O(1) crystal lookup.

```text
struct CrystalEntry {
    char[36]  crystal_id;    // UUID v4 as ASCII string, no null terminator
    uint64    offset;        // byte offset of crystal blob from payload start
    uint64    length;        // byte length of crystal blob
    float32   stability;     // pre-computed stability score
    uint8     frozen;        // 1 if crystal is frozen, 0 otherwise
    uint8[3]  reserved;      // padding to 64-byte alignment
}
```

64 bytes per entry.

### 5.3 Crystal Blob Payload

Concatenated RWIFC1 blobs, each independently parseable. A reader can seek to any
crystal using the index without loading the full bank.

### 5.4 Bank-Level Checksums

| Checksum field | Covers |
|---|---|
| `index_checksum` | the crystal index binary block |
| `payload_checksum` | the concatenated RWIFC1 crystal blobs |
| `layout_checksum` | canonical JSON header basis + index + payload |
| `header_checksum` | canonical JSON header with checksum fields omitted |

---

## Part 6: Temporal Phase Query Protocol

### 6.1 Querying Phase at Time T

To retrieve the phase of an edge at a specific time T:

1. Load the edge's `phase_trajectory` array
2. Filter to entries where `timestamp <= T`
3. Return the entry with the latest timestamp
4. If no entries exist before T, return `base_phase`

This makes every historical state of a crystal fully reconstructable.

### 6.2 Current Phase

Current phase is always the last entry in `phase_trajectory`. Current sigma is the
`confidence_band` of the last entry.

### 6.3 Phase Evolution Formula

```text
theta(t) = theta_0 + delta(t) + sigma(t) * eta(bounded)

Where:
  theta_0         = base_phase (initial crystallized value)
  delta(t)        = sum of all drift_delta values up to time t
  sigma(t)        = confidence_band at time t
  eta(bounded)    = stochastic term, |eta| <= 1, scaled by sigma
                    (used only for temporal resonance sampling, not stored)
```

### 6.4 Adaptive Contradiction Threshold

```text
threshold(t) = pi/2 + c * sigma(t)

Where c is a stability constant, recommended default: c = 0.5
```

Wide sigma -> wider threshold -> speculative edges are not prematurely flagged.  
Narrow sigma -> tighter threshold -> well-attested edges are held to strict standards.

---

## Part 7: Anti-Crystal Schema

An anti-crystal is a systematic phase inversion of an existing crystal.

For every edge with phase `theta`, the anti-crystal stores `wrap_pi(theta + pi)`.

Anti-crystals are valid RWIFC1 files. They are identified by:

1. `anti_crystal_id` field in the source crystal pointing to the anti-crystal's UUID
2. `tags` field containing `"anti_crystal"`
3. All edge `reinforcing` fields inverted

### 7.1 Annihilation Score

When a crystal and its anti-crystal are instantiated together in CSIF:

```text
annihilation_score = mean over all edges of:
  phase_distance(theta_crystal, theta_anti) / pi
```

A perfect anti-crystal scores `1.0`. Any deviation from perfect anti-phase indicates
partial coherence between the crystal and its complement.

### 7.2 Use Cases

- **Negation modeling:** Store "X is not Y" as the anti-crystal of "X is Y"
- **Counterfactual reasoning:** Instantiate anti-crystals to explore what the world
  would look like if a known fact were false
- **Adversarial robustness:** Test contradiction detection by injecting anti-crystals
- **Dialectical synthesis:** Measure residual between thesis crystal and
  antithesis anti-crystal; the residual encodes the synthesis target
- **Disinformation detection:** Flag content whose phase geometry matches an
  anti-crystal of established knowledge

---

## Part 8: Relationship to RWIF4 / RWIF5

RWIF4 and RWIF5 store transformer model activation lattices - the internal spherical
harmonic representations of an LLM's concept geometry at specific layers.

This schema (RWIF Crystal V1) stores semantic knowledge crystals - the external,
auditable phase-geometric records of what is known.

They are distinct formats. They should not be mixed in the same file or parsed
by the same reader without explicit conversion.

### 8.1 The Bridge: LLM Activation -> Crystal Phase

RWIF4/5 activations can serve as the *source* of phase values for RWIF Crystal V1.
The intended pipeline is:

```text
RWIF4/5 lattice (LLM internal geometry)
  ↓
Phase extraction: map (l, m) spherical harmonic coefficients
  to concept-pair phase angles via geometric projection
  ↓
Phase encoding event: write initial_encoding trajectory entry
  into RWIF Crystal V1 edge
  ↓
Consensus gate: require >=3 independent source activations
  before crystallizing the phase value
  ↓
CSIF instantiation: load RWIF Crystal V1 for geometric
  computation, contradiction detection, resonance scoring
```

This pipeline closes the loop between the LLM's internal geometry (RWIF4/5)
and the external auditable knowledge structure (RWIF Crystal V1).

**Status:** This bridge is architecturally specified but not yet implemented.
It is the next major engineering milestone after the crystal schema is locked.

---

## Part 9: Validation Rules

### 9.1 RWIFC1 (Single Crystal)

1. Magic bytes equal `RWIFC1\x00\x00`
2. `schema` equals `rwif_crystal`
3. `schema_version` starts with `crystal-1.`
4. `crystal_id` is a valid UUID v4
5. `node_count` matches the actual number of node entries
6. `edge_count` matches the actual number of edge entries
7. Every edge `source_node` and `target_node` references a valid `node_id`
8. Every `phase_trajectory` entry has `phase` in `[-pi, pi]`
9. Every `confidence_band` is in `[0, pi]`
10. `phase_trajectory` entries are sorted by `timestamp` ascending
11. If `frozen = true`, no trajectory entry after the `crystallization` event
    may have `event_type` other than read-only audit entries
12. `stability_score` is in `[0, 1]`
13. If `header_checksum` present, it validates over canonical header JSON
14. If `layout_checksum` present, it validates over all payload blocks

### 9.2 RWIFB1 (Crystal Bank)

All RWIFC1 rules apply to each embedded crystal, plus:

1. Magic bytes equal `RWIFB1\x00\x00`
2. `crystal_count` matches index entry count
3. Every index entry offset falls within `[payload_offset, file_end)`
4. No two index entries share the same `crystal_id`
5. Index `stability` values match the embedded crystal's `stability_score`
6. If `index_checksum` present, it validates over the index block
7. If `payload_checksum` present, it validates over concatenated crystal blobs

---

## Part 10: Reference Examples

### 10.1 Minimal Single Crystal Header

```json
{
  "schema": "rwif_crystal",
  "schema_version": "crystal-1.0.0",
  "crystal_id": "3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c",
  "crystal_label": "whale_mammal_coherent",
  "domain": "biology",
  "lobe": "English",
  "node_count": 3,
  "edge_count": 3,
  "stability_score": 1.0,
  "frozen": true,
  "created": "2026-05-17T00:00:00Z",
  "crystal_count": 1,
  "checksum_algorithm": "sha256",
  "header_checksum": "...",
  "layout_checksum": "..."
}
```

### 10.2 Minimal Edge with Trajectory

```json
{
  "edge_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "source_node": "node-uuid-whale",
  "relation": "is_a",
  "target_node": "node-uuid-mammal",
  "lobe": "English",
  "reinforcing": true,
  "base_phase": 0.5236,
  "confidence_band": 0.04,
  "phase_trajectory": [
    {
      "timestamp": "2026-01-15T10:00:00Z",
      "phase": 0.52,
      "confidence_band": 0.12,
      "drift_delta": 0.0,
      "event_type": "initial_encoding",
      "source": {
        "type": "llm_encoding",
        "model_id": "claude-sonnet-4",
        "run_id": "enc-run-001",
        "input_text_hash": "sha256:abcdef...",
        "timestamp": "2026-01-15T10:00:00Z"
      }
    },
    {
      "timestamp": "2026-03-01T14:30:00Z",
      "phase": 0.5236,
      "confidence_band": 0.04,
      "drift_delta": 0.0036,
      "event_type": "crystallization",
      "source": {
        "type": "consensus_gate",
        "source_count": 3,
        "sources": ["wikipedia-cetacea", "britannica-mammals", "marine-bio-textbook-ch4"],
        "timestamp": "2026-03-01T14:30:00Z"
      }
    }
  ],
  "provenance": {
    "encoding_model": "claude-sonnet-4",
    "encoding_run": "enc-run-001",
    "source_documents": ["wikipedia-cetacea", "britannica-mammals", "marine-bio-textbook-ch4"],
    "feedback_events": 1,
    "last_updated": "2026-03-01T14:30:00Z"
  }
}
```

### 10.3 Cross-Lobe Example

Same relationship encoded in two lobes:

```json
[
  {
    "edge_id": "edge-english-001",
    "source_node": "node-light-en",
    "relation": "dispels",
    "target_node": "node-darkness-en",
    "lobe": "English",
    "reinforcing": true,
    "base_phase": 0.0,
    "confidence_band": 0.02
  },
  {
    "edge_id": "edge-spanish-001",
    "source_node": "node-luz-es",
    "relation": "disipa",
    "target_node": "node-oscuridad-es",
    "lobe": "Spanish",
    "reinforcing": true,
    "base_phase": 0.0,
    "confidence_band": 0.03
  }
]
```

Cross-lobe resonance: `phase_distance(0.0, 0.0) / pi = 0.0` - perfect alignment.

---

## Part 11: Core Math Reference

All implementations must use these exact functions for geometric correctness:

```python
import math

def wrap_pi(theta):
    """Wrap angle to [-pi, pi]."""
    return ((theta + math.pi) % (2 * math.pi)) - math.pi

def phase_distance(theta_a, theta_b):
    """Angular distance between two phase values."""
    return abs(wrap_pi(theta_a - theta_b))

def normalized_resonance(theta_a, theta_b):
    """Normalized resonance. 0.0 = perfect coherence, 1.0 = maximum opposition."""
    return phase_distance(theta_a, theta_b) / math.pi

def contradiction_threshold(sigma, c=0.5):
    """Adaptive contradiction detection threshold."""
    return math.pi / 2 + c * sigma

def nudge_phase(theta, error_signal, evidence_weight, alpha=0.1):
    """Apply one outcome-driven phase correction."""
    delta = alpha * error_signal * evidence_weight
    return wrap_pi(theta + delta)

def tighten_sigma(sigma, evidence_weight, rate=0.1):
    """Tighten confidence band with new evidence."""
    return sigma * (1.0 - evidence_weight * rate)
```

---

## Part 12: Relationship to CSIF Architecture

This schema is the storage layer for the complete CSIF + RWIF architecture
described in `CSIF_RWIF_COMPLETE_ARCHITECTURE.md`.

The operational flow is:

```text
RWIF Crystal V1 file (dormant storage)
  ↓  load + parse
CSIF crystal bank (live, geometric, queryable)
  ↓  query / compare / detect contradictions
Resonance scores, conflict traces, provenance
  ↓  outcome observation
Phase nudge events appended to trajectory
  ↓  serialize
RWIF Crystal V1 file (updated, append-only history preserved)
```

Every phase change is written back to the trajectory. No history is ever lost.
Every query result is traceable to specific trajectory events, timestamps,
and source provenance.

---

## Appendix A: Relation Type Phase Conventions

Recommended base phases by relation type. These are conventions, not hard constraints.
Implementations may calibrate from empirical data (see Milestone D in the
CSIF milestone chain).

| Relation | Base Phase | Notes |
|---|---|---|
| `is_a` | `pi/6` (~0.524) | Class membership |
| `has_property` | `pi/6` (~0.524) | Property attribution |
| `implies` | `pi/8` (~0.393) | Logical implication |
| `causes` | `pi/4` (~0.785) | Causal relation |
| `supports` | `pi/12` (~0.262) | Evidential support |
| `synonym` | `0.0` | Identity-class equivalence |
| `antonym` | `pi` | Direct opposition |
| `hyponym` | `pi/2` (~1.571) | Narrower term |
| `domain_relation` | `pi/4` (~0.785) | Cross-domain bridge |
| `polyseme` | `pi/6` (~0.524) | Same form, different sense |

Anti-phase (negation) of any relation: `wrap_pi(base_phase + pi)`

---

## Appendix B: File Extension Conventions

| Extension | Meaning |
|---|---|
| `.rwif-crystal` | Single crystal (RWIFC1) |
| `.rwif-bank` | Crystal bank (RWIFB1) |
| `.rwif-crystal.json` | Human-readable JSON export (not binary format) |
| `.rwif-crystal.yaml` | YAML export (used by Language Banks in CSIF) |

---

## Appendix C: Changelog

| Version | Date | Changes |
|---|---|---|
| `crystal-1.0.0` | 2026-05-17 | Initial schema definition |

---

*This document is part of the Crystal Information Engine (CIE) / CSIF project.*  
*Repository: https://github.com/MoTechnicalities/Crystal-Structure-Information-Format*  
*This specification is living and will evolve with the project.*
