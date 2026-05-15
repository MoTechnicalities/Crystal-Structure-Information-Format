"""
Minimal CSIF crystal with nontrivial phase angles and geometric resonance.
Demonstrates how the medium (phase) changes retrieval/contradiction.
"""
import math
from typing import List, Tuple

class Crystal:
    def __init__(self, nodes: List[str], edges: List[Tuple[int, int, float]]):
        """
        nodes: list of concept names
        edges: list of (from_idx, to_idx, phase_angle_radians)
        """
        self.nodes = nodes
        self.edges = edges  # (from, to, phase)

    def torsion_cycle(self) -> float:
        """
        For a 3-node cycle, sum the phase angles modulo 2pi.
        Returns the net torsion (should be 0 for a flat cycle, nonzero for twisted).
        """
        if len(self.nodes) != 3 or len(self.edges) != 3:
            raise ValueError("This demo only supports 3-node cycles.")
        total_phase = sum(phase for _, _, phase in self.edges)
        return (total_phase + 2*math.pi) % (2*math.pi)

    def resonance_with(self, other: 'Crystal') -> float:
        """
        Compute a simple resonance score: sum of phase differences on matching edges.
        Lower is better (perfect resonance = 0).
        """
        score = 0.0
        for (a_from, a_to, a_phase), (b_from, b_to, b_phase) in zip(self.edges, other.edges):
            if a_from == b_from and a_to == b_to:
                score += abs((a_phase - b_phase + math.pi) % (2*math.pi) - math.pi)
            else:
                score += math.pi  # maximal mismatch
        return score

    def __repr__(self):
        edge_str = ", ".join(f"{self.nodes[f]}{self.nodes[t]} ={p:.2f}" for f, t, p in self.edges)
        return f"Crystal({self.nodes}, [{edge_str}])"

if __name__ == "__main__":
    # Example: Whale  Mammal  Warm-blooded  Whale (cycle)
    nodes = ["Whale", "Mammal", "Warm-blooded"]
    # All phase angles zero: flat storage
    flat = Crystal(nodes, [(0,1,0.0), (1,2,0.0), (2,0,0.0)])
    # Nontrivial phase: WhaleMammal /4, MammalWarm-blooded /2, Warm-bloodedWhale -/3
    geo = Crystal(nodes, [(0,1,math.pi/4), (1,2,math.pi/2), (2,0,-math.pi/3)])