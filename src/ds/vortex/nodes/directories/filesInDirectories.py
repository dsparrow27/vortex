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
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.directoriesPlug_ = plugs.InputPlug("directories", self)
        self.fullpathPlug_ = plugs.InputPlug("fullPath", self)

        self.addPlug(self.outputPlug_, clean=True)
        self.addPlug(self.directoriesPlug_, clean=True)
        self.addPlug(self.fullpathPlug_, clean=True)

        self.plugAffects(self.directoriesPlug_, self.outputPlug_)
        self.plugAffects(self.fullpathPlug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        result = []
        fullpath = self.fullpathPlug_.value

        for directory in self.directoriesPlug_.value:
            directory = os.path.normpath(directory)
            if not os.path.exists(directory):
                os.mkdir(directory)
            if fullpath:
                result.extend([os.path.join(directory, f)
                               for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
                continue
            result.extend([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return FilesInDirectoriesNode
