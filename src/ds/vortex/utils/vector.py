import math


class Vector(object):
    """Basic Vector Object
    """

    def __init__(self, vec):
        """
        :param vec: list
        """
        self.vec = vec
        self._x = vec[0]
        self._y = vec[1]

    def __repr__(self):
        return "{0}{1}".format(type(self).__name__, self.__dict__)

    def __eq__(self, vec):
        return isinstance(vec, Vector) and self.vec == vec.vec

    def __len__(self):
        """Returns the length, if its a vector2d then length 2 will be returned
        :return:
        """
        return len(self.vec)

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

    def __add__(self, vec):
        """Adds two vectors together and the returns the resulting example
        :param vec: Vector2D or flost3
        :return: Vector2D
        """
        assert len(self.vec) == len(vec)
        return Vector([self.vec[i] + vec[i] for i in range(len(self))])

    def __sub__(self, vec):
        """Subtracts the two vectors
        :param vec: Vector2D
        :return: Vector2D
        """
        return self + (-vec)

    def __neg__(self):
        """Negates the vector
        :return: new Vector
        """
        return Vector([vec * -1 for vec in self.vec])

    def __mul__(self, vec):
        """Dot product(scalar product) of two vectors. Takes Two equal length vectors and returns a single number.
        :param vec: Vector2D instance or float3
        :return: new Vector
        """
        assert len(self.vec) == len(vec)
        return sum(Vector([self.vec[i] * vec[i] for i in range(len(self.vec))]))

    def __rmul__(self, scalar):
        """Vector right multiplication
        :param scalar: float or int
        :return: new Vector
        """
        return Vector([x * scalar for x in self.vec])

    def __abs__(self):
        return Vector([abs(i) for i in self.vec])

    def length(self):
        """Return the length of the vector
        :return: float
        """
        return math.sqrt(sum(x * x for x in self.vec))

    def normalize(self):
        """Returns the normalized vector, modifies the original vec
        :return:
        """
        length = self.length()
        self._x /= length
        self._y /= length
        self.vec[0] = self._x
        self.vec[1] = self._y
        return self

    def rotate(self, angle):
        """Rotate the vector by the angle
        :param angle:
        """
        cos = math.cos(angle)
        sin = math.sin(angle)
        return Vector([self._x * cos - self._y * sin, self._x * sin + self._y * cos])

    @property
    def x(self):
        """Returns the x axis of the vector
        :return: int or float
        """
        return self.vec[0]

    @property
    def y(self):
        """Returns the y axis of the vector
        :return: int or float
        """
        return self.vec[1]

    @x.setter
    def x(self, value):
        """Sets the x axis of the vector
        """
        self._x = value

    @y.setter
    def y(self, value):
        """Sets the y axis of the vector
        """
        self._y = value


class Vector3D(Vector):
    def __init__(self, vec=None):
        super(Vector3D, self).__init__(vec)
        self.vec = [vec[0], vec[1], vec[2]]
        self._z = vec[3]

    def __eq__(self, vec):
        return isinstance(vec, Vector3D) and self.vec == vec.vec

    def __add__(self, vec):
        """Adds two vectors together and the returns the resulting example
        :param vec: Vector2D or flost3
        :return: Vector2D
        """
        assert len(self.vec) == len(vec)
        return Vector3D([self.vec[i] + vec[i] for i in range(len(self))])

    def __neg__(self):
        """Negates the vector
        :return: Vector2D, return the negative of the vector, eg (1,-1,2) == (-1,1,-2)
        """
        return Vector3D([vec * -1 for vec in self.vec])

    def __mul__(self, vec):
        """Dot product(scalar product) of two vectors. Takes Two equal length vectors and returns a single number.
        :param vec: Vector2D instance or float3
        :return: Vector2D
        """
        assert len(self.vec) == len(vec)
        return sum(Vector3D([self.vec[i] * vec[i] for i in range(len(self.vec))]))

    def __rmul__(self, scalar):
        """Returns the right multiplication
        :param scalar:
        :return:
        """
        return Vector3D([x * scalar for x in self.vec])

    def normalize(self):
        """Returns the normalized vector, modifies the original vec
        :return: self
        """
        length = self.length()
        self._x /= length
        self._y /= length
        self._z /= length
        self.vec[0] = self._x
        self.vec[1] = self._y
        self.vec[2] = self._z
        return self

    def crossProduct(self, vec):
        """Returns the cross product
        :param vec, Vector3D
        :return: Vector3D
        """
        x = self._y * vec.z - self._z * vec.y
        y = self._z * vec.x - self._x * vec.z
        z = self._x * vec.y - self._y * vec.x
        return Vector3D([x, y, z])

    def rotate(self, rotation):
        """Rotate the vector by the angle using a quaternion
        :param rotation: Quaternion
        """
        w = rotation * rotation.Conjugate()
        return Vector3D([w.x, w.y, w.z])

    def lerp(self, vec, lerpFactor):
        """
        :param vec: Vector3D
        :param lerpFactor: float
        :return: float
        """
        return vec - self * lerpFactor + self

    @property
    def z(self):
        """Returns the z axis of the vector
        :return: int or float
        """
        return self.vec[1]

    @z.setter
    def z(self, value):
        """Sets the x axis of the vector
        """
        self._z = value
