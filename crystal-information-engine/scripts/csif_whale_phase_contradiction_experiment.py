"""
Experiment script for validating phase angles distinguishing coherent and contradictory crystals.
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

# Define nodes and edges for the experiment
nodes = ["Whale", "Mammal", "Warm-blooded"]

# Coherent crystal
coherent_edges = [
    (0, 1, 0.0),  # Whale -> Mammal
    (1, 2, 0.0),  # Mammal -> Warm-blooded
    (0, 2, 0.0)   # Whale -> Warm-blooded
]
coherent_crystal = Crystal(nodes, coherent_edges)

# Contradictory crystal
contradictory_edges = [
    (0, 1, 0.0),  # Whale -> Mammal
    (1, 2, 0.0),  # Mammal -> Warm-blooded
    (0, 2, math.pi)  # Whale -> Warm-blooded (anti-phase)
]
contradictory_crystal = Crystal(nodes, contradictory_edges)

# Query crystal
query_edges = [
    (0, 1, 0.0),  # Whale -> Mammal
    (1, 2, 0.0),  # Mammal -> Warm-blooded
    (0, 2, 0.0)   # Whale -> Warm-blooded
]
query_crystal = Crystal(nodes, query_edges)

# Measure resonance
coherent_resonance = query_crystal.resonance_with(coherent_crystal)
contradictory_resonance = query_crystal.resonance_with(contradictory_crystal)

print("Resonance with coherent crystal:", coherent_resonance)
print("Resonance with contradictory crystal:", contradictory_resonance)