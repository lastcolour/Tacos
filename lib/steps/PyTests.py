from .Step import Step

import unittest

class PyTests(Step):
    def __init__(self):
        Step.__init__(self)
        self._path = None
        self._pattern = None

    def serialize(self, jsonData):
        self._path = jsonData["path"]
        self._pattern = jsonData["pattern"]

    def run(self):
        loader = unittest.TestLoader()
        testSuite = loader.discover(self._path, self._pattern)
        testRunner = unittest.TextTestRunner(verbosity=2)
        suiteRes = testRunner.run(testSuite)
        return suiteRes.wasSuccessful()