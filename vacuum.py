from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from map import Map
import heapq

from tiles import EmptyTile


@dataclass(order=True)
class PriorityTile:
    priority: int
    item: EmptyTile = field(compare=False)


class PathPart:
    class Action(Enum):
        go = auto()
        vacuum = auto()

    def __init__(self, x, y, action):
        self.x = x
        self.y = y
        self.action = action


class Vacuum:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def vacuum_all_dirt(self, m_orig: Map):
        m = deepcopy(m_orig)
        path = []
        q: List[PriorityTile] = [PriorityTile(0, m.at_empty(self.x, self.y))]
        heapq.heapify(q)
        while len(m.dirt_locations) > 0:
            cur = heapq.heappop(q)
            if cur.item.dirt_id is not None:
                path.append(PathPart(cur.item.x, cur.item.y, PathPart.Action.vacuum))
                m.vacuum_dirt(cur.item.x, cur.item.y)
            for n in m.neighbors(cur.item.x, cur.item.y):
                heapq.heappush(q, PriorityTile(n.from_start + n.heuristic, n))

