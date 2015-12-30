import unittest
from ds.vortex.core import baseNode, plug
from ds.vortex.nodes.math import add, multiply


class TestBaseNode(unittest.TestCase):
    def setUp(self):
        self.node = baseNode.BaseNode("testNode")
        self.plug = plug.BasePlug("testPlug", self.node)

    def testAddPlug(self):
        self.node.addPlug(self.plug)
        self.assertEquals(len(self.node.plugs), 1)
        self.node.deletePlug(self.plug)
        self.assertEquals(len(self.node.plugs), 0)

    def testGetPlug(self):
        self.node.addPlug(self.plug)
        self.assertEquals(self.node.getPlug("testPlug"), self.plug)
        self.node.deletePlug(self.plug)
        self.assertEquals(self.node.getPlug("testPlug"), None)


class TestAddNode(unittest.TestCase):
    def setUp(self):
        self.node = add.AddNode("add")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("input1")
        inputPlug2 = self.node.getPlug("input2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 20)
        inputPlug1.value = 6158449
        inputPlug2.value = 8568
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 6167017)


class TestMultipleNode(unittest.TestCase):
    def setUp(self):
        self.node = multiply.MultiplyNode("multiply")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("input1")
        inputPlug2 = self.node.getPlug("input2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 100)
        inputPlug1.value = 6158449
        inputPlug2.value = 8568
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 52765591032)
        inputPlug1.value = 1654138763
        inputPlug2.value = 0
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 0)

if __name__ == "__main__":
    import logging
    logger = logging.getLogger("baseNode")
    logger.setLevel(level=logging.INFO)
    unittest.main(verbosity=2)
