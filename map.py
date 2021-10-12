from copy import deepcopy
from typing import List

from dirt import Dirt, DirtPair
from tiles import TileState, Tile


def paths_to_dirt(m_orig, start_x, start_y, start_id):
    """
    Find the shortest path (BFS) to all dirt locations from specified starting point
    """
    class QElem:
        def __init__(self, x, y, dist):
            self.x = x
            self.y = y
            self.dist = dist

    m = deepcopy(m_orig)
    q = [QElem(start_x, start_y, 0)]
    dirt_paths = []
    dirt_found = 0
    while len(q) > 0 and dirt_found < len(m.dirt_locations):
        cur = q.pop(0)
        cur_id = m.at(cur.x, cur.y).dirt_id
        if cur_id is not None and cur_id != m.at(start_x, start_y).dirt_id:
            dirt_paths.append(DirtPair(start_id, m.at(cur.x, cur.y).dirt_id, cur.dist))
            dirt_found += 1
        for n in m.neighbors(cur.x, cur.y):
            n.state = TileState.opened
            q.append(QElem(n.x, n.y, cur.dist + 1))
        m.at(cur.x, cur.y).state = TileState.closed
    return dirt_paths


class Map:
    def __init__(self, text_maze):
        """
        Initialize the inner representation of the maze, find out where are located "dirty tiles"
        """
        self.maze = []
        self.maze.append([Tile(i, 0, False) for i in range(len(text_maze[0]) + 2)])
        dirt_id = 0
        self.dirt_locations = []
        for i, row in enumerate(text_maze, 1):
            row_tiles = [Tile(0, i, False)]
            for j, tile in enumerate(row, 1):
                if tile == 'E' or tile == 'V':
                    row_tiles.append(Tile(j, i, True))
                elif tile == 'D':
                    row_tiles.append(Tile(j, i, True, dirt_id))
                    self.dirt_locations.append(Dirt(dirt_id, j, i))
                    dirt_id += 1
                elif tile == 'B':
                    row_tiles.append(Tile(j, i, False))
            row_tiles.append(Tile(len(row)+1, i, False))
            self.maze.append(row_tiles)
        self.maze.append([Tile(i, 0, False) for i in range(len(text_maze[0]) + 2)])
        self.dirt_paths = None

    def calculate_dirt_paths(self):
        """
        Initialize dirt paths = lengths of paths between all pairs of dirt

        Needed for calculation of min spanning tree
        """
        self.dirt_paths = []
        for d in self.dirt_locations:
            self.dirt_paths.extend(paths_to_dirt(self, d.x, d.y, d.dirt_id))
        self.dirt_paths = list(set(self.dirt_paths))

    def neighbors(self, x, y) -> List[Tile]:
        """
        Returns unvisited neighbors of the specified tile that are free to step on
        """
        if not self.maze[y][x].is_free:
            raise Exception("Neighbors on blocked tile")
        n = []
        # left
        if self.maze[y][x - 1].is_free and self.maze[y][x - 1].state == TileState.unvisited:
            n.append(self.maze[y][x - 1])
        # right
        if self.maze[y][x + 1].is_free and self.maze[y][x + 1].state == TileState.unvisited:
            n.append(self.maze[y][x + 1])
        # up
        if self.maze[y - 1][x].is_free and self.maze[y - 1][x].state == TileState.unvisited:
            n.append(self.maze[y - 1][x])
        # down
        if self.maze[y + 1][x].is_free and self.maze[y + 1][x].state == TileState.unvisited:
            n.append(self.maze[y + 1][x])
        return n

    def opened_neighbors(self, x, y) -> List[Tile]:
        """
        Returns neighbors of the specified tile that are free to step on and are in state open
        """
        if not self.maze[y][x].is_free:
            raise Exception("Neighbors on blocked tile")
        n = []
        # left
        if self.maze[y][x - 1].is_free and self.maze[y][x - 1].state == TileState.opened:
            n.append(self.maze[y][x - 1])
        # right
        if self.maze[y][x + 1].is_free and self.maze[y][x + 1].state == TileState.opened:
            n.append(self.maze[y][x + 1])
        # up
        if self.maze[y - 1][x].is_free and self.maze[y - 1][x].state == TileState.opened:
            n.append(self.maze[y - 1][x])
        # down
        if self.maze[y + 1][x].is_free and self.maze[y + 1][x].state == TileState.opened:
            n.append(self.maze[y + 1][x])
        return n

    def at(self, x, y) -> Tile:
        return self.maze[y][x]

    def vacuum_dirt(self, x, y) -> Dirt:
        """
        Remove dirt on specific location and adjust data structures that contain it
        """
        if self.maze[y][x].dirt_id is None:
            raise Exception("Vacuum on non dirty tile")
        dirt_id = self.maze[y][x].dirt_id
        dirt = [d for d in self.dirt_locations if d.x == x and d.y == y][0]
        self.dirt_locations.remove(dirt)
        self.dirt_paths = [p for p in self.dirt_paths if p.id1 != dirt_id and p.id2 != dirt_id]
        self.maze[y][x].dirt_id = None
        return dirt
