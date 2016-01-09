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
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.sourceFile_ = plugs.InputPlug("sourceFiles", self, value=[])
        self.destinationDirectoryPlug_ = plugs.InputPlug("destinationDirectory", self, value="")

        self.addPlug(self.outputPlug_, clean=True)
        self.addPlug(self.sourceFile_, clean=True)
        self.addPlug(self.destinationDirectoryPlug_, clean=True)

        self.plugAffects(self.sourceFile_, self.outputPlug_)
        self.plugAffects(self.destinationDirectoryPlug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        sources = self.sourceFile_.value
        destination = self.destinationDirectoryPlug_.value
        if not os.path.exists(destination) and not os.path.isdir(destination):
            os.mkdir(destination)
        [shutil.copy2(src, destination) for src in sources]
        result = [os.path.join(destination, os.path.basename(newFile)) for newFile in sources]

        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return CopyFilesToNode
