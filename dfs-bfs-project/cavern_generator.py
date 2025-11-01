"""
Cavern Generator using cellular automata and BFS.
Creates open, organic-feeling cavern systems.
"""
import random
from collections import deque
from map import Map


class CavernGenerator:
    """Generates cavern-style maps using cellular automata and BFS."""
    
    def __init__(self, width, height, wall_probability=0.45, smoothing_iterations=4):
        """
        Initialize the generator.
        
        Args:
            width: Width of the map
            height: Height of the map
            wall_probability: Probability of a cell being a wall initially (0.0-1.0)
            smoothing_iterations: Number of cellular automata smoothing passes
        """
        self.width = width
        self.height = height
        self.wall_probability = wall_probability
        self.smoothing_iterations = smoothing_iterations
    
    def generate(self):
        """
        Generate a cavern map using cellular automata and BFS connectivity.
        
        Returns:
            A Map object with the generated cavern
        """
        game_map = Map(self.width, self.height)
        
        # Step 1: Random seeding
        self._random_seed(game_map)
        
        # Step 2: Smoothing with cellular automata
        for _ in range(self.smoothing_iterations):
            self._smooth(game_map)
        
        # Step 3: Ensure connectivity using BFS
        self._ensure_connectivity(game_map)
        
        return game_map
    
    def _random_seed(self, game_map):
        """Randomly initialize the map with walls and floors."""
        for y in range(1, self.height - 1):  # Keep borders as walls
            for x in range(1, self.width - 1):
                if random.random() > self.wall_probability:
                    game_map.set_cell(x, y, '.')
    
    def _smooth(self, game_map):
        """
        Apply one iteration of cellular automata smoothing.
        
        Rules:
        - If a wall has 4+ floor neighbors, it becomes a floor
        - If a floor has 5+ wall neighbors, it becomes a wall
        """
        # Create a copy of the current state
        new_grid = [row[:] for row in game_map.grid]
        
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                wall_count = game_map.count_wall_neighbors(x, y)
                
                if game_map.is_wall(x, y):
                    # Wall becomes floor if it has 4 or fewer wall neighbors
                    if wall_count <= 4:
                        new_grid[y][x] = '.'
                else:
                    # Floor becomes wall if it has 5 or more wall neighbors
                    if wall_count >= 5:
                        new_grid[y][x] = '#'
        
        # Apply the changes
        game_map.grid = new_grid
    
    def _ensure_connectivity(self, game_map):
        """
        Ensure there's one large connected area using BFS.
        Removes all disconnected smaller caverns.
        """
        # Find all connected components
        visited = set()
        components = []
        
        for y in range(self.height):
            for x in range(self.width):
                if game_map.is_floor(x, y) and (x, y) not in visited:
                    # Start BFS from this floor tile
                    component = self._bfs_component(game_map, x, y, visited)
                    components.append(component)
        
        # Find the largest component
        if not components:
            # No floor tiles found, create a small starting area
            center_x, center_y = self.width // 2, self.height // 2
            game_map.set_cell(center_x, center_y, '.')
            return
        
        largest_component = max(components, key=len)
        
        # Convert all floor tiles not in the largest component to walls
        for y in range(self.height):
            for x in range(self.width):
                if game_map.is_floor(x, y) and (x, y) not in largest_component:
                    game_map.set_cell(x, y, '#')
    
    def _bfs_component(self, game_map, start_x, start_y, visited):
        """
        Find all connected floor tiles using BFS.
        
        Args:
            game_map: The Map object
            start_x, start_y: Starting position
            visited: Set of already visited tiles
        
        Returns:
            Set of tiles in this connected component
        """
        component = set()
        queue = deque([(start_x, start_y)])
        visited.add((start_x, start_y))
        component.add((start_x, start_y))
        
        # 4-directional movement
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            x, y = queue.popleft()
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (game_map.in_bounds(nx, ny) and 
                    game_map.is_floor(nx, ny) and 
                    (nx, ny) not in visited):
                    
                    visited.add((nx, ny))
                    component.add((nx, ny))
                    queue.append((nx, ny))
        
        return component
