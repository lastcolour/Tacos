import sys
import os
import pathlib

import unittest
import TestUtils

from lib.ProjectBuilder import ProjectBuilder
from lib.Step import Step
from lib.Logger import Log

class TestSerializeData(Step):

    JSON_NODE = {}

    def __init__(self):
        Step.__init__(self)
        self.node = None

    def serialize(self, jsonNode):
        TestSerializeData.JSON_NODE = jsonNode

    def run(self):
        return True

class TestProjectBuilder(unittest.TestCase):

    LOG_LVL_TO_RESOTRE = None

    def _writeContentToTempFile(self, content):
        with open(self._getPathToTempFile(), 'w') as fout:
            fout.write(content)

    def _getPathToTempFile(self):
        return "{0}/tempFile.tmp".format(TestUtils.CreateAndGetTMPDir())

    def tearDown(self):
        if os.path.exists(self._getPathToTempFile()):
            os.remove(self._getPathToTempFile())

    @staticmethod
    def setUpClass():
        import logging
        TestProjectBuilder.LOG_LVL_TO_RESOTRE = Log.getEffectiveLevel()
        Log.setLevel(logging.FATAL)

    @staticmethod
    def tearDownClass():
        Log.setLevel(TestProjectBuilder.LOG_LVL_TO_RESOTRE)
        TestUtils.RemoteTMPDir()

    def test_invalid_project(self):
        builder = ProjectBuilder()
        project = builder.build("", None)
        self.assertIsNone(project)

    def test_empty_project_file(self):
        self._writeContentToTempFile('')
        builder = ProjectBuilder()
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNone(project)

    def test_empty_project_name(self):
        self._writeContentToTempFile('{"Project":"", "Steps":[]}')
        builder = ProjectBuilder()
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNone(project)

    def test_empty_steps(self):
        self._writeContentToTempFile('{"Project":"TestProject", "Steps":[]}')
        builder = ProjectBuilder()
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNone(project)

    def test_no_steps(self):
        self._writeContentToTempFile('{"Project":"TestProject"}')
        builder = ProjectBuilder()
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNone(project)

    def test_invalid_step_node(self):
        self._writeContentToTempFile('{"Project":"TestProject", "Steps":[{"type":"Invalid","data":{}}]}')
        builder = ProjectBuilder()
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNone(project)

    def test_normal_project(self):
        self._writeContentToTempFile('{"Project":"TestProject", "InputVariables":{}, "Steps":[{"type":"CreateVariables","data":{"one":1}}]}')
        builder = ProjectBuilder()
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNotNone(project)

    def test_context_format_step_data(self):
        self._writeContentToTempFile('{"Project":"TestProject", "InputVariables":{}, "Steps":[{"type":"TestSerializeData","data":{"test_var":"${currentDir}"}}]}')
        builder = ProjectBuilder()
        builder.addStepClass(TestSerializeData)
        project = builder.build(self._getPathToTempFile(), None)
        self.assertIsNotNone(project)
        project.run()

        self.assertEqual(len(TestSerializeData.JSON_NODE), 1)
        self.assertIn("test_var", TestSerializeData.JSON_NODE)

        currentDir = pathlib.Path(self._getPathToTempFile()).parent.__str__()
        self.assertEqual(TestSerializeData.JSON_NODE["test_var"], currentDir)