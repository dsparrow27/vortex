from collections import OrderedDict
from ds.vortex import customLogger as cusLogger
import inspect

from ds.vortex.core import vortexEvent

logger = cusLogger.getCustomLogger()


class BaseNode(object):
    """Core node class that stores the all the plugs, initialize and compute methods must be overridden in custom nodes
    """
    addedPlug = vortexEvent.VortexSignal(),  # emits the plug added
    deletedPlug = vortexEvent.VortexSignal()  # emits the deleted plug
    computed = vortexEvent.VortexSignal()  # emits the node instance computed and the outputPlug
    initializing = vortexEvent.VortexSignal()  # emits the node instance

    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        self.name = name
        self._plugs = OrderedDict()
        self.initialize()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        """Determines if the node and its plugs equal
        :param other:
        :return:
        """
        return isinstance(other, BaseNode) and self.plugs == other.plugs

    def __len__(self):
        """Return the length of the plugs for this node
        :return: int, the length of the plugs
        """
        return len(self._plugs)

    @staticmethod
    def plugAffects(inputPlug, outputPlug):
        """Add a link between to plugs on the same node, gets added to affects variable
        :param inputPlug: inputPlug instance
        :param outputPlug: outputPlug instance
        """
        logger.debug(
            "Setting plug affection:: inputPlug > {0}, outputPlug > {1}".format(inputPlug.name, outputPlug.name))
        inputPlug.affects.add(outputPlug)
        outputPlug.affects.add(inputPlug)

    @staticmethod
    def getPlugAffects(plug):
        """Return the affect set for the plug
        :param plug: plug instance
        :return: set()
        """
        affection = plug.affects
        logger.debug(
            "got plug affection:: plug > {0}, affected by > {1}".format(plug.name,
                                                                        [affect.name for affect in affection]))
        return affection

    @property
    def plugs(self):
        """Returns the the plugs for this node
        :return: dict(name:plug)
        """
        return self._plugs

    def addPlug(self, plug, clean=False):
        """Adds a plug to self
        :param plug: Plug instance to add
        :param value: any type, This argument get passed to the plug value attribute
        :param clean: sets the new plug dirty state, this gets set after the value is set
        """
        self._plugs[plug.name] = plug

        if clean:
            plug.dirty = False

    def getPlug(self, plugName):
        """Returns the plug based on the name
        :param plugName: str, the plug name to get
        :return: plug instance or None
        """
        return self._plugs.get(plugName)

    def deletePlug(self, plug):
        """Removes the plug from the node
        :param plug: the plug instance to delete
        """
        del self._plugs[plug.name]
        self.deletedPlug.emit(plug)

    def inputs(self):
        """Finds and returns all the inputs for self
        :return: list(Plug)
        """
        inputs = []
        for plug in self._plugs.values():
            if plug.isInput():
                inputs.append(plug)
        return inputs

    def outputs(self):
        """Finds and returns all the outputs for self
        :return: list(Plug)
        """
        outputs = []
        for plug in self._plugs.values():
            if plug.isOutput():
                outputs.append(plug)
        return outputs

    def initialize(self):
        """Intended to be overridden, this method is for cresting plugs, for the node before this node gets computed for the first time
        :return: None
        """
        self.initializing.emit(self)

    def compute(self, requestPlug):
        """Intended to be overloaded, main compute method for a node instance, this must return a result
        :param requestPlug: the output plug to compute, this must be passed to the overloaded
        :return: None
        """
        logger.debug("Computing {}".format(self.name))
        self.computed.emit(self, requestPlug)
        return None

    def serialize(self):
        """Returns a dict of the nodes data
        :return: dict
        """
        data = {"name": self.name,
                "plugs": OrderedDict(),
                "className": type(self).__name__,
                "moduleName": inspect.getmodulename(__file__),
                "modulePath": __file__.replace("\\", ".").split("src.")[-1].replace(".pyc", "").replace(".py", "")
                }
        for plug in self._plugs.values():
            data["plugs"][plug.name] = plug.serialize()
        return data

    def addPlugsFromDict(self, plugDict):
        """Creates plug objects for the node based on the plugDict
        :param plugDict: dict
        """
        for plug in plugDict.values():
            modulePath = plug.get("modulePath")
            try:
                module = __import__(modulePath, globals(), locals(), [plug.get("moduleName")], -1)
            except ImportError, er:
                logger.error("""importing {0} Failed! , have you typed the right name?,
                    check self.modulesDict for availables Modules.""".format(modulePath))
                raise er
            ioType = plug.get("io")
            if ioType == "input":
                self.addPlug(module.InputPlug(name=plug.get("name"), node=self, value=plug.get("value")))
            else:
                self.addPlug(module.OutputPlug(name=plug.get("name"), node=self, value=plug.get("value")))

    def log(self, tabLevel=-1):
        """Return the hierarchy for this node including the plugs
        :param tabLevel: int, spacing
        :return: str
        """
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|------" + self.name + "\n"

        for child in self._plugs.values():
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return BaseNode
