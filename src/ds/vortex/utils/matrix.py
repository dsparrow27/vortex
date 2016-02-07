class Matrix4(object):
    def __init__(self, matrix):
        if isinstance(matrix, Matrix4):
            self.matrix = [[matrix[0], matrix[1], matrix[2], matrix[3]],
                           [matrix[4], matrix[5], matrix[6], matrix[7]],
                           [matrix[8], matrix[9], matrix[10], matrix[11]],
                           [matrix[12], matrix[13], matrix[14], matrix[15]]]
        else:
            self.matrix = matrix

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.matrix)

    def __eq__(self, other):
        """Compares the left with the right of the operator
        :param other: Matrix
        :return: boolean
        """
        return isinstance(other, self) and self.matrix == other.matrix

    def __getitem__(self, pos):
        return self.matrix[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.matrix[pos[0]][pos[1]] = value

    def __add__(self, other):
        """Adds the left to the right of the operator
        :param other: Matrix
        """
        raise NotImplementedError

    def __sub__(self, other):
        """Substracts the right from the left of the operator
        :param other: Matrix
        """
        raise NotImplementedError

    def __mul__(self, other):
        """Multiples the matrix
        :param other: Matrix
        """
        for i in xrange(len(self.matrix)):
            for axis in xrange(len(self.matrix[i])):
                self.matrix[i][axis] *= other[i, axis]
        return self

    def __neg__(self):
        raise NotImplementedError

    def toIdentity(self):
        """Sets the matrix identity
        :return:
        """
        self.matrix = [[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]]
        return self

    def clear(self):
        """Sets the matrix to [[0,0,0,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]]
        """
        self.matrix = [[0, 0, 0] for i in xrange(len(self.matrix))]

    def translate(self):
        """Returns the translation component of this matrix
        """
        raise NotImplementedError

    def scale(self):
        raise NotImplementedError

    def rotate(self):
        raise NotImplementedError
