import tkinter as tk
from tkinter import messagebox, ttk
import random

from player import Player
from dungeon_generator import DungeonGenerator
from cavern_generator import CavernGenerator
from ai_director import AIDirector


class GameGUI(tk.Tk):
    """Tkinter based GUI for The Labyrinth of Chaos."""

    # Default cell size; will be adjusted to fit the screen
    DEFAULT_CELL_SIZE = 20
    CELL_SIZE = DEFAULT_CELL_SIZE

    def __init__(self, width=51, height=31):
        super().__init__()
        self.title("The Labyrinth of Chaos")
        # Allow window resizing; canvas will provide scrollbars if needed
        self.resizable(True, True)
        self.width = width
        self.height = height
        self.game_map = None
        self.player = None
        self.exit_x = None
        self.exit_y = None
        self.use_ai_director = False
        self.map_type = "dungeon"  # default

        # Adjust cell size based on screen dimensions before creating canvas
        self._adjust_cell_size()
        
        # Set window size based on map size and cell size
        window_width = max(self.width * self.CELL_SIZE + 40, 800)
        window_height = max(self.height * self.CELL_SIZE + 100, 600)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        # Ensure window doesn't exceed screen bounds
        window_width = min(window_width, int(screen_w * 0.95))
        window_height = min(window_height, int(screen_h * 0.95))
        
        # Center window on screen
        x = (screen_w - window_width) // 2
        y = (screen_h - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # UI elements
        self._create_controls()
        # Frame to hold canvas and scrollbars
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Canvas for drawing the map
        canvas_width = self.width * self.CELL_SIZE
        canvas_height = self.height * self.CELL_SIZE
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="black",
            highlightthickness=1,
            highlightbackground="#333333"
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Make canvas expand with window
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        # Bind movement keys (WASD and arrow keys) – use default args to avoid late binding
        moves = {
            "<Key-w>": (0, -1), "<Key-a>": (-1, 0), "<Key-s>": (0, 1), "<Key-d>": (1, 0),
            "<Up>": (0, -1), "<Left>": (-1, 0), "<Down>": (0, 1), "<Right>": (1, 0)
        }
        for seq, (dx, dy) in moves.items():
            self.bind_all(seq, lambda e, dx=dx, dy=dy: self._attempt_move(dx, dy))
        # Generate initial map
        self._generate_map()
        self._draw_map()

    def _adjust_cell_size(self):
        """Adjust CELL_SIZE so the map fits comfortably on the screen.

        The canvas will occupy up to 70% of the screen width/height. The cell size
        is reduced if necessary but never goes below 8 pixels to keep the map
        readable.
        """
        # Wait for window to be realized to get screen dimensions
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        max_w = int(screen_w * 0.70)
        max_h = int(screen_h * 0.70)
        cell_w = max_w // self.width
        cell_h = max_h // self.height
        new_size = min(cell_w, cell_h, self.DEFAULT_CELL_SIZE)
        if new_size < 8:
            new_size = 8
        self.CELL_SIZE = new_size

    def _create_controls(self):
        """Create styled controls using ttk widgets."""
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5, fill=tk.X)

        ttk.Label(control_frame, text="Map type:").grid(row=0, column=0, padx=5)
        self.map_var = tk.StringVar(value="dungeon")
        ttk.Radiobutton(
            control_frame, text="Dungeon (DFS)", variable=self.map_var,
            value="dungeon", command=self._restart
        ).grid(row=0, column=1, padx=2)
        ttk.Radiobutton(
            control_frame, text="Cavern (BFS)", variable=self.map_var,
            value="cavern", command=self._restart
        ).grid(row=0, column=2, padx=2)

        self.ai_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            control_frame, text="Use AI Director", variable=self.ai_var,
            command=self._restart
        ).grid(row=0, column=3, padx=10)

    def _restart(self):
        """Regenerate the map when settings change."""
        self.map_type = self.map_var.get()
        self.use_ai_director = self.ai_var.get()
        self._generate_map()
        self._draw_map()

    def _generate_map(self):
        """Generate the map using the selected generator and place player/exit."""
        if self.map_type == "dungeon":
            generator = DungeonGenerator(self.width, self.height)
        else:
            generator = CavernGenerator(self.width, self.height)
        self.game_map = generator.generate()

        floor_tiles = self.game_map.get_all_floor_tiles()
        if not floor_tiles:
            messagebox.showerror("Error", "No floor tiles generated!")
            self.destroy()
            return

        player_pos = random.choice(floor_tiles)
        self.player = Player(*player_pos)

        if self.use_ai_director:
            ai_director = AIDirector(self.game_map)
            exit_pos = ai_director.find_strategic_exit_position(
                self.player.x, self.player.y, min_distance=15
            )
            if exit_pos is None:
                floor_tiles.remove(player_pos)
                exit_pos = random.choice(floor_tiles)
        else:
            floor_tiles.remove(player_pos)
            exit_pos = random.choice(floor_tiles)

        self.exit_x, self.exit_y = exit_pos

    def _draw_map(self):
        """Render the map onto the canvas with a professional colour scheme."""
        # Ensure scroll region matches current cell size
        self.canvas.config(scrollregion=(0, 0, self.width * self.CELL_SIZE, self.height * self.CELL_SIZE))
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                cell = self.game_map.get_cell(x, y)
                # Base colours: walls dark gray, floors light gray
                color = "#2b2b2b" if cell == "#" else "#e0e0e0"
                # Override for player and exit
                if x == self.player.x and y == self.player.y:
                    color = "#1e90ff"  # dodger blue
                elif x == self.exit_x and y == self.exit_y:
                    color = "#32cd32"  # lime green
                x1 = x * self.CELL_SIZE
                y1 = y * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#444444"
                )

    def _attempt_move(self, dx, dy):
        """Handle player movement and win detection."""
        if self.player.move(dx, dy, self.game_map):
            self._draw_map()
            if (self.player.x, self.player.y) == (self.exit_x, self.exit_y):
                messagebox.showinfo("Victory!", "You have reached the exit!")
                self._restart()

if __name__ == "__main__":
    GameGUI().mainloop()
