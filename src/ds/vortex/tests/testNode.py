import unittest
from ds.vortex.core import baseNode, basePlug
from ds.vortex.nodes.math import add


class TestBaseNode(unittest.TestCase):
    def setUp(self):
        self.node = baseNode.BaseNode("testNode")
        self.plug = basePlug.BasePlug("testPlug", self.node)

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

if __name__ == "__main__":
    unittest.main(verbosity=2)
