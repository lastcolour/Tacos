import unittest

import lib.ParseArgs as PA

class TestParseArgs(unittest.TestCase):
    def test_only_project_in_args_0(self):
        projectName, startIdx = PA._extractProjectName(["--project", "Test"], 0)
        self.assertEqual(projectName, "Test")
        self.assertEqual(startIdx, 2)


    def test_only_project_in_args_1(self):
        projectName, startIdx = PA._extractProjectName(["--project:Test"], 0)
        self.assertEqual(projectName, "Test")
        self.assertEqual(startIdx, 1)

    def test_only_project_in_args_2(self):
        projectName, startIdx = PA._extractProjectName(["--project=Test"], 0)
        self.assertEqual(projectName, "Test")
        self.assertEqual(startIdx, 1)

    def test_no_project_name_in_args(self):
        projectName, startIdx = PA._extractProjectName(["--project:"], 0)
        self.assertEqual(projectName, None)
        self.assertEqual(startIdx, 0)

    def test_project_name_quoted(self):
        projectName, startIdx = PA._extractProjectName(["--project", "\"Test\""], 0)
        self.assertEqual(projectName, "Test")
        self.assertEqual(startIdx, 2)