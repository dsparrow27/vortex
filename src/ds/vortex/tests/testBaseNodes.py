import unittest
from collections import OrderedDict
from ds.vortex.core import baseNode, plug


class TestBaseNode(unittest.TestCase):
    def setUp(self):
        self.node = baseNode.BaseNode("testNode")
        self.plug = plug.InputPlug("testPlug", self.node)
        self.node.addPlug(self.plug)

    def testAddPlug(self):
        newplug = plug.InputPlug("testPlug1", self.node)
        self.node.addPlug(newplug)
        self.assertEquals(len(self.node.plugs), 2)
        self.node.deletePlug(newplug)
        self.assertEquals(len(self.node.plugs), 1)

    def testGetPlug(self):
        self.assertEquals(self.node.getPlug("testPlug"), self.plug)
        self.node.deletePlug(self.plug)
        self.assertEquals(self.node.getPlug("testPlug"), None)

    def testGetAttributeAffects(self):
        outputPlug1 = plug.OutputPlug("testOutPlug1", self.node)
        outputPlug2 = plug.OutputPlug("testOutPlug2", self.node)
        inputPlug2 = plug.InputPlug("testinPlug2", self.node)
        self.node.plugAffects(self.plug, outputPlug1)
        self.node.plugAffects(inputPlug2, outputPlug1)
        self.node.plugAffects(inputPlug2, outputPlug2)
        self.assertEqual(self.node.getPlugAffects(outputPlug1), set([self.plug, inputPlug2]))
        self.assertEqual(self.node.getPlugAffects(outputPlug2), set([inputPlug2]))
        self.assertEqual(self.node.getPlugAffects(self.plug), set([outputPlug1]))
        self.assertEqual(self.node.getPlugAffects(inputPlug2), set([outputPlug1, outputPlug2]))

    def testSerialize(self):
        data = self.node.serialize()
        correctData = {'className': 'BaseNode',
                       'moduleName': 'baseNode',
                       'modulePath': 'ds.vortex.core.baseNode',
                       'name': 'testNode',
                       'plugs': OrderedDict([('testPlug', {'moduleName': 'plug', 'name': 'testPlug', 'value': None,
                                                           'className': 'InputPlug', 'io': 'input',
                                                           'modulePath': 'ds.vortex.core.plug'})])}
        self.assertIsInstance(data, dict)
        self.assertEquals(data, correctData)


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    unittest.main(verbosity=2)
