"""
Maze generation and management for Pacman
"""
from constants import *


class Maze:
    """Handles maze layout, pellets, and collision detection"""
    
    def __init__(self):
        self.width = 28
        self.height = 31
        self.layout = self._generate_classic_layout()
        self.pellets = set()
        self.power_pellets = set()
        self._initialize_pellets()
        self.total_pellets = len(self.pellets) + len(self.power_pellets)
        
    def _generate_classic_layout(self):
        """Generate a classic Pacman-style maze layout"""
        # 1 = wall, 0 = empty, 2 = pellet, 3 = power pellet, 4 = ghost house
        layout = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,4,4,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
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
