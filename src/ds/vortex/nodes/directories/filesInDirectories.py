import os

from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class FilesInDirectoriesNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("directories", self), [], clean=True)
        self.addPlug(plugs.InputPlug("fullPath", self), True, clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        result = []
        fullpath = self.getPlug("fullPath").value

        for directory in self.getPlug("directories").value:
            directory = os.path.normpath(directory)
            if not os.path.exists(directory):
                os.mkdir(directory)
            if fullpath:
                result.extend([os.path.join(directory, f)
                               for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
                continue
            result.extend([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

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
    return FilesInDirectoriesNode
