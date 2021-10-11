from copy import deepcopy
from typing import List

from dirt import Dirt, DirtPair
from tiles import BlockedTile, EmptyTile, TileState, Tile


def paths_to_dirt(m_orig, start_x, start_y, start_id):
    class QElem:
        def __init__(self, x, y, dist):
            self.x = x
            self.y = y
            self.dist = dist

    m = deepcopy(m_orig)
    q = [QElem(start_x, start_y, 0)]
    dirt_paths = []
    while len(q) > 0 and len(dirt_paths) < len(m.dirt_locations):
        cur = q.pop()
        if m.at(cur.x, cur.y).dirt_id is not None:
            dirt_paths.append(DirtPair(start_id, m.at(cur.x, cur.y).dirt_id, cur.dist))
        for n in m.neighbors(cur.x, cur.y):
            n.state = TileState.opened
            q.append(n)
        cur.state = TileState.closed
    return dirt_paths


class Map:
    def __init__(self, text_maze):
        self.maze = []
        self.maze.append([BlockedTile(i, 0) for i in range(len(text_maze[0]))])
        dirt_id = 0
        self.dirt_locations = []
        for i, row in enumerate(text_maze, 1):
            row_tiles = [BlockedTile(0, i)]
            for j, tile in enumerate(row, 1):
                if tile == 'E':
                    row_tiles.append(EmptyTile(j, i))
                elif tile == 'D':
                    row_tiles.append(EmptyTile(j, i, dirt_id))
                    self.dirt_locations.append(Dirt(dirt_id, j, i))
                    dirt_id += 1
                elif tile == 'B':
                    row_tiles.append(BlockedTile(j, i))
            row_tiles.append(BlockedTile(len(row)+1, i))
        self.maze.append([BlockedTile(i, 0) for i in range(len(text_maze[0]))])
        self.dirt_paths: List[DirtPair] = None

    def calculate_dirt_paths(self):
        self.dirt_paths = []
        for d in self.dirt_locations:
            self.dirt_paths.extend(paths_to_dirt(self, d.x, d.y, d.dirt_id))

    def neighbors(self, x, y) -> List[EmptyTile]:
        if not self.maze[y][x].is_free():
            raise Exception("Neighbors on blocked tile")
        n = []
        # left
        if self.maze[y][x - 1].is_free() and self.maze[y][x - 1].state == TileState.unvisited:
            n.append(self.maze[y][x - 1])
        # right
        if self.maze[x + 1][y].is_free() and self.maze[x + 1][y].state == TileState.unvisited:
            n.append(self.maze[x + 1][y])
        # up
        if self.maze[x][y - 1].is_free() and self.maze[x][y - 1].state == TileState.unvisited:
            n.append(self.maze[x][y - 1])
        # down
        if self.maze[x][y + 1].is_free() and self.maze[x][y + 1].state == TileState.unvisited:
            n.append(self.maze[x][y + 1])
        return n

    def at(self, x, y) -> Tile:
        return self.maze[y][x]

    def at_empty(self, x, y) -> EmptyTile:
        if not isinstance(self.maze[y][x], EmptyTile):
            raise Exception("At empty on non empty tile")
        return self.maze[y][x]

    def vacuum_dirt(self, x, y):
        if self.maze[y][x].dirt_id is None:
            raise Exception("Vacuum on non dirty tile")
        dirt_id = self.maze[y][x].dirt_id
        self.dirt_locations.remove(Dirt(dirt_id, x, y))
        self.dirt_paths = [p for p in self.dirt_paths if p.id1 != dirt_id and p.id2 != dirt_id]
        self.maze[y][x].dirt_id = None



    # def show(self, vacuum):
    #     for i, row in enumerate(self.maze):
    #         for j, tile in enumerate(row):
    #             if i == vacuum.y and j == vacuum.x:
    #                 print('V', end='')
    #             else:
    #                 if tile == 'E':
    #                     print(' ', end='')
    #                 elif tile == 'D':
    #                     print('*', end='')
    #                 elif tile == 'B':
    #                     print('#', end='')
    #         print()

    # def write(self, x, y, value):
    #     self.maze[y][x] = value
