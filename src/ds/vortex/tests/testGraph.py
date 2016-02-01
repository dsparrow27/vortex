import pprint
import unittest
import logging
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs
from ds.vortex.nodes.math.basic import sum
from ds.vortex.core import graph

logger = logging.getLogger(__name__)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testGraph")
        self.testNode = baseNode.BaseNode("testNode")
        self.testNode2 = baseNode.BaseNode("testNode2")
        self.testNode.addPlug(plugs.InputPlug("testInput", self.testNode))
        self.testNode.addPlug(plugs.OutputPlug("testOutput", self.testNode))
        self.testNode2.addPlug(plugs.InputPlug("testInput1", self.testNode2))
        self.testNode2.addPlug(plugs.OutputPlug("testOutput1", self.testNode2))

    def testNodeUniqueNodeName(self):
        self.graph.addNode(self.testNode)
        testNode = baseNode.BaseNode("testNode")
        self.graph.addNode(testNode)
        self.assertEquals(testNode.name, "testNode0")

    def testAddNode(self):
        self.assertEquals(self.graph.addNode(self.testNode), self.testNode)
        self.assertTrue(len(self.graph.nodes))
        # should raise valueError if the node is already in the graph
        self.assertRaises(ValueError, self.graph.addNode(self.testNode))

    def testDeleteNode(self):
        self.graph.addNode(self.testNode)
        self.graph.deleteNode(self.testNode)
        self.assertEquals(len(self.graph.nodes), 0)

    def testGetNode(self):
        self.graph.addNode(self.testNode)
        self.assertEquals(self.graph.getNode("testNode"), self.testNode)

    def testGetter(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        self.assertEquals(self.graph.get("testNode|testInput"), self.testNode.getPlug("testInput"))
        self.assertEquals(self.graph.get("testNode|testOutput"), self.testNode.getPlug("testOutput"))
        self.assertEquals(self.graph.get("testNode"), self.testNode)
        testEdge = self.testNode.getPlug("testOutput").connect(self.testNode2.getPlug("testInput1"))
        self.assertEquals(self.graph.get("testOutput_testInput1"), testEdge)

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

    def testContains(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        isIn = self.testNode in self.graph
        self.assertTrue(self.testNode, isIn)


class TestGraphDirty(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testPushGraph")
        self.addNode1 = sum.SumNode("addNode1")
        self.addNode2 = sum.SumNode("addNode2")
        self.addNode3 = sum.SumNode("addNode3")
        self.graph.addNode(self.addNode1)
        self.graph.addNode(self.addNode2, value1=5, value2=15)
        self.graph.addNode(self.addNode3)
        self.addNode1.getPlug("output").connect(self.addNode3.getPlug("value1"))
        self.addNode2.getPlug("output").connect(self.addNode3.getPlug("value2"))

    def testSetValuePropagatesDirtyDownStream(self):
        self.addNode1.getPlug("value1").value = 50
        self.addNode1.getPlug("value2").value = 20
        # test that all plugs are dirty
        self.assertTrue(self.addNode1.getPlug("value2").dirty)
        self.assertTrue(self.addNode1.getPlug("output").dirty)
        self.assertTrue(self.addNode2.getPlug("value1").dirty)
        self.assertTrue(self.addNode2.getPlug("value2").dirty)
        self.assertTrue(self.addNode2.getPlug("output").dirty)
        self.assertTrue(self.addNode3.getPlug("value1").dirty)
        self.assertTrue(self.addNode3.getPlug("value2").dirty)
        self.assertTrue(self.addNode3.getPlug("output").dirty)
        self.assertEquals(self.addNode3.getPlug("output").value, 90)
        # requestEvalate computes all dirty nodes, so all the plugs should be clean
        self.assertFalse(self.addNode1.getPlug("value2").dirty)
        self.assertFalse(self.addNode1.getPlug("output").dirty)
        self.assertFalse(self.addNode2.getPlug("value1").dirty)
        self.assertFalse(self.addNode2.getPlug("value2").dirty)
        self.assertFalse(self.addNode2.getPlug("output").dirty)
        self.assertFalse(self.addNode3.getPlug("value1").dirty)
        self.assertFalse(self.addNode3.getPlug("value2").dirty)
        self.assertFalse(self.addNode3.getPlug("output").dirty)


class TestSerialize(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph("serialGraph")

    def testEmptyGraph(self):
        savedGraph = self.graph.serializeGraph()
        self.newGraph = graph.Graph("emptyGraph")
        self.newGraph.loadGraph(savedGraph)
        self.assertEquals(len(self.graph), len(self.newGraph))

    def testSerializeNodeToGraph(self):
        self.graph.addNode(baseNode.BaseNode("testNode"))
        self.graph.addNode(baseNode.BaseNode("testNode2"))
        savedGraph = self.graph.serializeGraph()
        self.newGraph = graph.Graph.loadGraph(savedGraph)
        self.assertEquals(len(self.graph.nodes), len(self.newGraph.nodes))
        self.assertEquals(self.graph._name, self.newGraph._name)

    def testSerializeNodePlugsToGraph(self):
        node = baseNode.BaseNode("testNode")
        node2 = baseNode.BaseNode("testNode2")
        node.addPlug(plugs.InputPlug("testInputPlug", node=node))
        node.addPlug(plugs.OutputPlug("testOutputPlug", node=node))
        node2.addPlug(plugs.InputPlug("testInputPlug", node=node2))
        node2.addPlug(plugs.OutputPlug("testOutputPlug", node=node2))
        node2.getPlug("testOutputPlug").connect(node.getPlug("testInputPlug"))
        self.graph.addNode(node)
        self.graph.addNode(node2)
        savedGraph = self.graph.serializeGraph()
        self.newGraph = graph.Graph.loadGraph(savedGraph)
        self.assertEquals(len(self.graph), len(self.newGraph))
        self.assertEquals(self.graph._name, self.newGraph._name)
        self.assertDictEqual(savedGraph, self.newGraph.serializeGraph())


if __name__ == "__main__":
    from ds.vortex import customLogger

    logger = customLogger.getCustomLogger(loglevel='DEBUG')
    unittest.main(verbosity=2)
