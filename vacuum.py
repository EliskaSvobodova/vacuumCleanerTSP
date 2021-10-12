from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from dirt import Dirt
from map import Map, paths_to_dirt
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


class Edge:
    def __init__(self, src_node, dest_node, weight):
        self.src_node = src_node
        self.dest_node = dest_node
        self.weight = weight


class BushNode:
    def __init__(self, parent, rank):
        self.parent = parent
        self.rank = rank

    def find_parent(self, node):
        if node.parent is None:
            return node
        return self.find_parent(node.parent)


def cost_min_spanning_tree(m, x, y) -> int:
    """
    Calculate the cost of the minimal spanning tree including the specified point with Kruskal algorithm
    """
    dirt_paths = deepcopy(m.dirt_paths)
    dirt_paths.extend(paths_to_dirt(m, x, y, -1))
    dirt_paths = sorted(dirt_paths, key=lambda d: d.distance)
    bushes = {d.dirt_id: BushNode(None, 0) for d in sorted(m.dirt_locations, key=lambda dirt: dirt.dirt_id)}
    bushes[-1] = BushNode(None, 0)
    span_tree = []
    for d_p in dirt_paths:
        u, v = bushes[d_p.id1], bushes[d_p.id2]
        parent_u, parent_v = u.find_parent(u), v.find_parent(v)
        if parent_u != parent_v:
            span_tree.append(d_p)
            if parent_u.rank < parent_v.rank:
                parent_u.parent = parent_v
                parent_v.rank = max(parent_v.rank, parent_u.rank + 1)
            else:
                parent_v.parent = parent_u
                parent_u.rank = max(parent_u.rank, parent_v.rank + 1)
        if len(span_tree) == len(m.dirt_locations):
            break
    return sum(edge.distance for edge in span_tree)


class Vacuum:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def vacuum_all_dirt(self, m_orig: Map):
        """
        Vacuum all dirt one by one

        Pick the next dirt with A* with min spanning tree heuristic
        """
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
        """
        Find path to the most suitable dirt, according to the shortest path and min spanning tree heuristic
        """
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
                        elem.priority = from_start + heuristic
            heapq.heapify(q)
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
