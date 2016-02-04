class Matrix(object):
    def __init__(self, matrix):
        self.matrix = matrix

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.matrix)

    def __eq__(self, other):
        return isinstance(other, self) and self.matrix == other.matrix

    def __getitem__(self, row, column):
        return self.matrix[row][column]

    def __setitem__(self, row, column, value):
        self.matrix[row][column] = value

    def __mul__(self, other):
        pass
    def __sub__(self, other):
        pass

    def clear(self):
        self.matrix = [[] for i in xrange(len(self.matrix))]

    def translate(self):
        pass

    def scale(self):
        pass

    def rotate(self):
        pass
