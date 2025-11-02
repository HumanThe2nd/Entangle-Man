"""
Maze generation and management for Pacman
"""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from constants import *


class Maze:
    """Handles maze layout, pellets, and collision detection"""
    
    def __init__(self):
        self.width = 28
        self.height = 31
        self.layout = self._generate_quantum_layout()
        self.pellets = set()
        self.power_pellets = set()
        self._initialize_pellets()
        self.total_pellets = len(self.pellets) + len(self.power_pellets)
        
    def _quantum_walk(self, steps=10):
        """
        Perform a quantum walk to generate probability distribution.
        Returns a probability distribution over positions.
        """
        # Use 5 qubits for position (can represent 32 positions)
        n_qubits = 5
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Initialize in superposition
        for i in range(n_qubits):
            qc.h(i)
        
        # Apply quantum walk steps
        for _ in range(steps):
            # Apply Hadamard gates (coin operator)
            for i in range(n_qubits):
                qc.h(i)
            
            # Apply conditional shifts (walking operator)
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)
            
            # Add some rotation for variety
            for i in range(n_qubits):
                qc.rz(0.5, i)
        
        # Measure
        qc.measure(range(n_qubits), range(n_qubits))
        
        # Simulate
        simulator = AerSimulator()
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1000).result()
        counts = result.get_counts()
        
        # Convert to probability distribution
        total = sum(counts.values())
        probs = {int(k, 2): v / total for k, v in counts.items()}
        
        return probs
    
    def _generate_quantum_layout(self):
        """Generate a Pacman maze using quantum walk algorithm"""
        # Start with all walls
        layout = [[WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Create border
        for x in range(self.width):
            layout[0][x] = WALL
            layout[self.height - 1][x] = WALL
        for y in range(self.height):
            layout[y][0] = WALL
            layout[y][self.width - 1] = WALL
        
        # Get quantum walk probability distribution
        probs = self._quantum_walk(steps=8)
        
        # Create corridors using quantum walk probabilities
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # Use quantum walk to determine if this should be a path
                position_hash = (x * y + x + y) % 32
                prob = probs.get(position_hash, 0.5)
                
                # Higher probability = more likely to be a path
                if prob > 0.02:  # Threshold for creating paths
                    layout[y][x] = PELLET
        
        # Ensure minimum connectivity - create main corridors
        for y in range(1, self.height - 1):
            # Horizontal corridors
            if y % 5 == 1 or y == self.height // 2:
                for x in range(1, self.width - 1):
                    if layout[y][x] == WALL:
                        layout[y][x] = PELLET
        
        for x in range(1, self.width - 1):
            # Vertical corridors
            if x % 5 == 1 or x == self.width // 2:
                for y in range(1, self.height - 1):
                    if layout[y][x] == WALL:
                        layout[y][x] = PELLET
        
        # Add power pellets in corners
        if layout[3][1] == PELLET:
            layout[3][1] = POWER_PELLET
        if layout[3][self.width - 2] == PELLET:
            layout[3][self.width - 2] = POWER_PELLET
        if layout[self.height - 4][1] == PELLET:
            layout[self.height - 4][1] = POWER_PELLET
        if layout[self.height - 4][self.width - 2] == PELLET:
            layout[self.height - 4][self.width - 2] = POWER_PELLET
        
        # Create ghost house in center
        center_x = self.width // 2
        center_y = self.height // 2
        for dy in range(-2, 3):
            for dx in range(-3, 4):
                y = center_y + dy
                x = center_x + dx
                if 0 < y < self.height - 1 and 0 < x < self.width - 1:
                    if abs(dy) <= 1 and abs(dx) <= 2:
                        layout[y][x] = GHOST_HOUSE
                    else:
                        layout[y][x] = EMPTY
        
        # Create entrance to ghost house
        layout[center_y - 3][center_x] = EMPTY
        layout[center_y - 3][center_x - 1] = EMPTY
        layout[center_y - 3][center_x + 1] = EMPTY
        
        # Ensure Pacman starting position is clear
        pacman_start_y = 23
        pacman_start_x = 14
        if 0 < pacman_start_y < self.height - 1 and 0 < pacman_start_x < self.width - 1:
            layout[pacman_start_y][pacman_start_x] = EMPTY
            # Clear area around Pacman start
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    y = pacman_start_y + dy
                    x = pacman_start_x + dx
                    if 0 < y < self.height - 1 and 0 < x < self.width - 1:
                        if layout[y][x] != GHOST_HOUSE:
                            layout[y][x] = PELLET
        
        return layout
    
    def _initialize_pellets(self):
        """Initialize pellet positions from layout"""
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == PELLET:
                    self.pellets.add((x, y))
                elif self.layout[y][x] == POWER_PELLET:
                    self.power_pellets.add((x, y))
    
    def is_wall(self, x, y):
        """Check if position is a wall"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.layout[y][x] == WALL
    
    def is_valid_position(self, x, y):
        """Check if position is valid (not a wall)"""
        return not self.is_wall(x, y)
    
    def get_tile(self, x, y):
        """Get tile type at position"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return WALL
        return self.layout[y][x]
    
    def eat_pellet(self, x, y):
        """Remove pellet at position if exists, return score"""
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        
        if (grid_x, grid_y) in self.pellets:
            self.pellets.remove((grid_x, grid_y))
            return PELLET_SCORE
        elif (grid_x, grid_y) in self.power_pellets:
            self.power_pellets.remove((grid_x, grid_y))
            return POWER_PELLET_SCORE
        return 0
    
    def is_power_pellet(self, x, y):
        """Check if position has a power pellet"""
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        return (grid_x, grid_y) in self.power_pellets
    
    def all_pellets_eaten(self):
        """Check if all pellets have been eaten"""
        return len(self.pellets) == 0 and len(self.power_pellets) == 0
    
    def reset_pellets(self):
        """Reset all pellets"""
        self.pellets.clear()
        self.power_pellets.clear()
        self._initialize_pellets()
