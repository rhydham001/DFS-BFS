"""
Development Guide and Algorithm Explanation
The Labyrinth of Chaos
"""

# ============================================================
# PHASE 1: GAME WORLD FOUNDATION
# ============================================================

"""
MAP REPRESENTATION
------------------
The Map class uses a 2D list (list of lists) where:
- Each element represents a cell in the grid
- '#' = Wall (impassable)
- '.' = Floor (walkable)
- '@' = Player (rendered during display)
- '>' = Exit (rendered during display)

The grid can be thought of as an implicit graph:
- Nodes: Floor tiles
- Edges: Adjacency between floor tiles (up/down/left/right)

Key Methods:
- set_cell(x, y, char): Modify a cell
- get_cell(x, y): Read a cell
- is_floor(x, y): Check if walkable
- render(): Display map to console
- get_all_floor_tiles(): Return list of walkable positions
- count_wall_neighbors(x, y): Count adjacent walls (for cellular automata)
"""

# ============================================================
# PHASE 2: DUNGEON GENERATOR (DFS)
# ============================================================

"""
ALGORITHM: Randomized Iterative Depth-First Search
---------------------------------------------------

Concept:
DFS explores as far as possible along each branch before backtracking.
In maze generation, this creates long, winding corridors with minimal loops.

Implementation Details:

1. INITIALIZATION:
   - Start with a grid completely filled with walls
   - Choose a random starting cell (must be on odd coordinates)
   - Mark it as floor and push to stack
   
2. MAIN LOOP (while stack is not empty):
   a. Peek at current cell (don't pop yet)
   
   b. Find unvisited neighbors TWO cells away:
      - We move 2 cells at a time to leave walls between corridors
      - Check all 4 directions: up, down, left, right
      - Only consider cells that are still walls
   
   c. If valid neighbors exist:
      i.   Choose one randomly
      ii.  Carve the neighbor cell (set to floor)
      iii. Carve the cell IN-BETWEEN (creates the corridor)
      iv.  Mark neighbor as visited
      v.   Push neighbor onto stack
   
   d. If no valid neighbors (dead end):
      i. Pop from stack (BACKTRACK)
      ii. Continue with previous cell

Data Structure: Stack (Python list)
- Push: stack.append(item)
- Pop: stack.pop()
- Peek: stack[-1]

Why odd coordinates?
- Moving 2 cells at a time: (1,1) -> (3,1) -> (5,1)
- Ensures walls remain between corridors
- Creates grid-aligned passages

Result Characteristics:
- Long, twisty corridors
- Few loops/cycles
- Many dead ends
- Low openness score
- Classic "dungeon crawler" feel
"""

# Example trace:
"""
Starting grid (5x5):
#####
#####
#####
#####
#####

After starting at (1,1):
#####
#.###
#####
#####
#####

Carve to (1,3):
#####
#.###
#.###
#.###
#####

Carve to (3,3):
#####
#.###
#.###
#...#
#####

... and so on with random choices and backtracking
"""

# ============================================================
# PHASE 3: CAVERN GENERATOR (BFS)
# ============================================================

"""
ALGORITHM: Cellular Automata + BFS Connectivity
------------------------------------------------

This is a multi-stage process that combines randomness, simulation,
and graph traversal.

STAGE 1: RANDOM SEEDING
- Iterate through entire grid
- Each cell has a probability of being a wall (e.g., 45%)
- Creates a noisy, random starting pattern
- Keep outer borders as walls for containment

STAGE 2: CELLULAR AUTOMATA SMOOTHING
- Simulate 3-4 iterations of rules-based evolution
- For each cell, count its wall neighbors in a 3x3 area
- Apply rules:
  * If WALL and 4 or fewer wall neighbors → becomes FLOOR
  * If FLOOR and 5 or more wall neighbors → becomes WALL
- This creates natural-looking cave formations
- Smooths out noise into organic shapes

Why these rules?
- Walls in open areas tend to erode away
- Isolated floor tiles in wall areas get filled in
- Creates clustering and natural boundaries

STAGE 3: CONNECTIVITY CLEANUP (BFS)
Problem: After smoothing, we may have multiple disconnected cave systems

Solution: Use BFS to find connected components
1. Iterate through all floor tiles
2. For each unvisited floor tile, start a BFS to find its component:
   a. Initialize queue with starting tile
   b. Mark as visited
   c. While queue not empty:
      - Dequeue current tile
      - Check all 4 neighbors
      - If neighbor is floor and unvisited:
        * Mark as visited
        * Add to component set
        * Enqueue neighbor

3. Track the size of each component found
4. Identify the LARGEST component
5. Convert all floor tiles NOT in largest component → walls

Data Structure: Queue (collections.deque)
- Enqueue: queue.append(item)
- Dequeue: queue.popleft()

Why BFS for connectivity?
- Explores level-by-level from source
- Naturally finds all reachable nodes
- Efficient for connected component detection

Result Characteristics:
- Open, spacious areas
- Organic, natural-looking shapes
- Single connected playable area
- Higher openness score
- Cave/cavern feel
"""

# Example cellular automata evolution:
"""
Initial random (45% wall):
.#.##
#..#.
.###.
..#..
#.#.#

After smoothing iteration 1:
.....
.##..
.###.
..#..
..#..

After smoothing iteration 2:
.....
.##..
.##..
.....
.....
"""

# ============================================================
# PHASE 4: GAME CONTROLLER
# ============================================================

"""
GAME LOOP STRUCTURE
-------------------

1. INITIALIZATION:
   - Welcome screen
   - Map type selection (dungeon/cavern)
   - AI Director option
   - Map generation
   - Player and exit placement

2. MAIN GAME LOOP:
   while not (player_at_exit or quit):
       a. Clear screen
       b. Render map with player (@) and exit (>)
       c. Display controls and status
       d. Get user input (WASD or Q)
       e. Process input:
          - Movement: Check collision, update position
          - Quit: Exit game
       f. Check win condition

3. WIN CONDITION:
   - Player position == Exit position
   - Display victory message

COLLISION DETECTION:
- Before moving, check destination cell
- If floor: allow movement
- If wall: reject movement (no position update)

INPUT HANDLING:
- W/Up: dy = -1 (move up)
- S/Down: dy = +1 (move down)
- A/Left: dx = -1 (move left)
- D/Right: dx = +1 (move right)
- Q: quit game
"""

# ============================================================
# PHASE 5: AI DIRECTOR (EXTENSION)
# ============================================================

"""
AI DIRECTOR FEATURES
--------------------

The AI Director analyzes generated maps and makes intelligent decisions
about game design and difficulty.

METRIC 1: PATH COMPLEXITY
Algorithm: BFS Shortest Path
- Start BFS from player position
- Track distance to each reachable tile
- Return distance to exit tile
- This represents minimum steps needed to win
- Higher = more complex/difficult

Implementation:
- Queue stores (x, y, distance) tuples
- Visit each tile at most once
- Level-by-level exploration guarantees shortest path

METRIC 2: DEAD END COUNT
Algorithm: Neighbor Counting
- For each floor tile, count floor neighbors
- If exactly 1 floor neighbor: it's a dead end
- Dead ends increase exploration difficulty
- More dead ends = more backtracking needed

METRIC 3: OPENNESS SCORE
Algorithm: Simple Ratio
- Count total floor tiles
- Count total tiles (width × height)
- Openness = (floors / total) × 100
- Higher = more open, less constrained movement

STRATEGIC EXIT PLACEMENT
Algorithm: Distance-Based BFS
1. Start BFS from player position
2. Track distance to all reachable tiles
3. Filter tiles that are >= minimum distance away
4. Randomly choose from filtered tiles
5. Ensures exit is not too close (boring) or impossible (broken map)

Why use BFS for shortest path?
- BFS explores level-by-level (all dist 1, then all dist 2, etc.)
- First time we reach goal = shortest path
- Contrast with DFS which explores deeply but not necessarily shortest

Benefits:
- Adaptive difficulty
- Fair but challenging placement
- Quantitative map analysis
- Data-driven game design
"""

# Example BFS distance map:
"""
Player at (1, 1):

  0 1 2 3 4
0 # # # # #
1 # @ . . #
2 # . # . #
3 # . . . #
4 # # # # #

Distance map:
  0 1 2 3 4
0 # # # # #
1 # 0 1 2 #
2 # 1 # 3 #
3 # 2 3 4 #
4 # # # # #

Tiles at distance >= 3: (3,1), (3,2), (3,3)
Strategic exit placement: choose from these
"""

# ============================================================
# DATA STRUCTURES SUMMARY
# ============================================================

"""
STACK (DFS):
- LIFO: Last In, First Out
- Operations: push, pop, peek
- Use case: Backtracking, depth-first exploration
- Implementation: Python list
- Time complexity: O(1) for all operations

QUEUE (BFS):
- FIFO: First In, First Out
- Operations: enqueue, dequeue
- Use case: Level-order traversal, shortest path
- Implementation: collections.deque
- Time complexity: O(1) for all operations

2D ARRAY (MAP):
- Grid representation
- Random access: O(1)
- Space: O(width × height)
- Use case: Spatial data, game worlds

SET (VISITED TRACKING):
- Fast membership testing: O(1)
- No duplicates
- Use case: Tracking visited nodes in graph traversal
"""

# ============================================================
# OBJECT-ORIENTED DESIGN
# ============================================================

"""
CLASS STRUCTURE:

Map
├── Grid storage (2D list)
├── Cell manipulation methods
├── Rendering logic
└── Spatial queries

Player
├── Position (x, y)
└── Movement with collision detection

DungeonGenerator
├── Map dimensions
└── generate() -> Map (using DFS)

CavernGenerator
├── Map dimensions
├── Automata parameters
└── generate() -> Map (using CA + BFS)

AIDirector
├── Map reference
├── Shortest path calculation (BFS)
├── Metric computation
└── Strategic placement

Game
├── Map, Player, Exit
├── Game loop
├── Input handling
└── Win condition checking

Benefits of OOP:
- Separation of concerns
- Reusable components
- Easy to extend (new generators, new metrics)
- Clean interfaces between modules
"""

# ============================================================
# ALGORITHM COMPARISON
# ============================================================

"""
DFS vs BFS IN THIS PROJECT:

DFS (Dungeon Generation):
✓ Creates maze-like structures
✓ Memory efficient (only stack depth)
✓ Good for: puzzles, exploration challenges
✗ Not guaranteed shortest path
✗ Can create very long corridors

BFS (Cavern Analysis):
✓ Finds shortest paths
✓ Level-by-level exploration
✓ Good for: distance calculations, connectivity
✗ More memory usage (queue can be large)
✗ Explores all nearby nodes before distant ones

Time Complexity:
- Both: O(V + E) where V = vertices, E = edges
- In grid: V = width × height, E ≈ 4V
- Practical: O(width × height)

Space Complexity:
- DFS: O(max_depth) ≈ O(width × height) worst case
- BFS: O(max_width) ≈ O(width × height) worst case
- In practice: Both acceptable for game-sized grids
"""

# ============================================================
# TESTING AND VALIDATION
# ============================================================

"""
HOW TO TEST:

1. Visual Inspection:
   - Run demo.py to see generated maps
   - Check for desired characteristics
   - Verify connectivity (no isolated areas)

2. Algorithmic Verification:
   - DFS: Check stack behavior, backtracking
   - BFS: Verify shortest paths, connectivity
   - Metrics: Validate calculations

3. Edge Cases:
   - Very small maps (5x5)
   - Very large maps (101x101)
   - Different wall probabilities
   - Different smoothing iterations

4. Gameplay Testing:
   - Can player reach exit?
   - Is difficulty appropriate?
   - Are controls responsive?
   - Do metrics make sense?

5. Code Quality:
   - Run with different random seeds
   - Check error handling
   - Verify bounds checking
   - Test collision detection
"""

# ============================================================
# EXTENSIONS AND IMPROVEMENTS
# ============================================================

"""
POSSIBLE ENHANCEMENTS:

1. Multiple Floors/Levels:
   - Generate sequence of maps
   - Increase difficulty per level
   - Stairs up/down

2. Enemies with Pathfinding:
   - Use BFS for enemy AI
   - Chase player or patrol
   - Combat system

3. Items and Inventory:
   - Keys and locked doors
   - Potions, weapons, treasure
   - Puzzle elements

4. Fog of War:
   - Only show tiles near player
   - Exploration mechanic
   - Memory of visited areas

5. Better Visualization:
   - Colors (using colorama)
   - Better ASCII art
   - Mini-map

6. Procedural Difficulty Scaling:
   - AI Director adjusts parameters
   - Learn from player behavior
   - Adaptive challenge

7. Save/Load System:
   - Serialize game state
   - Resume later
   - Leaderboard

8. Multiple Exit Strategy:
   - Collect keys before exit
   - Multiple objectives
   - Branching paths

9. Room-Based Generation:
   - Combine rooms with corridors
   - Special room types
   - Boss rooms

10. Hybrid Algorithms:
    - Combine DFS and BFS
    - Different areas with different styles
    - Transition zones
"""

print(__doc__)
