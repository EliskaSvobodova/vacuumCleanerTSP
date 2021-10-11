from abc import ABC, abstractmethod
from enum import Enum, auto


class TileState(Enum):
    unvisited = auto()
    opened = auto()
    closed = auto()


class Tile(ABC):
    def __init__(self, x, y, dirt_id=None):
        self.x = x
        self.y = y
        self.dirt_id = dirt_id
        self.state = TileState.unvisited

    @abstractmethod
    def is_free(self):
        pass


class BlockedTile(Tile):
    def is_free(self):
        return False


class EmptyTile(Tile):
    def __init__(self, x, y, dirt_id=None, parent=None, from_start=None, heuristic=None):
        super().__init__(x, y, dirt_id)
        self.parent = parent
        self.from_start = from_start
        self.heuristic = heuristic

    def is_free(self):
        return True
