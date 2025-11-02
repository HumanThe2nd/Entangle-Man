"""
Rendering logic for Pacman game
"""
import pygame
import math
from constants import *


class Renderer:
    """Handles all game rendering"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def render(self, game_state):
        """Render the entire game state"""
        self.screen.fill(BLACK)
        
        # Render each component
        self._render_maze(game_state.maze)
        self._render_pellets(game_state.maze)
        self._render_pacman(game_state.pacman)
        
        for ghost in game_state.ghosts:
            self._render_ghost(ghost)
        
        self._render_ui(game_state)
        
        if game_state.game_over:
            self._render_game_over()
        elif game_state.won:
            self._render_win()
        elif game_state.paused:
            self._render_pause()
        
        pygame.display.flip()
    
    def _render_maze(self, maze):
        """Render the maze walls"""
        for y in range(maze.height):
            for x in range(maze.width):
                tile = maze.get_tile(x, y)
                if tile == WALL:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pos = (x, y)
                    if pos in maze.disappeared_walls:
                        # Fill with black for quantum tunneled wall
                        pygame.draw.rect(self.screen, BLACK, rect)
                        # Draw dashed blue border
                        dash_length = 4
                        for i in range(0, TILE_SIZE, dash_length * 2):
                            # Top border
                            pygame.draw.line(self.screen, BLUE, 
                                (x * TILE_SIZE + i, y * TILE_SIZE),
                                (x * TILE_SIZE + i + dash_length, y * TILE_SIZE))
                            # Bottom border
                            pygame.draw.line(self.screen, BLUE,
                                (x * TILE_SIZE + i, (y + 1) * TILE_SIZE - 1),
                                (x * TILE_SIZE + i + dash_length, (y + 1) * TILE_SIZE - 1))
                            # Left border
                            pygame.draw.line(self.screen, BLUE,
                                (x * TILE_SIZE, y * TILE_SIZE + i),
                                (x * TILE_SIZE, y * TILE_SIZE + i + dash_length))
                            # Right border
                            pygame.draw.line(self.screen, BLUE,
                                ((x + 1) * TILE_SIZE - 1, y * TILE_SIZE + i),
                                ((x + 1) * TILE_SIZE - 1, y * TILE_SIZE + i + dash_length))
                    else:
                        # Normal solid wall
                        pygame.draw.rect(self.screen, BLUE, rect)
    
    def _render_pellets(self, maze):
        """Render pellets and power pellets"""
        # Regular pellets
        for (x, y) in maze.pellets:
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(self.screen, WHITE, (center_x, center_y), 3)
        
        # Power pellets (blinking)
        if pygame.time.get_ticks() % 500 < 250:  # Blink every 500ms
            for (x, y) in maze.power_pellets:
                center_x = x * TILE_SIZE + TILE_SIZE // 2
                center_y = y * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(self.screen, WHITE, (center_x, center_y), 8)
    
    def _render_pacman(self, pacman):
        """Render Pacman with mouth animation"""
        center_x = int(pacman.x)
        center_y = int(pacman.y)
        radius = TILE_SIZE // 2 - 2
        
        # Calculate mouth angle based on direction
        if pacman.direction == RIGHT:
            start_angle = 45
        elif pacman.direction == LEFT:
            start_angle = 225
        elif pacman.direction == UP:
            start_angle = 135
        elif pacman.direction == DOWN:
            start_angle = 315
        else:
            start_angle = 45
        
        # Calculate mouth opening
        mouth_angle = 30 + int(pacman.mouth_open * 15)
        
        # Draw filled circle
        pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), radius)
        
        # Draw black wedge for mouth
        if pacman.mouth_open > 0.1:
            mouth_points = [(center_x, center_y)]
            for angle in range(start_angle + mouth_angle, start_angle - mouth_angle + 360 + 1, -5):
                rad = math.radians(angle)
                point_x = center_x + radius * math.cos(rad)
                point_y = center_y - radius * math.sin(rad)
                mouth_points.append((int(point_x), int(point_y)))
            
            if len(mouth_points) > 2:
                pygame.draw.polygon(self.screen, BLACK, mouth_points)
    
    def _render_ghost(self, ghost):
        """Render a ghost"""
        center_x = int(ghost.x)
        center_y = int(ghost.y)
        radius = TILE_SIZE // 2 - 2
        
        # Choose color based on mode
        if ghost.mode == FRIGHTENED:
            if ghost.frightened_timer < FPS * 2:  # Flash white in last 2 seconds
                color = WHITE if pygame.time.get_ticks() % 400 < 200 else BLUE
            else:
                color = BLUE
        else:
            color = ghost.color
        
        # Draw ghost body (circle for simplicity)
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
        
        # Draw eyes (if not frightened)
        if ghost.mode != FRIGHTENED:
            eye_radius = 3
            eye_offset = 5
            
            # Left eye
            pygame.draw.circle(self.screen, WHITE, 
                             (center_x - eye_offset, center_y - 3), eye_radius)
            pygame.draw.circle(self.screen, BLACK, 
                             (center_x - eye_offset, center_y - 3), 2)
            
            # Right eye
            pygame.draw.circle(self.screen, WHITE, 
                             (center_x + eye_offset, center_y - 3), eye_radius)
            pygame.draw.circle(self.screen, BLACK, 
                             (center_x + eye_offset, center_y - 3), 2)
        else:
            # Draw frightened face
            pygame.draw.circle(self.screen, WHITE, 
                             (center_x - 4, center_y - 2), 2)
            pygame.draw.circle(self.screen, WHITE, 
                             (center_x + 4, center_y - 2), 2)
    
    def _render_ui(self, game_state):
        """Render score, lives, and level"""
        # Score
        score_text = self.font.render(f"Score: {game_state.score}", True, WHITE)
        self.screen.blit(score_text, (10, 5))
        
        # Level
        level_text = self.small_font.render(f"Level: {game_state.level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 120, 10))
        
        # Lives
        lives_text = self.small_font.render("Lives:", True, WHITE)
        self.screen.blit(lives_text, (10, SCREEN_HEIGHT - 30))
        
        for i in range(game_state.pacman.lives):
            x = 80 + i * 30
            y = SCREEN_HEIGHT - 20
            pygame.draw.circle(self.screen, YELLOW, (x, y), 10)
    
    def _render_game_over(self):
        """Render game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        restart_text = self.small_font.render("Press R to Restart", True, WHITE)
        
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def _render_win(self):
        """Render win screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.font.render("LEVEL COMPLETE!", True, YELLOW)
        continue_text = self.small_font.render("Press SPACE to Continue", True, WHITE)
        
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        self.screen.blit(win_text, text_rect)
        self.screen.blit(continue_text, continue_rect)
    
    def _render_pause(self):
        """Render pause screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
