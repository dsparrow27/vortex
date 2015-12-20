from ds.vortex.core import baseNode
from ds.vortex.core import basePlug as plugs


class AddNode(baseNode.BaseNode):
    """Add math node, sums the values from the input port and outputs the total sum.
    default input port names : input1, input2 (input1 + input2)
    default output port name: output.
    """
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        super(AddNode, self).__init__(name)

    def initialize(self):
        self.addPlug(plugs.InputPlug("input1", self, 0))
        self.addPlug(plugs.InputPlug("input2", self, 0))
        self.addPlug(plugs.OutputPlug("output", self))

    def compute(self):
        result = sum([plug.value for plug in self.inputs() if plug.value is not None])
        self.getPlug("output").value = result

def getNode():
    return AddNode