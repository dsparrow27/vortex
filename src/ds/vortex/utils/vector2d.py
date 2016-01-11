import math

class Vector2D(object):
    def __init__(self, vec=None):
        if isinstance(vec, Vector2D):
            self.vec = [vec[0], vec[1]]
        else:
            self.vec = vec
        self._x = vec[0]
        self._y = vec[1]

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
        return Vector2D([vec * -1 for vec in self.vec])

    def __mul__(self, other):
        return sum(Vector2D([self.vec[i] * other[i] for i in range(len(self.vec))]))

    def __rmul__(self, scalar):
        return Vector2D([x * scalar for x in self.vec])

    def __getitem__(self, item):
        return self.vec[item]

    def __setitem__(self, key, value):
        self.vec[key] = value

    def length(self):
        return math.sqrt(sum(x * x for x in self.vec))

    def normalize(self):
        length = self.length()
        return Vector2D([x / length for x in self.vec])

    @property
    def x(self):
        return self.vec[0]

    @property
    def y(self):
        return self.vec[1]

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value
