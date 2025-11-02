"""
Game constants and configuration for Pacman
"""

# Screen settings
TILE_SIZE = 20
SCREEN_WIDTH = 28 * TILE_SIZE  # Standard Pacman maze is 28x31
SCREEN_HEIGHT = 31 * TILE_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
DARK_BLUE = (33, 33, 222)
LIGHT_BLUE = (100, 100, 255)

# Game settings
PACMAN_SPEED = 2
GHOST_SPEED = 1.5
FRIGHTENED_SPEED = 1
POWER_PELLET_DURATION = 10  # seconds
GHOST_SCORE = 200
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50

# Entity types
WALL = 1
PELLET = 2
POWER_PELLET = 5
EMPTY = 0
GHOST_HOUSE = 4

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
NONE = (0, 0)

# Ghost modes
SCATTER = 0
CHASE = 1
FRIGHTENED = 2
