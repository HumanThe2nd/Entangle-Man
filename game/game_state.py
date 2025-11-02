"""
Game state management for Pacman
"""
import pygame
from constants import *
from entities import Pacman, Ghost
from maze import Maze


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
            for ghost in self.ghosts:
                ghost.set_frightened(self.frightened_timer)
        
        self.score += score_gained
        
        # Update frightened timer
        if self.frightened_timer > 0:
            self.frightened_timer -= 1

        # Check if any ghost was eaten
        ate = False

        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman, self.ghosts)
            
            # Check collision with Pacman
            if ghost.collides_with(self.pacman):
                if ghost.mode == FRIGHTENED:
                    ate = True
                else:
                    # Pacman dies
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.game_over = True
                    else:
                        self._reset_positions()

        # Superposition -> All ghosts eaten
        if ate:
            for ghost in self.ghosts:
                # Eat ghost
                self.score += GHOST_SCORE
                ghost.reset_position()

        # Check if level complete
        if self.maze.all_pellets_eaten():
            self.won = True
    
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
