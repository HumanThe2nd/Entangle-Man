"""
Quantum logic for Pacman using Qiskit for real quantum simulation
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Initialize the quantum simulator
simulator = AerSimulator()

def hadamard_measure():
    """
    Measures a qubit after applying a Hadamard gate using Qiskit.
    
    QUANTUM MECHANICS JUSTIFICATION:
    Each call creates a new quantum circuit, prepares a fresh qubit in superposition,
    and performs a measurement. This represents a new quantum interaction each time.
    
    In quantum mechanics, measuring a qubit collapses it to a definite state. 
    However, each collision attempt in the game represents preparing a NEW quantum 
    state and measuring it - like repeatedly preparing |0⟩ → H|0⟩ → measure.
    This is why we get probabilistic results on each call, not deterministic ones.
    
    The walls exist in quantum superposition (can be passed through OR solid)
    until Pacman attempts to move through them (observation/measurement).
    Each movement attempt is a new quantum measurement event.
    
    Returns:
        1 or 0 with equal probability (50/50 chance)
        1 = wall disappears (quantum tunneling successful)
        0 = wall stays solid (tunneling failed)
    """
    # Create a quantum circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)
    
    # Apply Hadamard gate to put qubit in superposition: |0⟩ → (|0⟩ + |1⟩)/√2
    qc.h(0)
    
    # Measure the qubit - collapses superposition to definite state
    qc.measure(0, 0)
    
    # Execute the circuit on the simulator
    job = simulator.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    # Return the measured value (0 or 1)
    return int(list(counts.keys())[0])