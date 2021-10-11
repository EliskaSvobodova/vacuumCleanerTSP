from map import Map
from vacuum import Vacuum

if __name__ == '__main__':
    filename = 'b1'
    with open(filename) as f:
        lines = f.readlines()
        m = Map(lines[1:])
        m.calculate_dirt_paths()
    x, y = lines[0].split()
    v = Vacuum(int(x), int(y))
    path = v.vacuum_all_dirt(m)
