import unittest


def createTestSuites():
<<<<<<< Updated upstream
    tests = ["testEdge", "testGraph", "testBaseNodes", "testBasicMathNodes", "testPlug", "testEventHandler"]
=======
    tests = ["testEdge", "testGraph", "testBaseNodes", "testBasicMathNodes", "testPlug", "testTrigonometry",
             "testConversion", "testDict", "testString", "testArray", "testComparison", "testConstants"]
>>>>>>> Stashed changes

    suites = [unittest.defaultTestLoader.loadTestsFromName("ds.vortex.tests."+name) for name in tests]
    testSuite = unittest.TestSuite(suites)
    return testSuite


if __name__ == "__main__":
    from ds.vortex import customLogger

    logger = customLogger.getCustomLogger()
    unittest.TextTestRunner(verbosity=2).run(createTestSuites())
