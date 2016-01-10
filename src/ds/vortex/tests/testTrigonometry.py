import unittest
import math
from ds.vortex import customLogger
from ds.vortex.nodes.math.trigonometry import arccos
from ds.vortex.nodes.math.trigonometry import arcsin
from ds.vortex.nodes.math.trigonometry import arctan
from ds.vortex.nodes.math.trigonometry import cos
from ds.vortex.nodes.math.trigonometry import sin
from ds.vortex.nodes.math.trigonometry import tan


class TestMathArcCosNode(unittest.TestCase):
    def setUp(self):
        self.node = arccos.ArcCosNode(name="arcCos")
        self.output = self.node.getPlug("output")

    def testArcCos(self):
        self.node.getPlug("value").value = None
        self.assertRaises(TypeError, self.node.compute, self.output)
        self.node.getPlug("value").value = -1
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, math.pi)
        self.node.getPlug("value").value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, math.pi / 2)
        self.node.getPlug("value").value = 1
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 0)


class TestMathArcSinNode(unittest.TestCase):
    def setUp(self):
        self.node = arcsin.ArcSinNode(name="arcSin")
        self.output = self.node.getPlug("output")

    def testArcSin(self):
        self.node.getPlug("value").value = None
        self.assertRaises(TypeError, self.node.compute, self.output)
        self.node.getPlug("value").value = -1
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, -math.pi / 2)
        self.node.getPlug("value").value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 0)
        self.node.getPlug("value").value = 1
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, math.pi / 2)


class TestMathArcTanNode(unittest.TestCase):
    def setUp(self):
        self.node = arctan.ArcTanNode(name="arcTan")
        self.output = self.node.getPlug("output")

    def testArcTan(self):
        self.node.getPlug("value").value = None
        self.assertRaises(TypeError, self.node.compute, self.output)
        self.node.getPlug("value").value = -1
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, -math.pi / 4)
        self.node.getPlug("value").value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 0)
        self.node.getPlug("value").value = 1
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, math.pi / 4)


class TestMathCosNode(unittest.TestCase):
    def setUp(self):
        self.node = cos.CosNode(name="cos")
        self.output = self.node.getPlug("output")

    def testCos(self):
        self.node.getPlug("value").value = None
        self.assertRaises(TypeError, self.node.compute, self.output)
        self.node.getPlug("value").value = -math.pi / 2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 6.123233995736766e-17)
        self.node.getPlug("value").value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 1)
        self.node.getPlug("value").value = math.pi/2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 6.123233995736766e-17)
        self.node.getPlug("value").value = math.pi
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, -1)


class TestMathSinNode(unittest.TestCase):
    def setUp(self):
        self.node = sin.SinNode(name="sin")
        self.output = self.node.getPlug("output")

    def testSin(self):
        self.node.getPlug("value").value = None
        self.assertRaises(TypeError, self.node.compute, self.output)
        self.node.getPlug("value").value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 0)
        self.node.getPlug("value").value = math.pi / 2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 1)
        self.node.getPlug("value").value = -math.pi / 2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, -1)


class TestMathTanNode(unittest.TestCase):
    def setUp(self):
        self.node = tan.TanNode(name="tan")
        self.output = self.node.getPlug("output")

    def testTan(self):
        self.node.getPlug("value").value = None
        self.assertRaises(TypeError, self.node.compute, self.output)
        self.node.getPlug("value").value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 0)
        self.node.getPlug("value").value = math.pi / 4
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, 0.9999999999999999)
        self.node.getPlug("value").value = -math.pi / 4
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.output.value, -0.9999999999999999)


if __name__ == "__main__":
    logging = customLogger.getCustomLogger()
    unittest.main(verbosity=2)
