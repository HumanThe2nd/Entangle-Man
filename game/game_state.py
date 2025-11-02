"""
Game state management for Pacman
"""
import pygame
from constants import *
from entities import Pacman, Ghost
from maze import Maze

# Entanglement matrix for ghosts (eaten together)
# Red, Pink, Cyan, Orange
entangle = [[1, 0, 1, 0],[0, 1, 0, 1],[1, 0, 1, 0],[0, 1, 0, 1]]
class GameState:
    """Manages the overall game state"""
    
    def __init__(self):
        self.maze = Maze()
        self.pacman = Pacman(14 * TILE_SIZE + TILE_SIZE // 2, 23 * TILE_SIZE + TILE_SIZE // 2)
        self.ghosts = self._create_ghosts()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.won = False
        self.paused = False
        self.frightened_timer = 0
        self.death_reason = None  # "ghost" or "wall"
        
    def _create_ghosts(self):
        """Create the four ghosts with different personalities"""
        return [
            Ghost(13 * TILE_SIZE + TILE_SIZE // 2, 14 * TILE_SIZE + TILE_SIZE // 2, RED, "Blinky", (25, 0)),
            Ghost(14 * TILE_SIZE + TILE_SIZE // 2, 14 * TILE_SIZE + TILE_SIZE // 2, PINK, "Pinky", (2, 0)),
            Ghost(13 * TILE_SIZE + TILE_SIZE // 2, 15 * TILE_SIZE + TILE_SIZE // 2, CYAN, "Inky", (27, 29)),
            Ghost(14 * TILE_SIZE + TILE_SIZE // 2, 15 * TILE_SIZE + TILE_SIZE // 2, ORANGE, "Clyde", (0, 29)),
        ]
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused or self.won:
            return
        
        # Update Pacman
        self.pacman.update(self.maze)
        
        # Check pellet collection
        score_gained = self.maze.eat_pellet(self.pacman.x, self.pacman.y)
        if score_gained == POWER_PELLET_SCORE:
            # Power pellet eaten, frighten ghosts
            self.frightened_timer = POWER_PELLET_DURATION * FPS
            # First clear any existing entanglements
            for ghost in self.ghosts:
                ghost.set_frightened(self.frightened_timer)
            
            # Randomly pair up ghosts for entanglement
            import random
            frightened_ghosts = [g for g in self.ghosts if g.mode == FRIGHTENED and not g.entangled_with]
            if len(frightened_ghosts) >= 2:
                # Shuffle the list
                random.shuffle(frightened_ghosts)
                # Pair up ghosts
                for i in range(0, len(frightened_ghosts) - 1, 2):
                    frightened_ghosts[i].entangle_with(frightened_ghosts[i + 1])
        
        self.score += score_gained
        
        # Update frightened timer
        if self.frightened_timer > 0:
            self.frightened_timer -= 1

        # Check if any ghost was eaten
        i = 0
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman, self.ghosts)
            
            # Check collision with Pacman
            if ghost.collides_with(self.pacman):
                if ghost.mode == FRIGHTENED:
                    j = 0
                    for ghost2 in self.ghosts:
                        if entangle[i][j]:
                            # Eat ghost
                            self.score += GHOST_SCORE
                            ghost2.reset_position()
                        j += 1
                else:
                    # Pacman dies
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.game_over = True
                        self.death_reason = "ghost"
                    else:
                        self._reset_positions()
            i += 1

        # Check if level complete
        if self.maze.all_pellets_eaten():
            self.won = True
        
        # Update quantum measurement locks based on Pacman's position
        # Walls far from Pacman return to superposition
        self.maze.update_quantum_state(self.pacman.x, self.pacman.y)
        
        # Check if Pacman is trapped by quantum walls
        if not self.game_over:
            pacman_grid_x = int(self.pacman.x // TILE_SIZE)
            pacman_grid_y = int(self.pacman.y // TILE_SIZE)
            if self.maze.entanglement.is_pacman_trapped(pacman_grid_x, pacman_grid_y):
                self.game_over = True
                self.death_reason = "wall"
    
    def _reset_positions(self):
        """Reset entity positions after death"""
        self.pacman.reset_position()
        for ghost in self.ghosts:
            ghost.reset_position()
    
    def reset_game(self):
        """Reset game to initial state"""
        self.maze = Maze()
        self.pacman = Pacman(14 * TILE_SIZE, 23 * TILE_SIZE)
        self.ghosts = self._create_ghosts()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.won = False
        self.frightened_timer = 0
        self.death_reason = None
    
    def next_level(self):
        """Progress to next level"""
        self.level += 1
        self.maze.reset_pellets()
        self._reset_positions()
        self.won = False
        # Increase difficulty
        for ghost in self.ghosts:
            ghost.speed = min(ghost.speed + 0.2, 3.0)
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        # Check all keys independently (last one wins)
        if keys[pygame.K_UP]:
            self.pacman.set_next_direction(UP)
        if keys[pygame.K_DOWN]:
            self.pacman.set_next_direction(DOWN)
        if keys[pygame.K_LEFT]:
            self.pacman.set_next_direction(LEFT)
        if keys[pygame.K_RIGHT]:
            self.pacman.set_next_direction(RIGHT)
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
