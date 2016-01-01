import os
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class SubDirectoriesNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("directories", self), [], clean=True)
        self.addPlug(plugs.InputPlug("recursive", self), True, clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        result = []
        if self.getPlug("recursive").value:
            for directory in self.getPlug("directories"):
                if not os.path.isdir(directory):
                    continue
                result.extend([d[0] for d in os.walk(os.path.normpath(directory))])
        else:
            for directory in self.getPlug("directories"):
                if not os.path.isdir(directory):
                    continue
                result.extend([d for d in os.listdir(directory) if os.path.isdir(d)])
        if not result:
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
    return SubDirectoriesNode
