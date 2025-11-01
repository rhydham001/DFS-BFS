"""
AI Director for analyzing generated maps and making intelligent decisions.
"""
from collections import deque


class AIDirector:
    """Analyzes maps and provides metrics and strategic placements."""
    
    def __init__(self, game_map):
        """
        Initialize the AI Director with a map.
        
        Args:
            game_map: The Map object to analyze
        """
        self.game_map = game_map
    
    def calculate_shortest_path(self, start_x, start_y, end_x, end_y):
        """
        Calculate the shortest path between two points using BFS.
        
        Args:
            start_x, start_y: Starting position
            end_x, end_y: Ending position
        
        Returns:
            Length of the shortest path, or -1 if no path exists
        """
        if not self.game_map.is_floor(start_x, start_y) or not self.game_map.is_floor(end_x, end_y):
            return -1
        
        visited = set()
        queue = deque([(start_x, start_y, 0)])  # (x, y, distance)
        visited.add((start_x, start_y))
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            x, y, dist = queue.popleft()
            
            if x == end_x and y == end_y:
                return dist
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (self.game_map.in_bounds(nx, ny) and 
                    self.game_map.is_floor(nx, ny) and 
                    (nx, ny) not in visited):
                    
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))
        
        return -1  # No path found
    
    def count_dead_ends(self):
        """
        Count the number of dead-end tiles (floor tiles with only one exit).
        
        Returns:
            Number of dead-end tiles
        """
        dead_end_count = 0
        
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                if self.game_map.is_floor(x, y):
                    # Count floor neighbors
                    floor_neighbors = 0
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if self.game_map.in_bounds(nx, ny) and self.game_map.is_floor(nx, ny):
                            floor_neighbors += 1
                    
                    # A dead end has only one floor neighbor
                    if floor_neighbors == 1:
                        dead_end_count += 1
        
        return dead_end_count
    
    def calculate_openness_score(self):
        """
        Calculate the openness score (ratio of floor to total tiles).
        
        Returns:
            Openness score as a percentage (0-100)
        """
        floor_count = len(self.game_map.get_all_floor_tiles())
        total_tiles = self.game_map.width * self.game_map.height
        
        if total_tiles == 0:
            return 0.0
        
        return (floor_count / total_tiles) * 100
    
    def find_strategic_exit_position(self, player_x, player_y, min_distance=15):
        """
        Find a strategic position for the exit that's far from the player.
        
        Args:
            player_x, player_y: Player's starting position
            min_distance: Minimum distance from player to exit
        
        Returns:
            (x, y) tuple for exit position, or None if no suitable position found
        """
        # Use BFS to find all reachable tiles and their distances
        visited = {}  # Maps (x, y) -> distance
        queue = deque([(player_x, player_y, 0)])
        visited[(player_x, player_y)] = 0
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            x, y, dist = queue.popleft()
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (self.game_map.in_bounds(nx, ny) and 
                    self.game_map.is_floor(nx, ny) and 
                    (nx, ny) not in visited):
                    
                    visited[(nx, ny)] = dist + 1
                    queue.append((nx, ny, dist + 1))
        
        # Find all tiles that are at least min_distance away
        far_tiles = [(x, y) for (x, y), dist in visited.items() if dist >= min_distance]
        
        if not far_tiles:
            # If no tiles are far enough, just use the farthest available
            if visited:
                farthest = max(visited.items(), key=lambda item: item[1])
                return farthest[0]
            return None
        
        # Return a random far tile
        import random
        return random.choice(far_tiles)
    
    def analyze_map(self, player_x, player_y, exit_x, exit_y):
        """
        Analyze the map and return all metrics.
        
        Args:
            player_x, player_y: Player position
            exit_x, exit_y: Exit position
        
        Returns:
            Dictionary containing all metrics
        """
        path_length = self.calculate_shortest_path(player_x, player_y, exit_x, exit_y)
        dead_ends = self.count_dead_ends()
        openness = self.calculate_openness_score()
        
        return {
            'path_complexity': path_length,
            'dead_ends': dead_ends,
            'openness': openness
        }
