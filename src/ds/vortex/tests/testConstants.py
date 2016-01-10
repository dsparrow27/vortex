import math
import unittest
from collections import OrderedDict

from ds.vortex.nodes.constants import boolean
from ds.vortex.nodes.constants import dict as dictNode
from ds.vortex.nodes.constants import halfPi
from ds.vortex.nodes.constants import integer
from ds.vortex.nodes.constants import orderedDict
from ds.vortex.nodes.constants import pi
from ds.vortex.nodes.constants import scalar


class TestConstants(unittest.TestCase):
    def testBoolean(self):
        node = boolean.BoolNode("boolean")
        valuePlug = node.getPlug("value")
        valuePlug.value = 0
        node.compute(node.getPlug("output"))
        self.assertFalse(valuePlug.value)

        valuePlug.value = "kdhf"
        node.compute(node.getPlug("output"))
        self.assertTrue(valuePlug.value)

    def testDict(self):
        node = dictNode.DictNode("dict")
        node.compute(node.getPlug("output"))
        self.assertIsInstance(node.getPlug("output").value, dict)
        self.assertEquals(node.getPlug("output").value, {})

    def testHalfPi(self):
        node = halfPi.HalfPiNode("scalar")
        node.compute(node.getPlug("output"))
        self.assertIsInstance(node.getPlug("output").value, float)
        self.assertEquals(node.getPlug("output").value, (math.pi / 2.0))

    def testInteger(self):
        node = integer.IntNode("int")
        valuePlug = node.getPlug("value")
        valuePlug.value = 163.6486534
        node.compute(node.getPlug("output"))
        self.assertIsInstance(node.getPlug("output").value, int)
        self.assertEquals(node.getPlug("output").value, 163)

    def testOrderedDict(self):
        node = orderedDict.DictNode("ordereddict")
        node.compute(node.getPlug("output"))
        self.assertIsInstance(node.getPlug("output").value, OrderedDict)
        self.assertEquals(node.getPlug("output").value, OrderedDict())

    def testPi(self):
        node = pi.PiNode("pi")
        node.compute(node.getPlug("output"))
        self.assertIsInstance(node.getPlug("output").value, float)
        self.assertEquals(node.getPlug("output").value, 3.141592653589793)

    def testScalar(self):
        node = scalar.ScalarNode("scalar")
        valuePlug = node.getPlug("value")
        valuePlug.value = 0
        node.compute(node.getPlug("output"))
        self.assertIsInstance(node.getPlug("output").value, float)
        self.assertEquals(node.getPlug("output").value, 0.0)


if __name__ == "__main__":
    unittest.main()
