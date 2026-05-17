# CSIF Engine Specification V1

**Document type:** Engine Specification  
**Author:** Mogir Jason Rofick (Mo)  
**Date:** May 17, 2026  
**Status:** Draft v1.0  
**Semantic version:** `csif-engine-1.0.0`  
**Audience:** AI Systems, Engineers, Implementers

---

## Purpose

This document specifies the Crystal Structure Information Format (CSIF) engine -
the active computational medium where RWIF Crystal V1 files are instantiated as
live, queryable, geometric knowledge structures.

The architecture is described in `CSIF_RWIF_COMPLETE_ARCHITECTURE.md`.
The storage format is specified in `RWIF_CRYSTAL_SCHEMA_V1.md`.
This document specifies the engine itself: data structures, algorithms,
interfaces, and behavioral contracts.

An engineer reading this document in combination with `RWIF_CRYSTAL_SCHEMA_V1.md`
should be able to implement a CSIF-compatible engine from scratch without reading
the Python source.

---

## Part 1: Core Data Structures

### 1.1 ConceptNode

Represents a concept in the active crystal graph.

```text
ConceptNode {
  node_id:    string (UUID v4)
  label:      string (canonical)
  aliases:    list[string]
  lobe:       string
  provenance: ProvenanceRecord
}
```

### 1.2 CrystalEdge

Represents a typed semantic relationship between two nodes, carrying live phase state.

```text
CrystalEdge {
  edge_id:          string (UUID v4)
  source_node:      string (node_id)
  relation:         string
  target_node:      string (node_id)
  lobe:             string
  reinforcing:      bool
  base_phase:       float   // theta_0, in [-pi, pi]
  confidence_band:  float   // sigma, in [0, pi]
  trajectory:       list[TrajectoryEvent]  // append-only
}
```

Current phase is always `trajectory[-1].phase`.
Current sigma is always `trajectory[-1].confidence_band`.

### 1.3 TrajectoryEvent

One timestamped phase state entry. Immutable once appended.

```text
TrajectoryEvent {
  timestamp:        string (ISO 8601)
  phase:            float   // in [-pi, pi]
  confidence_band:  float   // sigma, in [0, pi]
  drift_delta:      float   // change from prior event
  event_type:       string  // see RWIF Crystal Schema V1 §4.2
  source:           object  // provenance, structure varies by event_type
}
```

### 1.4 Crystal

A directed semantic graph of ConceptNodes and CrystalEdges.

```text
Crystal {
  crystal_id:      string (UUID v4)
  crystal_label:   string
  domain:          string
  lobe:            string
  frozen:          bool
  nodes:           map[node_id -> ConceptNode]
  edges:           map[edge_id -> CrystalEdge]
  version_history: list[VersionEntry]
  stability_score: float   // mean trust across all edges, [0, 1]
}
```

Stability score computation:

```text
stability_score = mean(1.0 - (sigma / pi) for each edge)
```

A frozen crystal accepts no new nodes or edges. Trajectory appends to existing
edges are still permitted after freeze.

### 1.5 PhaseGraph

A lightweight computation structure built from one or more crystals for
multi-path conflict analysis. Not persisted - rebuilt on demand.

```text
PhaseGraph {
  nodes:  set[string]              // concept labels (not node_ids)
  edges:  list[PhaseEdge]
}

PhaseEdge {
  source:  string   // concept label
  target:  string   // concept label
  phase:   float    // current phase value
  sigma:   float    // current confidence band
  edge_id: string   // reference back to CrystalEdge
}
```

PhaseGraph uses concept labels (not UUIDs) as node keys so that edges from
different crystals sharing the same concept label can be merged into one graph
for multi-path analysis.

### 1.6 ConflictPathTrace

Auditable record of one detected contradiction between two paths.

```text
ConflictPathTrace {
  source:   string          // concept label
  target:   string          // concept label
  path_a:   list[string]    // ordered concept labels along path A
  path_b:   list[string]    // ordered concept labels along path B
  phase_a:  float           // composed phase along path A
  phase_b:  float           // composed phase along path B
  residual: float           // phase_distance(phase_a, phase_b)
}
```

### 1.7 ResonanceResult

Output of a resonance computation between two crystals.

```text
ResonanceResult {
  crystal_a_id:          string
  crystal_b_id:          string
  raw_resonance:         float   // sum of angular distances
  normalized_resonance:  float   // in [0, 1]
  phase_conflict_score:  float   // max multi-path residual
  phase_conflict_traces: list[ConflictPathTrace]
  edge_count:            int     // number of aligned edges compared
  status:                string  // "coherent" | "divergent" | "contradictory"
  confidence:            float   // 1.0 - normalized_resonance
}
```

### 1.8 CrystallizeResult

Output of ingesting text or structured input into the crystal bank.

```text
CrystallizeResult {
  crystal_id:        string
  crystal_label:     string
  action:            string   // "created" | "updated" | "rejected"
  stability_score:   float
  phase_conflicts:   list[CrossCrystalConflict]
  concept_nodes:     list[string]   // canonical labels used
  edge_count:        int
  provenance:        object
}
```

### 1.9 CrossCrystalConflict

A detected contradiction between a newly ingested crystal and an existing bank crystal.

```text
CrossCrystalConflict {
  conflicting_crystal_id:    string
  conflicting_crystal_label: string
  max_residual:              float
  traces:                    list[ConflictPathTrace]
}
```

---

## Part 2: Core Mathematical Functions

All implementations must use these exact functions. Deviation breaks
cross-implementation compatibility.

### 2.1 wrap_pi

Wrap any angle to the principal interval `[-pi, pi]`.

```text
wrap_pi(theta):
  return ((theta + pi) mod (2 * pi)) - pi
```

### 2.2 phase_distance

Angular distance between two phase values. Always non-negative.
Correctly handles circular wraparound.

```text
phase_distance(theta_a, theta_b):
  return abs(wrap_pi(theta_a - theta_b))
```

### 2.3 normalized_resonance

Dimensionless alignment measure. `0.0` = perfect coherence, `1.0` = maximum opposition.

```text
normalized_resonance(theta_a, theta_b):
  return phase_distance(theta_a, theta_b) / pi
```

### 2.4 circular_mean

Correct mean of angles on a circle. Arithmetic mean of angles is incorrect
due to wraparound.

```text
circular_mean(phases):
  sin_sum = sum(sin(p) for p in phases)
  cos_sum = sum(cos(p) for p in phases)
  return atan2(sin_sum, cos_sum)
```

### 2.5 contradiction_threshold

Adaptive contradiction detection threshold. Widens with uncertainty.

```text
contradiction_threshold(sigma, c=0.5):
  return pi/2 + c * sigma
```

### 2.6 compose_path_phase

Compose phase angles along a directed path through the graph.

```text
compose_path_phase(phases):
  // phases: ordered list of edge phase values along a path
  total = sum(phases)
  return wrap_pi(total)
```

### 2.7 nudge_phase

Apply one outcome-driven phase correction.

```text
nudge_phase(theta, error_signal, evidence_weight, alpha=0.1):
  delta = alpha * error_signal * evidence_weight
  return wrap_pi(theta + delta)
```

### 2.8 tighten_sigma

Reduce confidence band width as evidence accumulates.

```text
tighten_sigma(sigma, evidence_weight, rate=0.1):
  return sigma * (1.0 - evidence_weight * rate)
```

---

## Part 3: PhaseGraph Construction

### 3.1 Building from a Single Crystal

```text
build_phase_graph(crystal):
  graph = PhaseGraph(nodes={}, edges=[])
  for edge in crystal.edges.values():
    source_label = crystal.nodes[edge.source_node].label
    target_label = crystal.nodes[edge.target_node].label
    graph.nodes.add(source_label)
    graph.nodes.add(target_label)
    graph.edges.append(PhaseEdge(
      source  = source_label,
      target  = target_label,
      phase   = current_phase(edge),
      sigma   = current_sigma(edge),
      edge_id = edge.edge_id
    ))
  return graph
```

`current_phase(edge)` returns `edge.trajectory[-1].phase`.
`current_sigma(edge)` returns `edge.trajectory[-1].confidence_band`.

### 3.2 Building from Two Crystals (Cross-Crystal Merge)

Used for cross-crystal contradiction detection. Shared concept labels
are bridge nodes - no new edge is added for the bridge itself.

```text
build_merged_phase_graph(crystal_a, crystal_b):
  graph_a = build_phase_graph(crystal_a)
  graph_b = build_phase_graph(crystal_b)

  shared_labels = graph_a.nodes ∩ graph_b.nodes

  merged = PhaseGraph(nodes={}, edges=[])
  merged.nodes = graph_a.nodes ∪ graph_b.nodes
  merged.edges = graph_a.edges + graph_b.edges

  // Bridge edges: zero-phase self-loops on shared nodes
  // allow path composition to cross from crystal_a to crystal_b
  for label in shared_labels:
    merged.edges.append(PhaseEdge(
      source  = label,
      target  = label,
      phase   = 0.0,
      sigma   = 0.0,
      edge_id = None   // bridge, no backing edge
    ))

  return merged, shared_labels
```

---

## Part 4: Multi-Path Conflict Detection

This is the primary contradiction detection algorithm. It operates on a PhaseGraph.

### 4.1 All Simple Paths

Enumerate all simple paths (no repeated nodes) from source to target in the graph.

```text
all_simple_paths(graph, source, target, max_depth=10):
  // Standard DFS with visited set
  // Returns list of paths, each path is list[concept_label]
  // Limit max_depth to prevent combinatorial explosion on dense graphs
```

### 4.2 Path Phase Composition

```text
path_phase(graph, path):
  // path: ordered list of concept labels
  phases = []
  for i in range(len(path) - 1):
    edge = find_edge(graph, path[i], path[i+1])
    phases.append(edge.phase)
  return compose_path_phase(phases)
```

If multiple edges exist between the same pair of nodes, select the one
with the lowest sigma (highest confidence). If sigmas are equal, select
the one with the lowest phase_distance to 0.

### 4.3 Pairwise Path Conflict

```text
pairwise_conflict(graph, source, target):
  paths = all_simple_paths(graph, source, target)
  if len(paths) < 2:
    return 0.0, []

  max_residual = 0.0
  traces = []

  for i in range(len(paths)):
    for j in range(i+1, len(paths)):
      phase_i = path_phase(graph, paths[i])
      phase_j = path_phase(graph, paths[j])
      residual = phase_distance(phase_i, phase_j)

      traces.append(ConflictPathTrace(
        source   = source,
        target   = target,
        path_a   = paths[i],
        path_b   = paths[j],
        phase_a  = phase_i,
        phase_b  = phase_j,
        residual = residual
      ))

      if residual > max_residual:
        max_residual = residual

  return max_residual, traces
```

### 4.4 Max Multi-Path Conflict Score

```text
max_multipath_phase_conflict(graph):
  global_max = 0.0
  all_traces = []

  for source in graph.nodes:
    for target in graph.nodes:
      if source == target:
        continue
      score, traces = pairwise_conflict(graph, source, target)
      all_traces.extend(traces)
      if score > global_max:
        global_max = score

  return global_max, all_traces
```

### 4.5 Contradiction Classification

Given a PhaseGraph and a crystal's mean sigma:

```text
classify_contradiction(phase_conflict_score, sigma):
  threshold = contradiction_threshold(sigma)

  if phase_conflict_score < threshold * 0.1:
    return "coherent"
  elif phase_conflict_score < threshold:
    return "divergent"
  else:
    return "contradictory"
```

### 4.6 Top Conflict Traces

Return only the N highest-residual traces for API responses:

```text
top_conflict_traces(traces, n=5):
  return sorted(traces, key=lambda t: t.residual, reverse=True)[:n]
```

---

## Part 5: Resonance Scoring

### 5.1 Edge-Aligned Resonance

Computes resonance between two crystals over their shared edge topology.
Edges are aligned by (source_label, relation, target_label) triple.

```text
compute_resonance(crystal_a, crystal_b):
  aligned_edges = find_aligned_edges(crystal_a, crystal_b)

  if len(aligned_edges) == 0:
    return ResonanceResult with normalized_resonance=1.0, status="divergent"

  raw = sum(
    phase_distance(edge_a.current_phase, edge_b.current_phase)
    for edge_a, edge_b in aligned_edges
  )

  normalized = raw / (len(aligned_edges) * pi)

  // Multi-path conflict over merged graph
  merged_graph, _ = build_merged_phase_graph(crystal_a, crystal_b)
  conflict_score, traces = max_multipath_phase_conflict(merged_graph)

  // Effective delta uses the worse of direct resonance and multi-path conflict
  effective_delta = max(normalized, conflict_score / pi)

  mean_sigma = mean(
    edge.current_sigma
    for edge_a, edge_b in aligned_edges
    for edge in [edge_a, edge_b]
  )

  status = classify_contradiction(conflict_score, mean_sigma)

  return ResonanceResult(
    crystal_a_id          = crystal_a.crystal_id,
    crystal_b_id          = crystal_b.crystal_id,
    raw_resonance         = raw,
    normalized_resonance  = normalized,
    phase_conflict_score  = conflict_score,
    phase_conflict_traces = top_conflict_traces(traces),
    edge_count            = len(aligned_edges),
    status                = status,
    confidence            = 1.0 - effective_delta
  )
```

### 5.2 Edge Alignment

Two edges are aligned if they share the same source label, relation type,
and target label, in the same lobe:

```text
find_aligned_edges(crystal_a, crystal_b):
  aligned = []
  index_a = {
    (nodes_a[e.source_node].label, e.relation, nodes_a[e.target_node].label): e
    for e in crystal_a.edges.values()
  }
  for e_b in crystal_b.edges.values():
    key = (nodes_b[e_b.source_node].label, e_b.relation, nodes_b[e_b.target_node].label)
    if key in index_a:
      aligned.append((index_a[key], e_b))
  return aligned
```

Cross-lobe resonance (comparing edges in different lobes) uses the same
algorithm but does not require lobe equality in the alignment key.
Cross-lobe comparison should be explicit and marked in the ResonanceResult.

---

## Part 6: Crystal Bank Manager

The CrystalBankManager is the runtime interface between the CSIF engine
and the RWIF Crystal V1 storage layer.

### 6.1 Interface Contract

```text
CrystalBankManager {

  // Load a crystal from a RWIF Crystal V1 file into the active bank
  load(path: string) -> Crystal

  // Persist a crystal from the active bank to a RWIF Crystal V1 file
  persist(crystal_id: string, path: string) -> void

  // Add a new crystal to the active bank
  add(crystal: Crystal) -> void

  // Retrieve a crystal by ID
  get(crystal_id: string) -> Crystal | None

  // List all crystals in the bank
  list() -> list[CrystalSummary]

  // Query: find crystals most resonant with a query crystal
  query(query_crystal: Crystal, top_k: int=5) -> list[ResonanceResult]

  // Crystallize: ingest text or structured input, create or update crystal
  crystallize_text(text: string, label: string, lobe: string) -> CrystallizeResult

  // Cross-crystal conflict check against all bank crystals
  check_conflicts(crystal: Crystal) -> list[CrossCrystalConflict]

  // Apply an outcome nudge to a specific edge
  nudge_edge(crystal_id: string, edge_id: string,
             error_signal: float, evidence_weight: float) -> TrajectoryEvent

  // Freeze a crystal (no new nodes or edges)
  freeze(crystal_id: string) -> void

  // Export bank summary statistics
  stats() -> BankStats
}
```

### 6.2 CrystalSummary

Lightweight descriptor returned by `list()`:

```text
CrystalSummary {
  crystal_id:      string
  crystal_label:   string
  domain:          string
  lobe:            string
  frozen:          bool
  node_count:      int
  edge_count:      int
  stability_score: float
  last_updated:    string (ISO 8601)
}
```

### 6.3 BankStats

```text
BankStats {
  crystal_count:        int
  total_nodes:          int
  total_edges:          int
  frozen_count:         int
  mean_stability:       float
  contradiction_count:  int   // crystals currently flagged contradictory
  lobe_distribution:    map[lobe -> int]
  domain_distribution:  map[domain -> int]
}
```

### 6.4 Query Behavior

`query(query_crystal, top_k)` must:

1. Check the fast cache first (normalized query text -> crystal_id mapping)
2. If cache miss, compute resonance between query_crystal and every bank crystal
3. Return top_k results sorted by `normalized_resonance` ascending
   (lower resonance = higher similarity)
4. Populate cache with result for subsequent identical queries
5. Never return the query crystal itself if it exists in the bank

Cache keys are derived from normalized concept label sets, not raw text.
Cache entries are invalidated when the referenced crystal is updated.

---

## Part 7: Text Crystallization Pipeline

### 7.1 Pipeline Stages

When `crystallize_text(text, label, lobe)` is called:

```text
Stage 1: Concept Extraction
  - Tokenize and filter stopwords
  - Extract candidate concept pairs by co-occurrence
  - Apply Language Bank normalization if available:
      for each extracted term:
        canonical = language_bank.lookup(term, lobe)
        if canonical exists: use canonical label, record original as alias
        else: use term as-is

Stage 2: Polarity Detection
  - For each sentence containing a concept pair:
      if sentence contains negation token:
        theta = pi   // anti-phase
        reinforcing = false
      else:
        theta = base_phase_for_relation(relation_type)
        reinforcing = true

Stage 3: Edge Construction
  - For each concept pair with detected polarity:
      create CrystalEdge with:
        base_phase = theta
        confidence_band = sigma_initial (default: 0.2)
        trajectory = [initial_encoding event]

Stage 4: Crystal Construction
  - Create Crystal with extracted nodes and edges
  - Compute stability_score

Stage 5: Cross-Crystal Conflict Check
  - Build PhaseGraph from new crystal
  - For each existing bank crystal:
      merged, shared = build_merged_phase_graph(new, existing)
      if shared is not empty:
        score, traces = max_multipath_phase_conflict(merged)
        if score > contradiction_threshold(mean_sigma):
          record CrossCrystalConflict

Stage 6: Bank Registration
  - Add crystal to bank
  - Write to RWIF Crystal V1 file (async, non-blocking)
  - Return CrystallizeResult
```

### 7.2 Negation Tokens

Default negation token list (extend per domain):

```text
["not", "never", "no", "cannot", "can't", "isn't", "aren't", "wasn't",
 "weren't", "doesn't", "don't", "didn't", "won't", "wouldn't", "couldn't",
 "shouldn't", "cold-blooded", "non-", "anti-", "un-"]
```

### 7.3 Initial Sigma Values by Source

```text
sigma_initial by source type:
  llm_encoding:       0.2   // LLM inference is uncertain until validated
  manual_teach:       0.1   // Human-provided, higher initial confidence
  consensus_gate:     0.05  // Three or more sources agreed
  adjudication:       0.02  // Human expert reviewed and confirmed
```

---

## Part 8: Consensus Gate

Before a phase value is crystallized (frozen), it must pass the consensus gate.

### 8.1 Gate Criteria

```text
consensus_gate(edge, proposed_phase, sources):
  if len(sources) < 3:
    return DEFERRED   // queue for more evidence

  // Check source independence: no two sources may be from the same document
  if any two sources share the same document_id:
    return DEFERRED

  // Check phase agreement: all sources must agree within tolerance
  phases = [s.proposed_phase for s in sources]
  spread = max(phases) - min(phases)
  if spread > pi / 4:
    return CONTESTED   // route to human adjudication

  // Gate passed: crystallize
  consensus_phase = circular_mean(phases)
  return PASS, consensus_phase
```

### 8.2 Gate Outcomes

| Outcome | Meaning | Action |
|---|---|---|
| `PASS` | Three+ sources agree | Append `consensus_gate` trajectory event, tighten sigma |
| `DEFERRED` | Fewer than three sources | Queue proposal, await more evidence |
| `CONTESTED` | Sources disagree beyond tolerance | Route to Teach panel for adjudication |

---

## Part 9: Anti-Crystal Engine Operations

### 9.1 Generating an Anti-Crystal

```text
generate_anti_crystal(crystal):
  anti = Crystal(
    crystal_id    = new_uuid(),
    crystal_label = crystal.crystal_label + "_anti",
    domain        = crystal.domain,
    lobe          = crystal.lobe,
    frozen        = crystal.frozen
  )

  // Copy nodes unchanged
  anti.nodes = deep_copy(crystal.nodes)

  // Invert all edge phases and reinforcing flags
  for edge in crystal.edges.values():
    anti_edge = deep_copy(edge)
    anti_edge.edge_id = new_uuid()
    anti_edge.reinforcing = not edge.reinforcing
    anti_phase = wrap_pi(current_phase(edge) + pi)
    // Append anti-phase as new trajectory event
    anti_edge.trajectory.append(TrajectoryEvent(
      timestamp        = now(),
      phase            = anti_phase,
      confidence_band  = current_sigma(edge),
      drift_delta      = phase_distance(current_phase(edge), anti_phase),
      event_type       = "anti_crystal_generation",
      source           = { "type": "anti_crystal", "source_crystal_id": crystal.crystal_id }
    ))
    anti.edges[anti_edge.edge_id] = anti_edge

  // Cross-reference
  crystal.anti_crystal_id = anti.crystal_id
  anti.tags = ["anti_crystal"]

  return anti
```

### 9.2 Annihilation Score

```text
annihilation_score(crystal, anti_crystal):
  aligned = find_aligned_edges(crystal, anti_crystal)
  if len(aligned) == 0:
    return 0.0

  scores = [
    phase_distance(current_phase(e_a), current_phase(e_b)) / pi
    for e_a, e_b in aligned
  ]
  return mean(scores)
```

A perfect anti-crystal scores `1.0`.
Values below `1.0` indicate partial coherence (some edges were not fully inverted
or have drifted from perfect anti-phase through temporal evolution).

---

## Part 10: API Surface

The CSIF engine exposes its capabilities through a structured API.
All endpoints return JSON. All write operations are idempotent where possible.

### 10.1 Core Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/teach` | Ingest text, create or update crystal |
| `POST` | `/v1/source/teach` | Ingest structured source with domain metadata |
| `POST` | `/v1/autolearn/upload` | Upload document for pipeline processing |
| `GET` | `/v1/autolearn/events/stream` | SSE stream of pipeline events |
| `POST` | `/v1/chat/completions` | Query interface (OpenAI-compatible) |

### 10.2 Crystal Bank Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/v1/bank/list` | List all crystals |
| `GET` | `/v1/bank/{crystal_id}` | Get crystal summary |
| `GET` | `/v1/bank/{crystal_id}/export` | Export as RWIF Crystal V1 |
| `POST` | `/v1/bank/{crystal_id}/nudge` | Apply outcome nudge to edge |
| `POST` | `/v1/bank/{crystal_id}/freeze` | Freeze crystal |
| `GET` | `/v1/bank/stats` | Bank summary statistics |

### 10.3 Language Bank Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/lang_bank/create` | Create new Language Bank |
| `POST` | `/v1/lang_bank/{bank_id}/add_term` | Add term node |
| `POST` | `/v1/lang_bank/{bank_id}/add_edge` | Add term relationship |
| `GET` | `/v1/lang_bank/{bank_id}/query` | Query single bank |
| `POST` | `/v1/lang_bank/federated_query` | Query across banks |
| `GET` | `/v1/lang_bank/{bank_id}/graph` | Graph visualization payload |
| `POST` | `/v1/lang_bank/{bank_id}/audit_trace` | Term audit trace |
| `POST` | `/v1/lang_bank/{bank_id}/propose_change` | Queue edit proposal |
| `GET` | `/v1/lang_bank/{bank_id}/proposals` | List pending proposals |

### 10.4 Standard Response Envelope

All API responses include:

```json
{
  "status": "ok | error",
  "intent": "QUERY | TEACH | COMPARE | TASK",
  "crystal_id": "uuid or null",
  "answer": "string",
  "confidence": 0.0,
  "phase_conflict_score": 0.0,
  "phase_conflict_traces": [],
  "autolearn": {
    "status": "existing_crystal | new_crystal | no_consensus | disabled",
    "crystal_label": "string or null"
  },
  "reasoning_steps": [],
  "context_stats": {
    "preflight_strong_bank_match": false,
    "context_short_circuit": false
  }
}
```

### 10.5 Phase Conflict Fields (Required in All Responses)

`phase_conflict_score` and `phase_conflict_traces` must always be present
in API responses. An absence of contradictions is represented by:

```json
{
  "phase_conflict_score": 0.0,
  "phase_conflict_traces": []
}
```

This is a schema lock requirement. Downstream consumers must be able to
rely on these fields being present without defensive null checks.

---

## Part 11: Caching and Latency

### 11.1 Fast Cache

The fast cache maps normalized query keys to crystal_id + answer pairs.

```text
cache_key(query_text):
  normalized = lowercase(strip_punctuation(query_text))
  normalized = remove_trailing_context_notes(normalized)
  return sha256(normalized)
```

Cache entries are stored as JSON in `_autolearn_query_cache.json` under
the bank directory. Writes use atomic temp-file replace to prevent
partial writes on crash.

Cache invalidation:
- On crystal update: invalidate all entries referencing that crystal_id
- On crystal deletion: invalidate all entries referencing that crystal_id
- On freeze: no invalidation required

### 11.2 Preflight Bank Check

Before any expensive LLM context expansion, the engine performs a fast
preflight check:

```text
preflight_check(query_text):
  key = cache_key(query_text)
  entry = cache.get(key)
  if entry is not None and entry.confidence >= STRONG_MATCH_THRESHOLD:
    return SHORT_CIRCUIT, entry
  return CONTINUE, None
```

`STRONG_MATCH_THRESHOLD` default: `0.85`

When a preflight short-circuit occurs, the response includes:
`"context_short_circuit": true` and `"preflight_strong_bank_match": true`.

### 11.3 Target Latency Budgets

| Path | Target |
|---|---|
| Preflight cache hit | < 10ms |
| Bank resonance scan (< 100 crystals) | < 100ms |
| Full LLM context expansion | < 30s (LLM-dependent) |
| Post-response crystallization | async, non-blocking |

---

## Part 12: Observability

### 12.1 Required Log Events

All CSIF engine implementations must emit structured log events for:

| Event | When |
|---|---|
| `crystal_created` | New crystal added to bank |
| `crystal_updated` | Existing crystal received new trajectory event |
| `crystal_frozen` | Crystal frozen |
| `contradiction_detected` | Cross-crystal conflict score exceeds threshold |
| `consensus_gate_passed` | Edge phase crystallized by consensus |
| `consensus_gate_deferred` | Insufficient sources, proposal queued |
| `consensus_gate_contested` | Sources disagree, routed to adjudication |
| `cache_hit` | Query resolved from fast cache |
| `cache_miss` | Query required full bank scan |
| `preflight_short_circuit` | Strong bank hit bypassed context expansion |
| `nudge_applied` | Outcome nudge written to edge trajectory |

### 12.2 Event Schema

```json
{
  "event": "contradiction_detected",
  "timestamp": "ISO 8601",
  "crystal_id": "uuid",
  "conflicting_crystal_id": "uuid",
  "phase_conflict_score": 3.1416,
  "trace_count": 2,
  "top_residual": 3.1416
}
```

---

## Part 13: Behavioral Contracts

These are required behaviors. Implementations that violate these contracts
are not CSIF-compatible.

### 13.1 Immutability

1. Trajectory entries are append-only. No trajectory event may be modified
   or deleted after it is written.
2. A frozen crystal accepts no new nodes or edges. This is enforced at the
   bank manager level, not only at the file level.
3. `base_phase` and `crystal_id` are immutable after crystal creation.

### 13.2 Auditability

1. Every response that reports a contradiction must include at least one
   `ConflictPathTrace` in `phase_conflict_traces`.
2. Every trajectory event must include a `source` object with enough
   provenance to identify the origin of the phase change.
3. The bank manager must be able to reconstruct any historical crystal
   state from the trajectory record alone.

### 13.3 Determinism

1. Given the same crystal bank state and the same query, the engine must
   return the same resonance scores and conflict traces.
2. `wrap_pi`, `phase_distance`, and `normalized_resonance` must produce
   identical float results across implementations (use IEEE 754
   double precision throughout).
3. The fast cache must not alter observable query results - only latency.

### 13.4 Graceful Degradation

1. If a Language Bank is unavailable, concept extraction falls through
   to raw string matching without error.
2. If the LLM encoder is unavailable, the engine returns the bank result
   if one exists, or a structured error if not. It does not silently
   return empty results.
3. If a crystal file is corrupt or unreadable, the bank manager logs the
   error and continues serving other crystals. It does not crash.

### 13.5 Non-Destructive Defaults

1. Semantic bridge proposals are queued, not applied directly.
2. Consensus gate failures route to adjudication, not silent rejection.
3. Anti-crystal generation does not modify the source crystal in place.

---

## Part 14: Regression Test Requirements

A CSIF-compatible implementation must pass the following test classes:

| Test Class | What is verified |
|---|---|
| Phase math | `wrap_pi`, `phase_distance`, `normalized_resonance` produce correct values including edge cases (theta = pi, theta = -pi, theta = 0) |
| Contradiction detection | Whale experiment: coherent residual near 0, contradictory residual near pi |
| Multi-path conflict | Two-path graph: coherent score = 0.0, anti-phase score = pi |
| Resonance ranking | Query crystal ranks closer to coherent crystal than contradictory crystal |
| Trajectory append | Nudge event appended correctly, prior events unchanged |
| Cache behavior | Second identical query resolves from cache, result identical to first |
| Preflight short-circuit | Strong bank hit bypasses context expansion |
| Anti-crystal | Annihilation score = 1.0 for perfect anti-crystal |
| Schema lock | `phase_conflict_score` and `phase_conflict_traces` present in all responses |
| Frozen crystal | Node/edge add to frozen crystal raises error; trajectory append succeeds |

---

## Appendix A: Intent Classification

The engine classifies incoming queries into intents before routing:

| Intent | Trigger | Action |
|---|---|---|
| `QUERY` | Knowledge question about a known concept | Bank lookup + resonance |
| `TEACH` | New knowledge being provided | Crystallization pipeline |
| `COMPARE` | Explicit comparison between two concepts or crystals | Cross-crystal resonance |
| `TASK` | Symbolic computation (arithmetic, code, logic) | Direct execution |
| `QUERY_AUTOLEARN` | Query that triggered auto-learn consensus | Bank lookup + auto-learn |

Intent classification must not route medical acronym forms (e.g., `COVID-19`,
`COVID19`) to `TASK`. These must remain in `QUERY` unless explicit math syntax
is present in the same query.

---

## Appendix B: Relation Type Registry

Standard relation types recognized by the engine. Custom relation types are
permitted but must be declared in the crystal header `tags` field.

| Relation | Direction | Base Phase | Meaning |
|---|---|---|---|
| `is_a` | source -> target | `pi/6` | Class membership |
| `has_property` | source -> target | `pi/6` | Property attribution |
| `implies` | source -> target | `pi/8` | Logical implication |
| `causes` | source -> target | `pi/4` | Causal relation |
| `supports` | source -> target | `pi/12` | Evidential support |
| `dispels` | source -> target | `0.0` | Active negation |
| `synonym` | bidirectional | `0.0` | Semantic equivalence |
| `antonym` | bidirectional | `pi` | Semantic opposition |
| `hyponym` | source -> target | `pi/2` | Narrower term |
| `domain_relation` | source -> target | `pi/4` | Cross-domain bridge |
| `polyseme` | source -> target | `pi/6` | Same form, different sense |

---

## Appendix C: Changelog

| Version | Date | Changes |
|---|---|---|
| `csif-engine-1.0.0` | 2026-05-17 | Initial engine specification |

---

*This document is part of the Crystal Information Engine (CIE) / CSIF project.*  
*Repository: https://github.com/MoTechnicalities/Crystal-Structure-Information-Format*  
*Read alongside: `CSIF_RWIF_COMPLETE_ARCHITECTURE.md` and `RWIF_CRYSTAL_SCHEMA_V1.md`*  
*This specification is living and will evolve with the project.*
