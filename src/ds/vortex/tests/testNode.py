import unittest
from ds.vortex.core import baseNode, plug
from ds.vortex.nodes.math.basic import multiply
from ds.vortex.nodes.math.basic import add
from ds.vortex.nodes.math.basic import divide
from ds.vortex.nodes.math.basic import invert


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
        self.node.atttributeAffects(self.plug, outputPlug1)
        self.node.atttributeAffects(inputPlug2, outputPlug1)
        self.node.atttributeAffects(inputPlug2, outputPlug2)
        self.assertEqual(self.node.getAttributeAffects(outputPlug1), [self.plug, inputPlug2])
        self.assertEqual(self.node.getAttributeAffects(outputPlug2), [inputPlug2])
        self.assertEqual(self.node.getAttributeAffects(self.plug), [outputPlug1])
        self.assertEqual(self.node.getAttributeAffects(inputPlug2), [outputPlug1, outputPlug2])

    def testSerialize(self):
        data = self.node.serialize()


class TestAddNode(unittest.TestCase):
    def setUp(self):
        self.node = add.AddNode("add")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value1")
        inputPlug2 = self.node.getPlug("value2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 20)
        inputPlug1.value = 6158449
        inputPlug2.value = 8568
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 6167017)


class TestMultipleNode(unittest.TestCase):
    def setUp(self):
        self.node = multiply.MultiplyNode("multiply")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value1")
        inputPlug2 = self.node.getPlug("value2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 100)
        inputPlug1.value = 6158449
        inputPlug2.value = 8568
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 52765591032)
        inputPlug1.value = 1654138763
        inputPlug2.value = 0
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 0)


class TestDivideNode(unittest.TestCase):
    def setUp(self):
        self.node = divide.DivideNode("divide")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value1")
        inputPlug2 = self.node.getPlug("value2")
        inputPlug1.value = 10
        inputPlug2.value = 10
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 1)
        inputPlug1.value = 855423
        inputPlug2.value = 8766663
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 0)
        inputPlug1.value = 1654138763
        inputPlug2.value = 0
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 0)


class TestInvertNode(unittest.TestCase):
    def setUp(self):
        self.node = invert.InvertNode("divide")

    def testCompute(self):
        inputPlug1 = self.node.getPlug("value")
        inputPlug1.value = 10
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, -10)
        inputPlug1.value = -855423
        self.node.compute()
        self.assertEquals(self.node.getPlug("output").value, 855423)


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    unittest.main(verbosity=2)
