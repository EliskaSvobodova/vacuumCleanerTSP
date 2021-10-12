from map import Map
from vacuum import Vacuum


def solve_map(filename):
    with open(filename) as f:
        lines = f.readlines()
        tmp = [line[:-1] for line in lines[:-1]]
        lines = tmp + lines[-1:]
        m = Map(lines[1:])
        m.calculate_dirt_paths()
    x, y = lines[0].split()
    v = Vacuum(int(x), int(y))
    return m, v.vacuum_all_dirt(m)


if __name__ == '__main__':
    m, path = solve_map('maps/b1')
    draw_m = []
    for row in m.maze:
        r = []
        for tile in row:
            if tile.is_free:
                if tile.dirt_id is not None:
                    r.append('D')
                else:
                    r.append(' ')
            else:
                r.append('#')
        draw_m.append(r)
    draw_m[path[0].y][path[0].x] = 'V'
    for p in path:
        if draw_m[p.y][p.x] == ' ':
            draw_m[p.y][p.x] = '.'
    for row in draw_m:
        for tile in row:
            print(tile, end='')
        print()
