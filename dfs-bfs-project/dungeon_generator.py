"""
Dungeon Generator using randomized iterative DFS.
Creates maps with long, winding corridors.
"""
import random
from map import Map


class DungeonGenerator:
    """Generates dungeon-style maps using DFS traversal."""
    
    def __init__(self, width, height):
        """
        Initialize the generator.
        
        Args:
            width: Width of the map (should be odd)
            height: Height of the map (should be odd)
        """
        # Ensure dimensions are odd for proper corridor generation
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
    
    def generate(self):
        """
        Generate a dungeon map using randomized iterative DFS.
        
        Returns:
            A Map object with the generated dungeon
        """
        game_map = Map(self.width, self.height)
        
        # Choose a random starting cell (must be on odd coordinates)
        start_x = random.randrange(1, self.width - 1, 2)
        start_y = random.randrange(1, self.height - 1, 2)
        
        # Stack for DFS
        stack = [(start_x, start_y)]
        visited = set()
        visited.add((start_x, start_y))
        game_map.set_cell(start_x, start_y, '.')
        
        # Directions: up, down, left, right (moving 2 cells at a time)
        directions = [
            (0, -2),  # Up
            (0, 2),   # Down
            (-2, 0),  # Left
            (2, 0)    # Right
        ]
        
        while stack:
            current_x, current_y = stack[-1]  # Peek at top of stack
            
            # Find all valid unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                
                # Check if neighbor is in bounds and unvisited
                if (game_map.in_bounds(nx, ny) and 
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Choose a random neighbor
                nx, ny, dx, dy = random.choice(neighbors)
                
                # Carve a path to the neighbor
                # First, carve the cell in between
                mid_x = current_x + dx // 2
                mid_y = current_y + dy // 2
                game_map.set_cell(mid_x, mid_y, '.')
                
                # Then carve the neighbor cell
                game_map.set_cell(nx, ny, '.')
                
                # Mark as visited and push to stack
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # No unvisited neighbors, backtrack
                stack.pop()
        
        return game_map
