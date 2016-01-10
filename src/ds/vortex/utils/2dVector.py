class Vector2D(object):
    def __init__(self, vec):
        self.vec = vec

    def __repr__(self):
        return "{0}{1}".format(type(self).__name__, self.__dict__)

    def __len__(self):
        return len(self.vec)

    def __eq__(self, other):
        return isinstance(other, Vector2D) and self.vec == other.vec

    def __add__(self, vec):
        assert len(self.vec) == len(vec)
        return Vector2D([self.vec[i] + vec[i] for i in range(len(self))])

    def __sub__(self, vec):
        return self + (-vec)

    def __neg__(self):
        assert len(self.vec) == len(vec)
        return Vector2D([vec * -1 for vec in self.vec])

    def __getitem__(self, item):
        return self.vec[item]

    def __setitem__(self, key, value):
        self.vec[key] = value

    @property
    def x(self):
        return self.vec[0]

    @property
    def y(self):
        return self.vec[1]
