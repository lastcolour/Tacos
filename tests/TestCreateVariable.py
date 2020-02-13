import unittest

from lib.CreateVariables import SwtichCaseCreateVariable
from lib.Project import Project

class TestCreateVariable(unittest.TestCase):

    def test_switch_create(self):
        data = {
            "variable":"${a}",
            "cases":{
                "b":{
                    "var":"1"
                },
                "c":{
                    "var":"2"
                }
            }
        }

        project = Project("Test")
        ctx = project.getContext()
        ctx.addVariable("a", "b")
        ctx.createStepNode(data)

        self.assertIsNone(ctx.getVariable("var"))

        switchCreate = SwtichCaseCreateVariable()
        switchCreate.setProject(project)

        self.assertTrue(switchCreate.init())
        self.assertTrue(switchCreate.serialize(data))
        self.assertTrue(switchCreate.run())

        varVal = project.getContext().getVariable("var")
        self.assertEqual(varVal, "1")
