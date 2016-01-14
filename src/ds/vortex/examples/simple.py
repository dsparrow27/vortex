"""
Very simple example for creating and adding nodes to a graph
"""
from ds.vortex.core import graph
from ds.vortex.nodes.constants import scalar
from ds.vortex.nodes.math.basic import add
from ds.vortex.nodes.math.basic import multiply


def testExample():
    """Simple test example adding three math nodes, setting plug values and triggering a compute
    :return:
    """
    # first create an instance of a node from the nodeLibrary
    scalar1 = scalar.ScalarNode(name="scalar1")
    scalar2 = scalar.ScalarNode(name="scalar2")
    add1 = add.AddNode(name="testAddNode")
    mult1 = multiply.MultiplyNode(name="testMultiply")
    # create the graph, the graph is the main interface for getting and adding nodes
    gx = graph.Graph(name="newGraph")
    # add each node, kwargs are accept here, the key == plugName on the node you're adding
    # and the value is the value to give to the plug
    gx.addNode(scalar1, value=3.0)
    gx.addNode(scalar2, value=10.0)
    gx.addNode(add1)
    gx.addNode(mult1)
    # example of setting a input value
    mult1.getPlug("multiplyBy").value = 2
    # connect nodes together via the plug object, the connect method returns the Edge Object when can be used to access
    # or set edge data
    # You can connect only from outputs to input or inputs to outputs, inputs can only have one connection
    scalar1.getPlug("output").connect(add1.getPlug("value1"))
    scalar2.getPlug("output").connect(add1.getPlug("value2"))
    add1.getPlug("output").connect(mult1.getPlug("value"))
    # ask for a output value which triggers a compute of the graph, this will transverse the graph to
    # compute the right nodes.
    # for this its will first travel to add1.output and see if it needs computing, since it does it will ask for the value
    # it will then go to both scalar nodes in any order and compute those, the output value will be push back to the add
    # node compute it then to the multiply node then compute and return the result.
    # order of travel: mult1 --> add1 -->scalar1(computes) --> add1 -->>scalar2(computes) --> add1(computes) -->mult1(computes)
    endResult = mult1.getPlug("output").value
    return endResult
