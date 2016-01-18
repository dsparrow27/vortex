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

    def __eq__(self, vec):
        return isinstance(vec, Vector2D) and self.vec == vec.vec

    def __add__(self, vec):
        """Adds two vectors together and the returns the resulting example
        :param vec: Vector2D or flost3
        :return: Vector2D
        """
        assert len(self.vec) == len(vec)
        return Vector2D([self.vec[i] + vec[i] for i in range(len(self))])

    def __sub__(self, vec):
        """Subtracts the two vectors
        :param vec: Vector2D
        :return: Vector2D
        """
        return self + (-vec)

    def __neg__(self):
        """Negates the vector
        :return: Vector2D, return the negative of the vector, eg (1,-1,2) == (-1,1,-2)
        """
        return Vector2D([vec * -1 for vec in self.vec])

    def __mul__(self, vec):
        """Dot product(scalar product) of two vectors. Takes Two equal length vectors and returns a single number.
        :param other: Vector2D instance or float3
        :return: Vector2D
        """
        assert len(self.vec) == len(vec)
        return sum(Vector2D([self.vec[i] * vec[i] for i in range(len(self.vec))]))

    def __rmul__(self, scalar):
        return Vector2D([x * scalar for x in self.vec])

    def __getitem__(self, item):
        """Gets the index value from the vector
        :param item: int, the index value in the vector to get
        :return: float or int
        """
        return self.vec[item]

    def __setitem__(self, key, value):
        """Sets the value within the vector via the index
        :param key:
        :param value:
        """
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
