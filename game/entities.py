"""
Entity classes for Pacman game (Pacman and Ghosts)
"""
import random
import math
from constants import *
from pathfinding import get_best_direction


class Entity:
    """Base class for moveable entities"""
    
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = LEFT
        self.next_direction = NONE
        
    def get_grid_pos(self):
        """Get grid position"""
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
    
    def is_at_intersection(self):
        """Check if entity is at a grid intersection"""
        return (self.x % TILE_SIZE < 5 or self.x % TILE_SIZE > TILE_SIZE - 5) and \
               (self.y % TILE_SIZE < 5 or self.y % TILE_SIZE > TILE_SIZE - 5)
    
    def move_left(self, maze, grid_x, grid_y, center_y):
        """Move entity left"""
        next_x = grid_x - 1
        # For ghosts, use for_ghost=True to prevent quantum tunneling
        is_ghost = isinstance(self, Ghost)
        if maze.is_valid_position(next_x, grid_y, for_ghost=is_ghost):
            # Can move freely
            self.x -= self.speed
            self.y = center_y
        else:
            # Only Pacman can try quantum tunneling
            if not is_ghost and maze.try_quantum_tunneling(next_x, grid_y):
                # Wall disappeared, can move now
                self.x -= self.speed
                self.y = center_y
            else:
                # Wall is solid, clamp to current tile center
                target_x = grid_x * TILE_SIZE + TILE_SIZE // 2
                if self.x > target_x:
                    self.x = max(self.x - self.speed, target_x)
                    self.y = center_y
    
    def move_right(self, maze, grid_x, grid_y, center_y):
        """Move entity right"""
        next_x = grid_x + 1
        # For ghosts, use for_ghost=True to prevent quantum tunneling
        is_ghost = isinstance(self, Ghost)
        if maze.is_valid_position(next_x, grid_y, for_ghost=is_ghost):
            # Can move freely
            self.x += self.speed
            self.y = center_y
        else:
            # Only Pacman can try quantum tunneling
            if not is_ghost and maze.try_quantum_tunneling(next_x, grid_y):
                # Wall disappeared, can move now
                self.x += self.speed
                self.y = center_y
            else:
                # Wall is solid, clamp to current tile center
                target_x = grid_x * TILE_SIZE + TILE_SIZE // 2
                if self.x < target_x:
                    self.x = min(self.x + self.speed, target_x)
                    self.y = center_y
    
    def move_up(self, maze, grid_x, grid_y, center_x):
        """Move entity up"""
        next_y = grid_y - 1
        # For ghosts, use for_ghost=True to prevent quantum tunneling
        is_ghost = isinstance(self, Ghost)
        if maze.is_valid_position(grid_x, next_y, for_ghost=is_ghost):
            # Can move freely
            self.y -= self.speed
            self.x = center_x
        else:
            # Only Pacman can try quantum tunneling
            if not is_ghost and maze.try_quantum_tunneling(grid_x, next_y):
                # Wall disappeared, can move now
                self.y -= self.speed
                self.x = center_x
            else:
                # Wall is solid, clamp to current tile center
                target_y = grid_y * TILE_SIZE + TILE_SIZE // 2
                if self.y > target_y:
                    self.y = max(self.y - self.speed, target_y)
                    self.x = center_x
    
    def move_down(self, maze, grid_x, grid_y, center_x):
        """Move entity down"""
        next_y = grid_y + 1
        # For ghosts, use for_ghost=True to prevent quantum tunneling
        is_ghost = isinstance(self, Ghost)
        if maze.is_valid_position(grid_x, next_y, for_ghost=is_ghost):
            # Can move freely
            self.y += self.speed
            self.x = center_x
        else:
            # Only Pacman can try quantum tunneling
            if not is_ghost and maze.try_quantum_tunneling(grid_x, next_y):
                # Wall disappeared, can move now
                self.y += self.speed
                self.x = center_x
            else:
                # Wall is solid, clamp to current tile center
                target_y = grid_y * TILE_SIZE + TILE_SIZE // 2
                if self.y < target_y:
                    self.y = min(self.y + self.speed, target_y)
                    self.x = center_x


class Pacman(Entity):
    """Pacman player character"""
    
    def __init__(self, x, y):
        super().__init__(x, y, PACMAN_SPEED)
        self.lives = 3
        self.mouth_open = 0
        self.mouth_direction = 1
        
    def update(self, maze):
        """Update Pacman position and animation"""
        # Update mouth animation
        self.mouth_open += self.mouth_direction * 0.2
        if self.mouth_open >= 1:
            self.mouth_direction = -1
        elif self.mouth_open <= 0:
            self.mouth_direction = 1
        
        grid_x, grid_y = self.get_grid_pos()
        center_x = grid_x * TILE_SIZE + TILE_SIZE // 2
        center_y = grid_y * TILE_SIZE + TILE_SIZE // 2
        
        # Check if we're aligned with grid center
        aligned_x = abs(self.x - center_x) < 1
        aligned_y = abs(self.y - center_y) < 1
        
        # Try to change direction if requested and at intersection
        if self.next_direction != NONE and aligned_x and aligned_y:
            next_grid_x = grid_x + self.next_direction[0]
            next_grid_y = grid_y + self.next_direction[1]
            
            if maze.is_valid_position(next_grid_x, next_grid_y, for_ghost=False):
                self.direction = self.next_direction
            self.next_direction = NONE
        
        # Try to move in current direction
        if self.direction == LEFT:
            self.move_left(maze, grid_x, grid_y, center_y)
        elif self.direction == RIGHT:
            self.move_right(maze, grid_x, grid_y, center_y)
        elif self.direction == UP:
            self.move_up(maze, grid_x, grid_y, center_x)
        elif self.direction == DOWN:
            self.move_down(maze, grid_x, grid_y, center_x)
        
        # Wrap around screen edges
        if self.x < 0:
            self.x = maze.width * TILE_SIZE
        elif self.x > maze.width * TILE_SIZE:
            self.x = 0
    
    def set_next_direction(self, direction):
        """Set the next direction to move"""
        self.next_direction = direction
    
    def reset_position(self):
        """Reset to starting position"""
        self.x = 14 * TILE_SIZE + TILE_SIZE // 2
        self.y = 23 * TILE_SIZE + TILE_SIZE // 2
        self.direction = NONE
        self.next_direction = NONE


class Ghost(Entity):
    """Ghost enemy character"""
    
    def __init__(self, x, y, color, name, scatter_target):
        super().__init__(x, y, GHOST_SPEED)
        self.color = color
        self.name = name
        self.scatter_target = scatter_target
        self.mode = SCATTER
        self.frightened_timer = 0
        self.start_x = x
        self.start_y = y
        self.target = (0, 0)
        self.decision_timer = 0  # Timer for pathfinding decisions (in frames)
        self.decision_delay = 3  # 0.5 seconds at 60 FPS
        
    def update(self, maze, pacman, ghosts):
        """Update ghost position and behavior"""
        # Update frightened mode timer
        if self.mode == FRIGHTENED:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = SCATTER
        
        # Choose target based on mode
        if self.mode == FRIGHTENED:
            self.target = self._get_random_target(maze)
        elif self.mode == CHASE:
            self.target = self._get_chase_target(pacman, ghosts)
        else:  # SCATTER
            self.target = self.scatter_target
        
        grid_x, grid_y = self.get_grid_pos()
        center_x = grid_x * TILE_SIZE + TILE_SIZE // 2
        center_y = grid_y * TILE_SIZE + TILE_SIZE // 2
        
        speed = FRIGHTENED_SPEED if self.mode == FRIGHTENED else self.speed
        
        # Check if we're at the center of a tile
        at_center = abs(self.x - center_x) <= speed and abs(self.y - center_y) <= speed
        
        if at_center:
            # Decrement decision timer
            self.decision_timer -= 1
            
            # Make a new decision if timer expired
            if self.decision_timer <= 0:
                # Use pathfinding to chase Pacman
                pacman_grid = pacman.get_grid_pos()
                best_direction = get_best_direction(maze, (grid_x, grid_y), pacman_grid, self.direction)
                
                if best_direction:
                    self.direction = best_direction
                
                # Reset timer
                self.decision_timer = self.decision_delay
        
        # Move in current direction using inherited movement methods
        if self.direction == LEFT:
            self.move_left(maze, grid_x, grid_y, center_y)
        elif self.direction == RIGHT:
            self.move_right(maze, grid_x, grid_y, center_y)
        elif self.direction == UP:
            self.move_up(maze, grid_x, grid_y, center_x)
        elif self.direction == DOWN:
            self.move_down(maze, grid_x, grid_y, center_x)
        
        # Wrap around screen edges
        if self.x < 0:
            self.x = maze.width * TILE_SIZE
        elif self.x > maze.width * TILE_SIZE:
            self.x = 0
    
    def _choose_direction(self, maze, grid_x, grid_y):
        """Choose best direction towards target"""
        possible_directions = []
        
        # Check all directions except reverse
        reverse_dir = (-self.direction[0], -self.direction[1])
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if direction == reverse_dir:
                continue
            
            next_x = grid_x + direction[0]
            next_y = grid_y + direction[1]
            
            # Check wall collision specifically for ghost
            next_pos_x = grid_x + direction[0]
            next_pos_y = grid_y + direction[1]
            if not maze.is_wall(next_pos_x, next_pos_y, for_ghost=True):
                # Calculate distance to target
                dist = math.sqrt((next_x - self.target[0])**2 + (next_y - self.target[1])**2)
                possible_directions.append((dist, direction))
        
        if possible_directions:
            # Sort by distance and choose closest
            possible_directions.sort()
            return possible_directions[0][1]
        
        return self.direction
    
    def _get_chase_target(self, pacman, ghosts):
        """Get chase target based on ghost personality"""
        px, py = pacman.get_grid_pos()
        
        if self.name == "Blinky":
            # Red ghost targets Pacman directly
            return (px, py)
        elif self.name == "Pinky":
            # Pink ghost targets 4 tiles ahead of Pacman
            offset_x = pacman.direction[0] * 4
            offset_y = pacman.direction[1] * 4
            return (px + offset_x, py + offset_y)
        elif self.name == "Inky":
            # Blue ghost uses complex targeting
            offset_x = pacman.direction[0] * 2
            offset_y = pacman.direction[1] * 2
            intermediate = (px + offset_x, py + offset_y)
            
            # Find Blinky
            blinky = next((g for g in ghosts if g.name == "Blinky"), None)
            if blinky:
                bx, by = blinky.get_grid_pos()
                target_x = intermediate[0] + (intermediate[0] - bx)
                target_y = intermediate[1] + (intermediate[1] - by)
                return (target_x, target_y)
            return intermediate
        else:  # Clyde
            # Orange ghost targets Pacman if far, scatter if close
            gx, gy = self.get_grid_pos()
            dist = math.sqrt((px - gx)**2 + (py - gy)**2)
            if dist > 8:
                return (px, py)
            else:
                return self.scatter_target
        
    def _get_random_target(self, maze):
        """Get random valid target for frightened mode"""
        return (random.randint(0, maze.width - 1), random.randint(0, maze.height - 1))
    
    def set_frightened(self, duration):
        """Set ghost to frightened mode"""
        if self.mode != FRIGHTENED:
            self.mode = FRIGHTENED
            self.frightened_timer = duration
            # Reverse direction
            self.direction = (-self.direction[0], -self.direction[1])
    
    def reset_position(self):
        """Reset to starting position"""
        self.x = self.start_x
        self.y = self.start_y
        self.direction = UP
        self.mode = SCATTER
        self.frightened_timer = 0
    
    def collides_with(self, pacman):
        """Check collision with Pacman"""
        distance = math.sqrt((self.x - pacman.x)**2 + (self.y - pacman.y)**2)
        return distance < TILE_SIZE * 0.8
