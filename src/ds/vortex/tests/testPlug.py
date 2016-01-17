import unittest

from ds.vortex.core import plug as plugs


class TestPlug(unittest.TestCase):
    def setUp(self):
        self.plug = plugs.InputPlug(name="testName")

    def testIsInput(self):
        self.assertTrue(self.plug.isInput())
        self.assertFalse(self.plug.isOutput())

    def testConnect(self):
        inputAttr = plugs.InputPlug(name="testInput")
        outputAttr = plugs.OutputPlug(name="testOutput")
        self.plug.connect(outputAttr)
        self.assertEquals(self.plug.connections[0].name, self.plug.name + "_" + outputAttr.name)
        self.assertEquals(self.plug.connections[0].input, self.plug)
        self.assertEquals(self.plug.connections[0].output, outputAttr)
        self.assertTrue(self.plug.isConnected())
        self.assertTrue(outputAttr.isConnected())
        self.assertTrue(outputAttr.isConnectedTo(self.plug))
        self.assertEquals(outputAttr.getConnection(self.plug), self.plug.connections[0])
        #  failed to connect as plug already exists
        self.assertIsNone(self.plug.connect(inputAttr))

    def testDisconnect(self):
        floatTypeAttr = plugs.OutputPlug(name="testOutput")
        self.plug.connect(floatTypeAttr)
        self.plug.disconnect(floatTypeAttr)
        self.assertEquals(len(self.plug), 0)

    def testSerialize(self):
        pass


if __name__ == "__main__":
    from vortex import customLogger

    logger = customLogger.getCustomLogger()
    unittest.main(verbosity=2)
