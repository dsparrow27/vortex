import unittest
from ds.vortex.nodes.math.basic import absolute
from ds.vortex.nodes.math.basic import add
from ds.vortex.nodes.math.basic import divide
from ds.vortex.nodes.math.basic import floor
from ds.vortex.nodes.math.basic import invert
from ds.vortex.nodes.math.basic import modulo
from ds.vortex.nodes.math.basic import multiply
from ds.vortex.nodes.math.basic import power
from ds.vortex.nodes.math.basic import squareRoot
from ds.vortex.nodes.math.basic import subtract


class TestAbsoluteNode(unittest.TestCase):
    def setUp(self):
        self.node = absolute.AbsoluteNode("absolute")

    def testCompute(self):
        inputPlug = self.node.getPlug("value")
        inputPlug.value = 10
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 10)
        inputPlug.value = -153
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 153)


class TestAddNode(unittest.TestCase):
    def setUp(self):
        self.node = add.AddNode("add")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value1")
        inputPlug2 = self.node.getPlug("value2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 20)


class TestMultipleNode(unittest.TestCase):
    def setUp(self):
        self.node = multiply.MultiplyNode("multiply")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value")
        inputPlug2 = self.node.getPlug("multiplyBy")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 100)


class TestDivideNode(unittest.TestCase):
    def setUp(self):
        self.node = divide.DivideNode("divide")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value1")
        inputPlug2 = self.node.getPlug("value2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 1)
        inputPlug1.value = 855423
        inputPlug2.value = 8766663
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 0)
        inputPlug1.value = 1654138763
        inputPlug2.value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 0)


class TestFloorNode(unittest.TestCase):
    def setUp(self):
        self.node = floor.FloorNode("floor")

    def testCompute(self):
        inputPlug = self.node.getPlug("value")
        inputPlug.value = 10.002
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 10)
        inputPlug.value = -10.002
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, -11.0)
        self.assertNotEquals(self.node.getPlug("output").value, -10)


class TestInvertNode(unittest.TestCase):
    def setUp(self):
        self.node = invert.InvertNode("divide")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value")
        inputPlug1.value = 10
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, -10)
        inputPlug1.value = -855423
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 855423)


class TestModuloByNode(unittest.TestCase):
    def setUp(self):
        self.node = modulo.ModuloNode("moduloBy")

    def testCompute(self):
        inputPlug = self.node.getPlug("value")
        moduloByPlug = self.node.getPlug("moduloBy")
        inputPlug.value = 7
        moduloByPlug.value = 2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 1)
        moduloByPlug.value = 6
        self.node.compute(self.node.getPlug("output"))
        self.assertNotEquals(self.node.getPlug("output").value, 0)


class TestPowerNode(unittest.TestCase):
    def setUp(self):
        self.node = power.PowerNode("power")

    def testCompute(self):
        value1Plug = self.node.getPlug("value1")
        value2Plug = self.node.getPlug("value2")
        value1Plug.value = 7
        value2Plug.value = 2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 49)
        value2Plug.value = 0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 1)


class TestSquareRootNode(unittest.TestCase):
    def setUp(self):
        self.node = squareRoot.SquareRootNode("squareRoot")

    def testCompute(self):
        inputPlug = self.node.getPlug("value")
        inputPlug.value = 7
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 2.6457513110645907)


class TestSubtractNode(unittest.TestCase):
    def setUp(self):
        self.node = subtract.SubtractNode("subtract")

    def testCompute(self):
        inputPlug = self.node.getPlug("value")
        subtractPlug = self.node.getPlug("subtract")
        inputPlug.value = 7
        subtractPlug.value = 2
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 5)
        subtractPlug.value = 6.0
        self.node.compute(self.node.getPlug("output"))
        self.assertEquals(self.node.getPlug("output").value, 1.0)


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    unittest.main(verbosity=2)
