#!/usr/bin/env python3
"""
CSIF release showcase sample.

This script demonstrates three release-ready ideas:
1) Coherent vs contradictory phase geometry separation.
2) Auditable path-level contradiction trace output.
3) Tiny cross-language bridge alignment (English <-> Spanish).
"""

import json
import math
from dataclasses import asdict, dataclass
from typing import Dict, List, Sequence, Tuple


def wrap_pi(theta: float) -> float:
    return ((theta + math.pi) % (2.0 * math.pi)) - math.pi


def angular_distance(a: float, b: float) -> float:
    return abs(wrap_pi(a - b))


def compose_phase(path_edges: Sequence[Tuple[str, str]], edge_phases: Dict[Tuple[str, str], float]) -> float:
    return wrap_pi(sum(edge_phases[e] for e in path_edges))


@dataclass
class ConflictTrace:
    source: str
    target: str
    path_a: List[str]
    path_b: List[str]
    phase_a: float
    phase_b: float
    residual: float


@dataclass
class Crystal:
    name: str
    edge_phases: Dict[Tuple[str, str], float]

    def resonance_with(self, other: "Crystal") -> float:
        common = sorted(set(self.edge_phases).intersection(other.edge_phases))
        if not common:
            return math.pi
        return sum(angular_distance(self.edge_phases[e], other.edge_phases[e]) for e in common)


def transitivity_residual(crystal: Crystal, a: str, b: str, c: str) -> float:
    return wrap_pi(crystal.edge_phases[(a, b)] + crystal.edge_phases[(b, c)] - crystal.edge_phases[(a, c)])


def contradiction_trace_for_triangle(crystal: Crystal, a: str, b: str, c: str) -> ConflictTrace:
    path_a_edges = [(a, b), (b, c)]
    path_b_edges = [(a, c)]
    phase_a = compose_phase(path_a_edges, crystal.edge_phases)
    phase_b = compose_phase(path_b_edges, crystal.edge_phases)
    residual = angular_distance(phase_a, phase_b)
    return ConflictTrace(
        source=a,
        target=c,
        path_a=[f"{u}->{v}" for (u, v) in path_a_edges],
        path_b=[f"{u}->{v}" for (u, v) in path_b_edges],
        phase_a=phase_a,
        phase_b=phase_b,
        residual=residual,
    )


def rel_phase(relation: str) -> float:
    table = {
        "is_a": math.pi / 6.0,
    }
    return table[relation]


def build_whale_crystals() -> Tuple[Crystal, Crystal, Crystal]:
    base = rel_phase("is_a")
    coherent_direct = wrap_pi(base + base)
    contradictory_direct = wrap_pi(coherent_direct + math.pi)

    coherent = Crystal(
        name="whale_coherent_en",
        edge_phases={
            ("Whale", "Mammal"): base,
            ("Mammal", "Warm-blooded"): base,
            ("Whale", "Warm-blooded"): coherent_direct,
        },
    )
    contradictory = Crystal(
        name="whale_contradictory_en",
        edge_phases={
            ("Whale", "Mammal"): base,
            ("Mammal", "Warm-blooded"): base,
            ("Whale", "Warm-blooded"): contradictory_direct,
        },
    )
    query = Crystal(
        name="query_en",
        edge_phases={
            ("Whale", "Mammal"): base,
            ("Mammal", "Warm-blooded"): base,
            ("Whale", "Warm-blooded"): coherent_direct,
        },
    )
    return coherent, contradictory, query


def build_spanish_bank() -> Crystal:
    base = rel_phase("is_a")
    coherent_direct = wrap_pi(base + base)
    return Crystal(
        name="whale_coherent_es",
        edge_phases={
            ("Ballena", "Mamifero"): base,
            ("Mamifero", "Sangre-caliente"): base,
            ("Ballena", "Sangre-caliente"): coherent_direct,
        },
    )


def bridge_translate_edges(
    source_edges: Dict[Tuple[str, str], float],
    bridge_map: Dict[str, str],
) -> Dict[Tuple[str, str], float]:
    translated: Dict[Tuple[str, str], float] = {}
    for (u, v), theta in source_edges.items():
        if u in bridge_map and v in bridge_map:
            translated[(bridge_map[u], bridge_map[v])] = theta
    return translated


def main() -> None:
    coherent, contradictory, query = build_whale_crystals()
    trace = contradiction_trace_for_triangle(contradictory, "Whale", "Mammal", "Warm-blooded")

    coherent_residual = transitivity_residual(coherent, "Whale", "Mammal", "Warm-blooded")
    contradictory_residual = transitivity_residual(contradictory, "Whale", "Mammal", "Warm-blooded")

    resonance_coherent = query.resonance_with(coherent)
    resonance_contradictory = query.resonance_with(contradictory)

    spanish_bank = build_spanish_bank()
    bridge = {
        "Whale": "Ballena",
        "Mammal": "Mamifero",
        "Warm-blooded": "Sangre-caliente",
    }
    bridged_query = Crystal(
        name="query_es_via_bridge",
        edge_phases=bridge_translate_edges(query.edge_phases, bridge),
    )
    cross_language_resonance = bridged_query.resonance_with(spanish_bank)

    checks = {
        "coherent_residual_near_zero": abs(coherent_residual) < 1e-9,
        "contradictory_residual_near_pi": abs(abs(contradictory_residual) - math.pi) < 1e-9,
        "query_prefers_coherent": resonance_coherent < resonance_contradictory,
        "trace_residual_near_pi": abs(trace.residual - math.pi) < 1e-9,
        "cross_language_bridge_aligns": cross_language_resonance < 1e-9,
    }

    result = {
        "metrics": {
            "coherent_transitivity_residual": coherent_residual,
            "contradictory_transitivity_residual": contradictory_residual,
            "resonance_query_vs_coherent": resonance_coherent,
            "resonance_query_vs_contradictory": resonance_contradictory,
            "cross_language_resonance": cross_language_resonance,
        },
        "audit_trace": asdict(trace),
        "bridge": {
            "source_language": "en",
            "target_language": "es",
            "mapping": bridge,
        },
        "checks": checks,
    }

    passed = all(checks.values())

    print("=== CSIF Release Showcase ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("RESULT:", "PASS" if passed else "FAIL")


if __name__ == "__main__":
    main()
