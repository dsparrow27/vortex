import os
import shutil

from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class CopyFilesToNode(baseNode.BaseNode):
    """Copy a list of files to a directory and returns the new file paths
    """
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("sourceFiles", self), [], clean=True)
        self.addPlug(plugs.InputPlug("destinationDirectory", self), "", clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        sources = self.getPlug("sourceFiles").value
        destination = self.getPlug("destinationDirectory").value
        if not os.path.exists(destination) and not os.path.isdir(destination):
            os.mkdir(destination)
        [shutil.copy2(src, destination) for src in sources]
        result = [os.path.join(destination, os.path.basename(newFile)) for newFile in sources]
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
    return CopyFilesToNode
