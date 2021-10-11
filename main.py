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
    return v.vacuum_all_dirt(m)


if __name__ == '__main__':
    path = solve_map('maps/b1')
    for p in path:
        print(p)
