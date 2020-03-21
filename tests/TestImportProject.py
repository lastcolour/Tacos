import unittest
import pathlib

import TestUtils

from lib.ProjectBuilder import ProjectBuilder

class TestImportProject(unittest.TestCase):

    def _getTestProjectPath(self):
        path = pathlib.Path(__file__).parent
        return "{0}/testData/testConfig/TestImportProject.json".format(path)

    @staticmethod
    def tearDownClass():
        TestUtils.RemoteTMPDir()

    def test_build_import_project(self):
        builder = ProjectBuilder()
        project = builder.build(self._getTestProjectPath(), None)
        self.assertIsNotNone(project)

        res = project.run()
        self.assertTrue(res)