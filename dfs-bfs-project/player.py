"""
Player class for managing player state.
"""


class Player:
    """Represents the player character in the game."""
    
    def __init__(self, x, y):
        """
        Initialize the player at a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.x = x
        self.y = y
    
    def move(self, dx, dy, game_map):
        """
        Attempt to move the player by a delta.
        
        Args:
            dx: Change in x
            dy: Change in y
            game_map: The Map object to check for collisions
        
        Returns:
            True if the move was successful, False otherwise
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is valid (in bounds and not a wall)
        if game_map.in_bounds(new_x, new_y) and game_map.is_floor(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def get_position(self):
        """Return the player's current position as a tuple."""
        return (self.x, self.y)
