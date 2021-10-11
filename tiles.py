from enum import Enum, auto


class TileState(Enum):
    unvisited = auto()
    opened = auto()
    closed = auto()


class Tile:
    def __init__(self, x, y, is_free, dirt_id=None, parent=None, from_start=None, heuristic=None):
        self.x = x
        self.y = y
        self.is_free = is_free
        self.dirt_id = dirt_id
        self.state = TileState.unvisited
        self.parent = parent
        self.from_start = from_start
        self.heuristic = heuristic

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash([self.x, self.y])
