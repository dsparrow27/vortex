import unittest
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs
from ds.vortex.core import graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testGraph")
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
        self.testNode2.getPlug("testInput1").connect(self.testNode.getPlug("testOutput"))
        leafNodes = self.graph.allLeaves()
        self.assertEquals(len(leafNodes), 1)
        self.assertEquals(leafNodes[0], self.testNode)

        self.testNode.getPlug("testOutput").disconnect(self.testNode2.getPlug("testInput1"))
        self.testNode2.getPlug("testInput1").disconnect(self.testNode.getPlug("testOutput"))
        leafNodes = self.graph.allLeaves()
        self.assertEquals(len(leafNodes), 2)

if __name__ == "__main__":
    unittest.main(verbosity=2)
