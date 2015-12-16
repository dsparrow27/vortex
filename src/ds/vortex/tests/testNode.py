import unittest
from ds.vortex.core import baseNode, basePlug


class TestNode(unittest.TestCase):
    def setUp(self):
        self.node = baseNode.BaseNode("testNode")
        self.plug = basePlug.BasePlug("testPlug", self.node, attributeType=float, io="input")

    def testAddInputPlug(self):
        self.node.addPlug(self.plug)
        self.assertEquals(len(self.node.plugs), 1)
        self.node.deletePlug(self.plug)
        self.assertEquals(len(self.node.plugs), 0)

    def testGetPlug(self):
        self.node.addPlug(self.plug)
        self.assertEquals(len(self.node.getPlug("testPlug")), 1)
        self.node.deletePlug(self.plug)
        self.assertEquals(len(self.node.getPlug("testPlug")), 0)

    def testGetInputs(self):
        pass

    def testGetOutputs(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
