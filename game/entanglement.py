"""
Quantum entanglement manager for Pacman walls
"""
from quantum_logic import hadamard_measure

class EntanglementManager:
    def __init__(self, maze):
        self.maze = maze
        # Cache for storing measurement results 
        # Structure: {(x,y): measurement_result}
        self.measurement_cache = {}
        # Track which walls have been measured and locked
        # Once measured, the result is locked until Pacman moves away
        self.locked_measurements = {}
        
    def get_local_entangled_group(self, x, y):
        """
        Get the immediately adjacent walls (8-directional) that are entangled with (x,y).
        Only returns the LOCAL group (1 tile away), not the entire connected maze.
        This prevents the entire maze from collapsing to one state.
        """
        # Check actual wall status (not the disappeared state)
        if self.maze.layout[y][x] != 1:  # 1 is WALL constant
            return set()
        
        group = {(x, y)}
        
        # Only check the 8 immediately adjacent tiles (no recursion - local entanglement only)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.maze.width and 0 <= next_y < self.maze.height:
                    # Check actual wall status (not the disappeared state)
                    if self.maze.layout[next_y][next_x] == 1:  # 1 is WALL constant
                        group.add((next_x, next_y))
        
        return group
    
    def try_entangled_tunneling(self, x, y):
        """
        Try quantum tunneling, affecting only LOCALLY entangled walls.
        
        QUANTUM SUPERPOSITION & MEASUREMENT:
        Walls exist in quantum superposition until measured.
        Once a wall is measured, the result is LOCKED - you cannot re-measure
        by just holding the button. This prevents "measurement shopping" where
        Pacman keeps trying until getting a favorable result.
        
        The measurement lock is only released when Pacman moves away from the wall,
        allowing it to return to superposition.
        
        QUANTUM ENTANGLEMENT:
        Only the 8 immediately adjacent walls are entangled (local entanglement).
        This prevents the entire maze from collapsing to one quantum state.
        When one wall is measured, only its immediate neighbors share the same fate.
        
        Returns True if the wall allows tunneling (measurement result = 1).
        """
        # Check if this wall already has a locked measurement
        if (x, y) in self.locked_measurements:
            return self.locked_measurements[(x, y)]
        
        # Get the locally entangled group (only immediate neighbors)
        entangled_group = self.get_local_entangled_group(x, y)
        
        if not entangled_group:
            return False
        
        # Perform a NEW quantum measurement for this group
        # This represents preparing a fresh quantum state and measuring it
        measurement_result = hadamard_measure()
        
        # LOCK the result for all walls in the entangled group
        # This prevents re-measuring the same wall by holding against it
        can_tunnel = (measurement_result == 1)
        for wall_x, wall_y in entangled_group:
            self.locked_measurements[(wall_x, wall_y)] = can_tunnel
        
        return can_tunnel
    
    def unlock_walls_far_from_pacman(self, pacman_grid_x, pacman_grid_y):
        """
        Unlock measurements for walls that are not adjacent to Pacman.
        This allows walls to return to superposition when Pacman moves away.
        
        Only walls in the 8 tiles surrounding Pacman remain locked.
        All other walls return to superposition state.
        """
        walls_to_unlock = []
        
        for (wall_x, wall_y) in self.locked_measurements.keys():
            # Calculate distance to Pacman
            dx = abs(wall_x - pacman_grid_x)
            dy = abs(wall_y - pacman_grid_y)
            
            # If wall is more than 1 tile away (not in the 8 surrounding tiles)
            if dx > 1 or dy > 1:
                walls_to_unlock.append((wall_x, wall_y))
        
        # Unlock these walls - they return to superposition
        for wall_pos in walls_to_unlock:
            del self.locked_measurements[wall_pos]
    
    def is_pacman_trapped(self, pacman_grid_x, pacman_grid_y):
        """
        Check if Pacman is completely trapped by walls in all 4 cardinal directions.
        
        Returns True if:
        - All 4 cardinal directions (up, down, left, right) are walls
        - Those walls are all measured as SOLID (not passable)
        
        This represents a quantum trap where Pacman has collapsed into a position
        they cannot escape from.
        """
        # Check all 4 cardinal directions
        directions = [
            (pacman_grid_x, pacman_grid_y - 1),  # Up
            (pacman_grid_x, pacman_grid_y + 1),  # Down
            (pacman_grid_x - 1, pacman_grid_y),  # Left
            (pacman_grid_x + 1, pacman_grid_y),  # Right
        ]
        
        trapped_count = 0
        
        for (check_x, check_y) in directions:
            # Check if out of bounds (counts as trapped)
            if check_x < 0 or check_x >= self.maze.width or check_y < 0 or check_y >= self.maze.height:
                trapped_count += 1
                continue
            
            # Check if it's a wall
            if self.maze.layout[check_y][check_x] == 1:  # 1 is WALL constant
                # Check if the wall is locked as SOLID (not passable)
                if (check_x, check_y) in self.locked_measurements:
                    if not self.locked_measurements[(check_x, check_y)]:
                        # Wall is locked as solid
                        trapped_count += 1
                else:
                    # Wall hasn't been measured yet, not trapped
                    continue
            # If not a wall, Pacman can potentially move there
        
        # Pacman is trapped if all 4 cardinal directions are blocked
        return trapped_count >= 4
