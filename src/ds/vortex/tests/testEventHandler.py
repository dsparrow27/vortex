import unittest

from ds.vortex import customLogger
from ds.vortex.core import vortexEvent


class TestEventHandler(unittest.TestCase):
    def setUp(self):
        self.handler = vortexEvent.VortexSignal()

    def testSignalConnectWithoutArgs(self):
        self.handler.connect(self.signalTestFunc)
        self.assertEquals(len(self.handler), 1)
        self.handler.emit()

    def testSignalConnectWithArgs(self):
        self.handler.connect(self.signalTestFunc)
        self.handler.emit(False)

    def testSignalRemove(self):
        self.handler.connect(self.signalTestFunc)
        self.assertEquals(len(self.handler), 1)
        self.handler.removeEvent(self.signalTestFunc)
        self.assertEquals(len(self.handler), 0)

    def signalTestFunc(self, testArg=True):
        return testArg


if __name__ == "__main__":
    customLogger.getCustomLogger()
    unittest.main(verbosity=2)
