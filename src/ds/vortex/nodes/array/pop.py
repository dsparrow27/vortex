from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class PopIndex(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("array", self), [], clean=True)
        self.addPlug(plugs.InputPlug("index", self), 0, clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        value = self.getPlug("index").value
        array = self.getPlug("array").value
        if value in array:
            result = self.getPlug("array").value.pop(value)
        else:
            return
        output = self.getPlug("output")
        if output is not None:
            output.value = result
        output.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return PopIndex
