import enum


class MazeBase(object):
    """This class contains base functions."""
    class Create(enum.Enum):
        """Enum for creation algorithms."""
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT = "Hunt and kill algorithm"
        ELLER = "Eller's algorithm"
        SIDEWINDER = "Sidewinder algorithm"
        PRIM = "Prim's algorithm"
        KRUSKAL = "Kruskal's algorithm"

    def __init__(self):
        """Constructor."""
        self.maze = None
        self.solution = None
        self._dll = None

    @property
    def row_count_with_walls(self):
        """Returns the mazes row count with walls."""
        return self.maze.shape[0]

    @property
    def col_count_with_walls(self):
        """Returns the mazes column count with walls."""
        return self.maze.shape[1]

    @property
    def row_count(self):
        """Returns the mazes row count."""
        return self.row_count_with_walls // 2

    @property
    def col_count(self):
        """Returns the mazes column count."""
        return self.col_count_with_walls // 2
