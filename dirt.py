class Dirt:
    def __init__(self, dirt_id, x, y):
        self.dirt_id = dirt_id
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Dirt):
            return self.dirt_id == other.dirt_id
        return False

    def __hash__(self):
        return hash(self.dirt_id)


class DirtPair:
    def __init__(self, id1, id2, distance):
        self.id1 = id1
        self.id2 = id2
        self.distance = distance
