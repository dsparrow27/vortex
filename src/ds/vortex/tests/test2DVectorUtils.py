import unittest
from ds.vortex.utils import vector2d


class Test2DVector(unittest.TestCase):
    def setUp(self):
        self.vector = vector2d.Vector2D([2.0, 3.0])
        self.vec = vector2d.Vector2D([2.0, 3.0])

    def testLength(self):
        self.assertEquals(len(self.vector), 2)
        self.assertNotEquals(len(self.vector), 3)
        self.assertEquals(self.vector.length(), 3.605551275463989)

    def testNormalize(self):
        self.assertEquals(self.vector.normalize(), vector2d.Vector2D([0.5547001962252291, 0.8320502943378437]))

    def testEquals(self):
        self.assertTrue(self.vec, self.vector)
        self.assertNotEquals([2, 6], self.vector)
        self.assertNotEquals(vector2d.Vector2D([2.0, 3.5]), self.vector)
        vector2 = vector2d.Vector2D(self.vec)
        self.assertEquals(vector2.vec, [2.0, 3.0])
        self.assertEquals(vector2 + vector2, vector2d.Vector2D([4.0, 6.0]))

    def testAdd(self):
        added = self.vec + self.vector
        self.assertEquals(added, vector2d.Vector2D([4.0, 6.0]))
        self.vec += self.vector
        self.assertEquals(added, vector2d.Vector2D([4.0, 6.0]))

    def testSubtract(self):
        self.assertEquals(self.vector - self.vec, vector2d.Vector2D([0.0, 0.0]))
        self.vec.x = -10
        self.vec.y = -5

    def testNeg(self):
        self.assertNotEquals(-self.vector, vector2d.Vector2D([-2.0, 3.0]))
        self.assertEquals(-self.vector, vector2d.Vector2D([-2.0, -3.0]))

    def testGetX(self):
        self.assertEquals(self.vector[0], 2.0)
        self.assertEquals(self.vector.x, 2.0)

    def testGetY(self):
        self.assertEquals(self.vector[1], 3.0)
        self.assertEquals(self.vector.y, 3.0)

    def testMult(self):
        self.assertEquals(self.vector * self.vec, 13)
        self.assertEquals(self.vector * -self.vec, -13)
        self.assertEquals(10 * self.vector, vector2d.Vector2D([20.0, 30.0]))
