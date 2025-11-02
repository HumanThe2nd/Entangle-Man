"""
Simple quantum logic for Pacman using random choice to simulate H-gate measurement
"""
import random

def hadamard_measure():
    """
    Simulates measuring a qubit after Hadamard gate.
    Returns:
        1 or 0 with equal probability (simulating H|0⟩ measurement)
    """
    return random.choice([0, 1])