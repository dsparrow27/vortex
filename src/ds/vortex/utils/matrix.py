class Matrix(object):
    def __init__(self, matrix):
        self.matrix = matrix

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.matrix)

    def __eq__(self, other):
        """Compares the left with the right of the operator
        :param other: Matrix
        :return: boolean
        """
        return isinstance(other, self) and self.matrix == other.matrix

    def __add__(self, other):
        """Adds the left to the right of the operator
        :param other: Matrix
        """
        pass

    def __sub__(self, other):
        """Substracts the right from the left of the operator
        :param other: Matrix
        """
        pass

    def __mul__(self, other):
        """Multiples the matrix
        :param other: Matric
        """
        pass

    def __neg__(self):
        pass

    def __getitem__(self, row, column):
        return self.matrix[row][column]

    def __setitem__(self, row, column, value):
        self.matrix[row][column] = value

    def isNull(self):
        """Check to is if the matrix is empty [[],[],[]]
        :return:bool
        """
        return all(i == [] for i in self.matrix)

    def clear(self):
        """Sets the matrix to [[],[],[]]
        """
        self.matrix = [[] for i in xrange(len(self.matrix))]

    def translate(self):
        """Returns the translation component of this matrix
        """
        pass

    def scale(self):
        pass

    def rotate(self):
        pass
