"""
Pathfinding algorithms for ghost AI
"""
from collections import deque
from constants import UP, DOWN, LEFT, RIGHT


def bfs_find_path(maze, start_pos, target_pos):
    """
    Use BFS to find the shortest path from start to target.
    Returns the first direction to take.
    
    Args:
        maze: The maze object
        start_pos: Tuple (x, y) of starting grid position
        target_pos: Tuple (x, y) of target grid position
    
    Returns:
        Direction tuple (dx, dy) or None if no path found
    """
    start_x, start_y = start_pos
    target_x, target_y = target_pos
    
    # BFS queue: (x, y, path)
    queue = deque([(start_x, start_y, [])])
    visited = {(start_x, start_y)}
    
    directions = [UP, DOWN, LEFT, RIGHT]
    
    while queue:
        x, y, path = queue.popleft()
        
        # Found target
        if (x, y) == (target_x, target_y):
            if path:
                return path[0]  # Return first direction in path
            return None
        
        # Explore neighbors
        for direction in directions:
            dx, dy = direction
            next_x = x + dx
            next_y = y + dy
            
            if (next_x, next_y) not in visited and maze.is_valid_position(next_x, next_y):
                visited.add((next_x, next_y))
                queue.append((next_x, next_y, path + [direction]))
    
    return None  # No path found


def get_best_direction(maze, current_pos, target_pos, current_direction):
    """
    Get the best direction to move towards target using pathfinding.
    Avoids reversing direction unless necessary.
    
    Args:
        maze: The maze object
        current_pos: Tuple (x, y) of current grid position
        target_pos: Tuple (x, y) of target grid position
        current_direction: Current direction tuple (dx, dy)
    
    Returns:
        Best direction tuple (dx, dy)
    """
    # First try pathfinding
    best_dir = bfs_find_path(maze, current_pos, target_pos)
    
    if best_dir:
        # Avoid reversing direction unless it's the only option
        reverse_dir = (-current_direction[0], -current_direction[1])
        if best_dir != reverse_dir:
            return best_dir
        
        # Check if there are other valid directions
        x, y = current_pos
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if direction != reverse_dir:
                next_x = x + direction[0]
                next_y = y + direction[1]
                if maze.is_valid_position(next_x, next_y):
                    return direction
        
        # No choice but to reverse
        return best_dir
    
    # No path found, try any valid direction
    x, y = current_pos
    reverse_dir = (-current_direction[0], -current_direction[1])
    
    for direction in [UP, DOWN, LEFT, RIGHT]:
        if direction != reverse_dir:
            next_x = x + direction[0]
            next_y = y + direction[1]
            if maze.is_valid_position(next_x, next_y):
                return direction
    
    # Last resort: reverse
    return reverse_dir
