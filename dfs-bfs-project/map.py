"""
Map class for representing the game world.
"""
import os
import sys


class Map:
    """Represents a 2D grid-based game map."""
    
    def __init__(self, width, height):
        """
        Initialize a map filled with walls.
        
        Args:
            width: Width of the map
            height: Height of the map
        """
        self.width = width
        self.height = height
        self.grid = [['#' for _ in range(width)] for _ in range(height)]
    
    def set_cell(self, x, y, char):
        """Set a cell to a specific character."""
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x] = char
    
    def get_cell(self, x, y):
        """Get the character at a specific cell."""
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return '#'
    
    def is_floor(self, x, y):
        """Check if a cell is a floor tile."""
        return self.get_cell(x, y) == '.'
    
    def is_wall(self, x, y):
        """Check if a cell is a wall."""
        return self.get_cell(x, y) == '#'
    
    def in_bounds(self, x, y):
        """Check if coordinates are within map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, player_x=None, player_y=None, exit_x=None, exit_y=None):
        """
        Render the map to the console.
        
        Args:
            player_x, player_y: Player position (optional)
            exit_x, exit_y: Exit position (optional)
        """
        # Clear the console
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        
        # Print the map
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                # Check if this is the player position
                if player_x is not None and player_y is not None and x == player_x and y == player_y:
                    row += '@'
                # Check if this is the exit position
                elif exit_x is not None and exit_y is not None and x == exit_x and y == exit_y:
                    row += '>'
                else:
                    row += self.grid[y][x]
            print(row)
        print()  # Extra newline for spacing
    
    def get_all_floor_tiles(self):
        """Return a list of all floor tile coordinates."""
        floor_tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.is_floor(x, y):
                    floor_tiles.append((x, y))
        return floor_tiles
    
    def count_wall_neighbors(self, x, y, radius=1):
        """
        Count the number of wall neighbors around a cell.
        
        Args:
            x, y: Cell coordinates
            radius: Search radius (default 1 for 3x3 area)
        
        Returns:
            Number of wall neighbors
        """
        wall_count = 0
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                # Treat out-of-bounds as walls
                if not self.in_bounds(nx, ny) or self.is_wall(nx, ny):
                    wall_count += 1
        return wall_count
