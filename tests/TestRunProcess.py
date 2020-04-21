from lib.steps.RunProcess import RunProcess

import unittest

import TestUtils

class TestRunProcess(unittest.TestCase):
    def test_run_invalid_process(self):
        data = {
            "cwd":"",
            "process":"win_dir",
            "args":[
            ]
        }
        runProcess = RunProcess()
        runProcess.serialize(data)
        self.assertFalse(runProcess.run())

    def test_run_valid_process(self):
        data = {
            "cwd":"",
            "process":"dir",
            "args":[
            ]
        }
        runProcess = RunProcess()
        runProcess.serialize(data)
        self.assertFalse(runProcess.run())