from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from dirt import Dirt
from map import Map
import heapq

from tiles import Tile, TileState


@dataclass(order=True)
class PriorityTile:
    priority: int
    item: Tile = field(compare=False)

    def __init__(self, t: Tile):
        self.priority = t.from_start + t.heuristic
        self.item = t


class PathPart:
    class Action(Enum):
        go = auto()
        vacuum = auto()

    def __init__(self, x, y, action):
        self.x = x
        self.y = y
        self.action = action

    def __repr__(self):
        return f"({self.x}, {self.y}): {self.action.name}"


def cost_min_spanning_tree(m, x, y) -> int:
    return 0


class Vacuum:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def vacuum_all_dirt(self, m_orig: Map):
        found_dirt = []
        path = []
        while len(found_dirt) < len(m_orig.dirt_locations):
            dirt, path_to_dirt = self.to_next_dirt(m_orig, found_dirt)
            found_dirt.append(dirt)
            path.extend(path_to_dirt)
            self.x = dirt.x
            self.y = dirt.y
        return path

    def to_next_dirt(self, m_orig: Map, found_dirt: List[Dirt]):
        m = deepcopy(m_orig)
        for f_d in found_dirt:
            m.vacuum_dirt(f_d.x, f_d.y)
        m.at(self.x, self.y).heuristic = cost_min_spanning_tree(m, self.x, self.y)
        m.at(self.x, self.y).from_start = 0
        m.at(self.x, self.y).state = TileState.opened
        cur = PriorityTile(m.at(self.x, self.y))
        q: List[PriorityTile] = [cur]
        heapq.heapify(q)
        while len(q) > 0 and len(m.dirt_locations) > 0:
            cur = heapq.heappop(q)
            if cur.item.dirt_id is not None:
                dirt = m.vacuum_dirt(cur.item.x, cur.item.y)
                return dirt, self.construct_path(cur.item, m_orig)
            o_n = m.opened_neighbors(cur.item.x, cur.item.y)
            for elem in q:
                if elem.item in o_n:
                    from_start = cur.item.from_start + 1
                    heuristic = cost_min_spanning_tree(m, elem.item.x, elem.item.y)
                    if elem.priority < from_start + heuristic:
                        elem.item.from_start = from_start
                        elem.item.heuristic = heuristic
                        elem.item.parent = cur.item
            for n in m.neighbors(cur.item.x, cur.item.y):
                n.from_start = cur.item.from_start + 1
                n.heuristic = cost_min_spanning_tree(m, n.x, n.y)
                n.state = TileState.opened
                n.parent = cur.item
                heapq.heappush(q, PriorityTile(n))
            cur.item.state = TileState.closed
        raise Exception("Dirt not found")

    def construct_path(self, cur_node: Tile, m_orig) -> List[PathPart]:
        path = []
        while cur_node.parent is not None:
            if m_orig.at(cur_node.x, cur_node.y).dirt_id is not None:
                path.append(PathPart(cur_node.x, cur_node.y, PathPart.Action.vacuum))
            path.append(PathPart(cur_node.x, cur_node.y, PathPart.Action.go))
            cur_node = cur_node.parent
        return list(reversed(path))
