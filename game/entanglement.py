"""
Quantum entanglement manager for Pacman walls
"""
from quantum_logic import hadamard_measure

class EntanglementManager:
    def __init__(self, maze):
        self.maze = maze
        self.wall_groups = []
        self._find_wall_groups()
        
    def _find_wall_groups(self):
        """Find connected groups of walls using recursion"""
        visited = set()
        
        def find_connected_walls(x, y):
            """Recursively find all walls connected to (x,y)"""
            if (x, y) in visited or not self.maze.is_wall(x, y):
                return set()
                
            group = {(x, y)}
            visited.add((x, y))
            
            # Check all adjacent positions
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.maze.width and 0 <= next_y < self.maze.height:
                    connected = find_connected_walls(next_x, next_y)
                    group.update(connected)
            
            return group
        
        # Find all wall groups
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (x, y) not in visited and self.maze.is_wall(x, y):
                    group = find_connected_walls(x, y)
                    if len(group) > 1:  # Only store groups of 2 or more walls
                        self.wall_groups.append(group)
    
    def try_entangled_tunneling(self, x, y):
        """
        Try quantum tunneling, affecting all entangled walls in the group.
        Returns True if the walls should disappear.
        """
        # Find which group contains this wall
        target_group = None
        for group in self.wall_groups:
            if (x, y) in group:
                target_group = group
                break
        
        if not target_group:
            return False
            
        # Apply single Hadamard measurement for the entire group
        if hadamard_measure() == 1:
            # Make all walls in the group disappear
            for wall_x, wall_y in target_group:
                self.maze.disappeared_walls.add((wall_x, wall_y))
            return True
            
        return False
    
    def reset_wall_group(self, x, y):
        """Reset entire group of walls that contains (x,y)"""
        # Find which group contains this wall
        for group in self.wall_groups:
            if (x, y) in group:
                self.maze.disappeared_walls.difference_update(group)
                break