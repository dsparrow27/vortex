import logging
import unittest

from ds.vortex.core import baseEdge
from ds.vortex.core import plug


class TestCase(unittest.TestCase):
    def setUp(self):
        self.inputPlug = plug.InputPlug("inputPlug1")
        self.outputPlug = plug.OutputPlug("outputPlug1")
        self.edge = baseEdge.Edge("testEdge1", inputPlug=self.inputPlug, outputPlug=self.outputPlug)
        self.edge2 = baseEdge.Edge("testEdg2", inputPlug=self.inputPlug, outputPlug=self.outputPlug)

    def testEquality(self):
        edge3 = baseEdge.Edge("testEdg2")
        self.assertEquals(self.edge, self.edge2)
        self.assertNotEquals(self.edge, edge3)

    def testDelete(self):
        self.edge.delete()
        self.assertEquals(len(self.inputPlug), 0)
        self.assertEquals(len(self.outputPlug), 0)

    def testIsConnected(self):
        edge3 = baseEdge.Edge("testEdg2")
        self.assertTrue(self.edge.isConnected(self.inputPlug, self.outputPlug))
        self.assertFalse(edge3.isConnected(self.inputPlug, self.outputPlug))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    unittest.main(verbosity=2)
