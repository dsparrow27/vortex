import unittest
from ds.vortex.nodes.dict import add
from ds.vortex.nodes.dict import get
from ds.vortex.nodes.dict import remove


class TestAddDict(unittest.TestCase):
    def setUp(self):
        self.node = add.AddToDictNode(name="addDict")
        self.output = self.node.getPlug("output")
        self.value = self.node.getPlug("value")
        self.valueToAdd = self.node.getPlug("valueToAdd")
        self.keyPlug = self.node.getPlug("key")

    def testNoneRaiseTypeError(self):
        self.value.value = []
        self.assertRaises(TypeError, self.node.compute, self.output)

    def testAddToDict(self):
        self.value.value = {}
        self.valueToAdd.value = [6251, 354]
        self.keyPlug.value = "test"
        self.node.compute(self.output)
        self.assertEquals(self.output.value, {"test": [6251, 354]})


class TestGetDict(unittest.TestCase):
    def setUp(self):
        self.node = get.GetKeyNode(name="getDict")
        self.output = self.node.getPlug("output")
        self.value = self.node.getPlug("value")
        self.keyPlug = self.node.getPlug("key")

    def testGetDictRaisesError(self):
        self.value.value = {}
        self.keyPlug.value = "test"
        self.assertIsNone(self.node.compute(self.output))

    def testGetDictFromKey(self):
        pass


class TestRemoveDict(unittest.TestCase):
    def setUp(self):
        self.node = get.GetKeyNode(name="getDict")
        self.output = self.node.getPlug("output")
        self.value = self.node.getPlug("value")
        self.keyPlug = self.node.getPlug("key")

    def testRemoveDictRaisesError(self):
        pass

    def testRemoveEntryByKey(self):
        pass
