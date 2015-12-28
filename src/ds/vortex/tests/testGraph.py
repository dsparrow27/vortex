import unittest
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs
from ds.vortex.core import graph
from ds.vortex.nodes.math import add


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testGraph")
        self.graph.model = "push"
        self.testNode = baseNode.BaseNode("testNode")
        self.testNode2 = baseNode.BaseNode("testNode1")
        self.testNode.addPlug(plugs.InputPlug("testInput", self.testNode))
        self.testNode.addPlug(plugs.OutputPlug("testOutput", self.testNode))
        self.testNode2.addPlug(plugs.InputPlug("testInput1", self.testNode2))
        self.testNode2.addPlug(plugs.OutputPlug("testOutput1", self.testNode2))

    def testAddNode(self):
        self.assertEquals(self.graph.addNode(self.testNode), self.testNode)
        self.assertTrue(len(self.graph.nodes))
        # should return none if the node is already in the graph
        self.assertIsNone(self.graph.addNode(self.testNode))

    def testDeleteNode(self):
        self.graph.addNode(self.testNode)
        self.graph.deleteNode(self.testNode)
        self.assertEquals(len(self.graph.nodes), 0)

    def testGetNode(self):
        self.graph.addNode(self.testNode)
        self.assertEquals(self.graph.getNode("testNode00"), self.testNode)

    def testClearGraph(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        self.graph.clear()
        self.assertEquals(len(self.graph.nodes), 0)

    def testGraphAllLeaves(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        self.testNode.getPlug("testOutput").connect(self.testNode2.getPlug("testInput1"))
        leafNodes = self.graph.allLeaves()
        self.assertEquals(len(leafNodes), 1)
        self.assertEquals(leafNodes[0], self.testNode)

        self.testNode.getPlug("testOutput").disconnect(self.testNode2.getPlug("testInput1"))
        leafNodes = self.graph.allLeaves()
        self.assertEquals(len(leafNodes), 2)


class TestGraphDirty(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testPushGraph")
        self.graph.model = "push"
        self.addNode1 = add.AddNode("addNode1")
        self.addNode2 = add.AddNode("addNode2")
        self.addNode3 = add.AddNode("addNode3")
        self.graph.addNode(self.addNode1)
        self.graph.addNode(self.addNode2, input1=5, input2=15)
        self.graph.addNode(self.addNode3)
        self.addNode1.getPlug("output").connect(self.addNode3.getPlug("input1"))
        self.addNode2.getPlug("output").connect(self.addNode3.getPlug("input2"))

    def testSetValuePropagatesDirtyDownStream(self):
        self.addNode1.getPlug("input1").value = 50
        self.addNode1.getPlug("input2").value = 20
        # test that all plugs are dirty
        self.assertTrue(self.addNode1.getPlug("input2").dirty)
        self.assertTrue(self.addNode1.getPlug("output").dirty)
        self.assertTrue(self.addNode2.getPlug("input1").dirty)
        self.assertTrue(self.addNode2.getPlug("input2").dirty)
        self.assertTrue(self.addNode2.getPlug("output").dirty)
        self.assertTrue(self.addNode3.getPlug("input1").dirty)
        self.assertTrue(self.addNode3.getPlug("input2").dirty)
        self.assertTrue(self.addNode3.getPlug("output").dirty)
        self.graph.requestEvaluate(self.addNode3.getPlug("output"))
        self.assertEquals(self.addNode3.getPlug("output").value, 90)
        # requestEvalate computes all dirty nodes, so all the plugs should be clean
        self.assertFalse(self.addNode1.getPlug("input2").dirty)
        self.assertFalse(self.addNode1.getPlug("output").dirty)
        self.assertFalse(self.addNode2.getPlug("input1").dirty)
        self.assertFalse(self.addNode2.getPlug("input2").dirty)
        self.assertFalse(self.addNode2.getPlug("output").dirty)
        self.assertFalse(self.addNode3.getPlug("input1").dirty)
        self.assertFalse(self.addNode3.getPlug("input2").dirty)
        self.assertFalse(self.addNode3.getPlug("output").dirty)

if __name__ == "__main__":
    import logging
    logger = logging.getLogger("graph")
    logger.setLevel(level=logging.INFO)
    unittest.main(verbosity=2)
