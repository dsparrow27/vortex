import math
import vector


class Quaternion(object):
    def __init__(self, quat):
        """
        :param quat: list(float4)
        """
        self.quaternion = quat
        self._x = quat[0]
        self._y = quat[1]
        self._z = quat[2]
        self._w = quat[3]

    def length(self):
        """Return the length of the quaternion
        :return: float
        """
        return math.sqrt(sum(x * x for x in self.quaternion))

    def normalize(self):
        """Returns the normalized vector, modifies the original vec
        :return:
        """
        length = self.length()
        self._x /= length
        self._y /= length
        self._z /= length
        self._w /= length
        self.quaternion[0] = self._x
        self.quaternion[1] = self._y
        self.quaternion[2] = self._z
        self.quaternion[3] = self._w
        return self

    def conjugate(self):
        """Returns the conjugate of this quaternion ie the negated x, y , z
        :return: Quaternion
        """
        return Quaternion([-self._x, -self._y, -self._z, self._w])

    def __mul__(self, r):
        if isinstance(r, vector.Vector3D):
            w = (-self._x * r.x) - (self._y * r.y) - (self._z * r.z)
            x = (self._w * r.x) + (self._y * r.z) - (self._z * r.y)
            y = (self._w * r.y) + (self._z * r.x) - (self._x * r.z)
            z = (self._w * r.z) + (self._x * r.y) - (self._y * r.x)

        else:

            w = (self._w * r.w) - (self._x * r.x) - (self._y * r.y) - (self._z * r.z)
            x = (self._x * r.w) + (self._w * r.x) + (self._y * r.z) - (self._z * r.y)
            y = (self._y * r.w) + (self._w * r.y) + (self._z * r.x) - (self._x * r.z)
            z = (self._z * r.w) + (self._w * r.z) + (self._x * r.y) - (self._y * r.x)

        return Quaternion([x, y, z, w])

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @z.setter
    def z(self, value):
        self._z = value

    @w.setter
    def w(self, value):
        self._w = value
