import pprint
import unittest
from ds.vortex.core import baseNode
from ds.vortex.core import baseEdge
from ds.vortex.core import plug as plugs
from ds.vortex.nodes.math.basic import add
from ds.vortex.core import graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testGraph")
        self.testNode = baseNode.BaseNode("testNode1")
        self.testNode2 = baseNode.BaseNode("testNode2")
        self.testNode.addPlug(plugs.InputPlug("testInput", self.testNode))
        self.testNode.addPlug(plugs.OutputPlug("testOutput", self.testNode))
        self.testNode2.addPlug(plugs.InputPlug("testInput1", self.testNode2))
        self.testNode2.addPlug(plugs.OutputPlug("testOutput1", self.testNode2))

    def testNodeUniqueNodeName(self):
        self.graph.addNode(self.testNode)
        testNode = baseNode.BaseNode("testNode1")
        self.graph.addNode(testNode)
        self.assertEquals(testNode.name, "testNode10")

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
        self.assertEquals(self.graph.getNode("testNode1"), self.testNode)

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

    def testGetNodeFromIndex(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        self.assertEquals(self.graph[0], self.testNode)
        with self.assertRaises(IndexError):
            self.graph[2]

    def testContains(self):
        self.graph.addNode(self.testNode)
        self.graph.addNode(self.testNode2)
        isIn = self.testNode in self.graph
        self.assertTrue(self.testNode, isIn)


class TestGraphDirty(unittest.TestCase):
    def setUp(self):
        self.graph = graph.Graph(name="testPushGraph")
        self.addNode1 = add.AddNode("addNode1")
        self.addNode2 = add.AddNode("addNode2")
        self.addNode3 = add.AddNode("addNode3")
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

        # pprint.pprint(savedGraph)

        # the graph dict needs to be a fucking json file should do that at some point next week

    def testSerializeNodePlugsToGraph(self):
        node = baseNode.BaseNode("testNode")
        node2 = baseNode.BaseNode("testNode2")
        node.addPlug(plugs.InputPlug("testInputPlug", node=node))
        node.addPlug(plugs.OutputPlug("testOutputPlug", node=node))
        node2.addPlug(plugs.InputPlug("testInputPlug2", node=node2))
        node2.addPlug(plugs.OutputPlug("testOutputPlug2", node=node2))
        node2.getPlug("testOutputPlug2").connect(node.getPlug("testInputPlug"))
        self.graph.addNode(node)
        self.graph.addNode(node2)

        savedGraph = self.graph.serializeGraph()
        print "loading>>>>>>>>>>>>>>>>>>>>>>>"
        self.newGraph = graph.Graph.loadGraph(savedGraph)
        self.assertEquals(len(self.graph), len(self.newGraph))
        self.assertEquals(self.graph._name, self.newGraph._name)

        for index, node in enumerate(self.graph.nodes.values()):
            self.assertEquals(len(node.plugs), len(self.newGraph.nodes.values()[index].plugs))
            for plugIndex, plug in enumerate(node.plugs.values()):
                newGraphNode = self.newGraph.nodes.values()[index]
                newGraphPlug = newGraphNode.plugs.values()[plugIndex]
                self.assertEqual(plug.name, newGraphPlug.name)
                self.assertEquals(len(plug.connections), 1)
                self.assertEquals(len(newGraphPlug.connections), 1)
                for plugConnection in plug.connections:
                    self.assertIsInstance(plugConnection, baseEdge.Edge)
                for plugConnection in newGraphPlug.connections:
                    self.assertIsInstance(plugConnection, baseEdge.Edge)
        #
        #     self.assertIsInstance(savedGraph, dict)
        #     correctDict = {'className': 'Graph',
        #                    'edges': {'testOutputPlug2_testInputPlug': {'arbitraryData': None,
        #                                                                'className': 'Edge',
        #                                                                'input': ('testInputPlug',
        #                                                                          'testNode'),
        #                                                                'moduleName': 'baseEdge',
        #                                                                'modulePath': 'vortex.core.baseEdge',
        #                                                                'name': 'testOutputPlug2_testInputPlug',
        #                                                                'output': ('testOutputPlug2',
        #                                                                           'testNode2')
        #                                                                }
        #                              },
        #                    'moduleName': 'graph',
        #                    'modulePath': 'vortex.core.graph',
        #                    'name': 'serialGraph',
        #                    'nodes': OrderedDict([('testNode', {'className': 'BaseNode', 'plugs': OrderedDict([(
        #                        'testInputPlug',
        #                        {
        #                            'moduleName': 'plug',
        #                            'name': 'testInputPlug',
        #                            'value': None,
        #                            'className': 'InputPlug',
        #                            'io': 'input',
        #                            'modulePath': 'vortex.core.plug'
        #                        }), (
        #                        'testOutputPlug',
        #                        {
        #                            'moduleName': 'plug',
        #                            'name': 'testOutputPlug',
        #                            'value': None,
        #                            'className': 'OutputPlug',
        #                            'io': 'output',
        #                            'modulePath': 'vortex.core.plug'
        #                        })]),
        #                                                        'moduleName': 'baseNode', 'name': 'testNode',
        #                                                        'modulePath': 'vortex.core.baseNode'
        #                                                        }), ('testNode2', {'className': 'BaseNode',
        #                                                                           'plugs': OrderedDict([('testInputPlug2', {
        #                                                                               'moduleName': 'plug',
        #                                                                               'name': 'testInputPlug2',
        #                                                                               'value': None,
        #                                                                               'className': 'InputPlug',
        #                                                                               'io': 'input',
        #                                                                               'modulePath': 'vortex.core.plug'
        #                                                                           }), ('testOutputPlug2',
        #                                                                                {'moduleName': 'plug',
        #                                                                                 'name': 'testOutputPlug2',
        #                                                                                 'value': None,
        #                                                                                 'className': 'OutputPlug',
        #                                                                                 'io': 'output',
        #                                                                                 'modulePath': 'vortex.core.plug'
        #                                                                                 })]), 'moduleName': 'baseNode',
        #                                                                           'name': 'testNode2',
        #                                                                           'modulePath': 'vortex.core.baseNode'
        #                                                                           })]),
        #                    'version': '1.0.0'
        #                    }
        #     self.assertEquals(savedGraph, correctDict)


if __name__ == "__main__":
    from ds.vortex import customLogger

    logger = customLogger.getCustomLogger()
    unittest.main(verbosity=2)
