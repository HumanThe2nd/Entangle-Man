"""
Main game loop for Pacman
"""
import pygame
import sys
import maze
import time
from constants import *
from game_state import GameState
from renderer import Renderer


def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()
    last_time = time.time()
    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    
    # Create game objects
    clock = pygame.time.Clock()
    game_state = GameState()
    renderer = Renderer(screen)
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    game_state.toggle_pause()
                elif event.key == pygame.K_r and game_state.game_over:
                    game_state.reset_game()
                elif event.key == pygame.K_SPACE and game_state.won:
                    game_state.next_level()
        
        # Handle continuous input
        keys = pygame.key.get_pressed()
        game_state.handle_input(keys)
        

        # Update wall
        cur_time = time.time()
        if cur_time - last_time > 5:
            game_state.maze.reset_all_walls()
            last_time = cur_time
        
        # Update game state
        game_state.update()
        
        # Render
        renderer.render(game_state)
        
        # Control frame rate
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
