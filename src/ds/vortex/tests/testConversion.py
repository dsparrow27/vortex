import unittest

from ds.vortex.nodes.conversion import toArray


class TestToArray(unittest.TestCase):
    def setUp(self):
        self.node = toArray.ToArray(name="toArray")
        self.output = self.node.getPlug("output")

    def testToArray(self):
        self.node.getPlug("value").value = None
        self.node.compute(self.output)
        self.assertEquals(self.output.value, [None])
        self.node.getPlug("value").value = "testMe"
        self.node.compute(self.output)
        self.assertEquals(self.output.value, ["testMe"])