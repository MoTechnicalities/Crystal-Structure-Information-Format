#!/usr/bin/env python3
"""
Portable CPU-only Crystal Bank runtime.

Design goals:
- No GPU dependencies.
- Deterministic JSON export/import with checksum verification.
- Auditable phase geometry for contradiction/coherence checks.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


def wrap_pi(theta: float) -> float:
    return ((theta + math.pi) % (2.0 * math.pi)) - math.pi


def angular_distance(a: float, b: float) -> float:
    return abs(wrap_pi(a - b))


@dataclass
class ClaimEdge:
    subject: str
    relation: str
    object: str
    phase: float
    polarity: str
    source: str
    created_at: float

    def key(self) -> Tuple[str, str, str]:
        return (self.subject, self.relation, self.object)


@dataclass
class Crystal:
    label: str
    edges: List[ClaimEdge] = field(default_factory=list)

    def edge_map(self) -> Dict[Tuple[str, str, str], ClaimEdge]:
        return {edge.key(): edge for edge in self.edges}


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
class CrystalBank:
    name: str
    version: str = "0.1.0"
    relation_base_phases: Dict[str, float] = field(
        default_factory=lambda: {
            "is_a": math.pi / 6.0,
            "has_property": math.pi / 5.0,
            "supports": math.pi / 7.0,
            "causes": math.pi / 4.0,
        }
    )
    crystals: Dict[str, Crystal] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def phase_for(self, relation: str, polarity: str) -> float:
        if relation not in self.relation_base_phases:
            raise ValueError(f"Unknown relation '{relation}'. Add it to relation_base_phases first.")
        base = self.relation_base_phases[relation]
        if polarity not in {"true", "false"}:
            raise ValueError("polarity must be 'true' or 'false'")
        return wrap_pi(base if polarity == "true" else base + math.pi)

    def ensure_crystal(self, label: str) -> Crystal:
        if label not in self.crystals:
            self.crystals[label] = Crystal(label=label)
        return self.crystals[label]

    def add_claim(
        self,
        crystal_label: str,
        subject: str,
        relation: str,
        object_: str,
        polarity: str,
        source: str,
        phase_override: Optional[float] = None,
    ) -> ClaimEdge:
        theta = wrap_pi(phase_override) if phase_override is not None else self.phase_for(relation=relation, polarity=polarity)
        edge = ClaimEdge(
            subject=subject,
            relation=relation,
            object=object_,
            phase=theta,
            polarity=polarity,
            source=source,
            created_at=time.time(),
        )
        crystal = self.ensure_crystal(crystal_label)
        edge_by_key = crystal.edge_map()
        edge_by_key[edge.key()] = edge
        crystal.edges = list(edge_by_key.values())
        self.updated_at = time.time()
        return edge

    def _edge_phase(self, crystal: Crystal, s: str, r: str, o: str) -> Optional[float]:
        edge = crystal.edge_map().get((s, r, o))
        return edge.phase if edge else None

    def resonance_with_query(self, query_edges: Iterable[ClaimEdge], crystal_label: str) -> float:
        if crystal_label not in self.crystals:
            raise KeyError(f"Crystal '{crystal_label}' not found")
        crystal = self.crystals[crystal_label]
        crystal_map = crystal.edge_map()
        score = 0.0
        for query_edge in query_edges:
            crystal_edge = crystal_map.get(query_edge.key())
            if crystal_edge is None:
                score += math.pi
            else:
                score += angular_distance(query_edge.phase, crystal_edge.phase)
        return score

    def query(self, subject: str, relation: str, object_: str, expected_polarity: str) -> List[Tuple[str, float]]:
        query_phase = self.phase_for(relation, expected_polarity)
        query_edge = ClaimEdge(
            subject=subject,
            relation=relation,
            object=object_,
            phase=query_phase,
            polarity=expected_polarity,
            source="query",
            created_at=time.time(),
        )
        scored = []
        for label in sorted(self.crystals):
            score = self.resonance_with_query([query_edge], label)
            scored.append((label, score))
        scored.sort(key=lambda item: item[1])
        return scored

    def triangle_trace(
        self,
        crystal_label: str,
        a: str,
        b: str,
        c: str,
        relation_ab: str,
        relation_bc: str,
        relation_ac: str,
    ) -> ConflictTrace:
        if crystal_label not in self.crystals:
            raise KeyError(f"Crystal '{crystal_label}' not found")
        crystal = self.crystals[crystal_label]

        theta_ab = self._edge_phase(crystal, a, relation_ab, b)
        theta_bc = self._edge_phase(crystal, b, relation_bc, c)
        theta_ac = self._edge_phase(crystal, a, relation_ac, c)
        if None in (theta_ab, theta_bc, theta_ac):
            raise ValueError("Triangle trace requires all three edges to exist in the selected crystal")

        phase_a = wrap_pi(theta_ab + theta_bc)
        phase_b = wrap_pi(theta_ac)
        residual = angular_distance(phase_a, phase_b)

        return ConflictTrace(
            source=a,
            target=c,
            path_a=[f"{a}-[{relation_ab}]->{b}", f"{b}-[{relation_bc}]->{c}"],
            path_b=[f"{a}-[{relation_ac}]->{c}"],
            phase_a=phase_a,
            phase_b=phase_b,
            residual=residual,
        )

    def as_serializable(self) -> Dict:
        return {
            "name": self.name,
            "version": self.version,
            "relation_base_phases": self.relation_base_phases,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "crystals": {
                label: {
                    "label": crystal.label,
                    "edges": [asdict(edge) for edge in sorted(crystal.edges, key=lambda e: (e.subject, e.relation, e.object))],
                }
                for label, crystal in sorted(self.crystals.items(), key=lambda item: item[0])
            },
        }

    @staticmethod
    def _canonical_json(data: Dict) -> str:
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def _checksum_for_payload(payload: Dict) -> str:
        canonical = CrystalBank._canonical_json(payload)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def save(self, path: str) -> str:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        payload = self.as_serializable()
        checksum = self._checksum_for_payload(payload)
        envelope = {
            "format": "csif-crystal-bank",
            "format_version": "1",
            "checksum_sha256": checksum,
            "payload": payload,
        }

        target.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return checksum

    @classmethod
    def load(cls, path: str) -> "CrystalBank":
        src = Path(path)
        envelope = json.loads(src.read_text(encoding="utf-8"))

        if envelope.get("format") != "csif-crystal-bank":
            raise ValueError("Unsupported bank format")

        payload = envelope.get("payload")
        checksum = envelope.get("checksum_sha256")
        actual = cls._checksum_for_payload(payload)
        if checksum != actual:
            raise ValueError("Checksum mismatch: bank file may be corrupted or modified")

        bank = cls(
            name=payload["name"],
            version=payload.get("version", "0.1.0"),
            relation_base_phases=payload.get("relation_base_phases", {}),
            created_at=payload.get("created_at", time.time()),
            updated_at=payload.get("updated_at", time.time()),
        )
        crystals_blob = payload.get("crystals", {})
        for label, crystal_blob in crystals_blob.items():
            crystal = Crystal(label=label)
            for edge_blob in crystal_blob.get("edges", []):
                crystal.edges.append(
                    ClaimEdge(
                        subject=edge_blob["subject"],
                        relation=edge_blob["relation"],
                        object=edge_blob["object"],
                        phase=float(edge_blob["phase"]),
                        polarity=edge_blob["polarity"],
                        source=edge_blob["source"],
                        created_at=float(edge_blob["created_at"]),
                    )
                )
            bank.crystals[label] = crystal
        return bank

    def summary(self) -> Dict:
        edge_count = sum(len(c.edges) for c in self.crystals.values())
        return {
            "name": self.name,
            "version": self.version,
            "crystal_count": len(self.crystals),
            "edge_count": edge_count,
            "relations": sorted(self.relation_base_phases.keys()),
        }
