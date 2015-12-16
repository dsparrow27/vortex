import unittest
from ds.vortex.core import baseNode
from ds.vortex.core import basePlug
from ds.vortex.core import graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testGraph")
        self.testNode = baseNode.BaseNode("testNode")
        self.testNode2 = baseNode.BaseNode("testNode1")
        self.inputPlug = basePlug.BasePlug("testInput", self.testNode, attributeType=float, io="input")
        self.outputPlug = basePlug.BasePlug("testOutput", self.testNode, attributeType=float, io="output")
        self.node2inputPlug = basePlug.BasePlug("testInput", self.testNode2, attributeType=float, io="input")
        self.node2OutputPlug = basePlug.BasePlug("testOutput", self.testNode2, attributeType=float, io="output")
        self.testNode.addPlug(self.inputPlug)
        self.testNode.addPlug(self.outputPlug)
        self.testNode2.addPlug(self.inputPlug)
        self.testNode2.addPlug(self.outputPlug)

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
        self.assertEquals(self.graph.getNode("testNode"), [self.testNode])

    def testClearGraph(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        self.graph.clear()
        self.assertEquals(len(self.graph.nodes), 0)

    def testGraphAllLeaves(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        self.testNode.getPlug("testOutput").connect(self.testNode2.getPlug("testInput"))
        leafNodes = self.graph.allLeaves()
        self.assertEquals(leafNodes, None)
        self.node2OutputPlug.disconnect(self.outputPlug)
        self.outputPlug.disconnect(self.node2OutputPlug)
        leafNodes = self.graph.allLeaves()
        self.assertIsNone(leafNodes)

if __name__ == "__main__":
    unittest.main(verbosity=2)
