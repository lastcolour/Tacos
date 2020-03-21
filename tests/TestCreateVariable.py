import unittest

from lib.CreateVariables import SwtichCaseCreateVariable
from lib.Project import Project
from lib.ProjectBuilder import ProjectBuilder

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

        switchCreate.serialize(data)
        self.assertTrue(switchCreate.run())

        varVal = project.getContext().getVariable("var")
        self.assertEqual(varVal, "1")

    def test_create_variable_require_format(self):
        projectData = {
            "Project":"Test",
            "InputVariables":{},
            "Steps":[
                {
                    "type":"CreateVariables",
                    "data":{
                        "var1":"a",
                        "var2":"${var1}/b"
                    }
                }
            ]
        }

        project = ProjectBuilder().buildFromData(projectData, ".")
        self.assertIsNotNone(project)
        self.assertTrue(project.run())

        ctx = project.getContext()
        varVal = ctx.getVariable("var2")
        self.assertEqual(varVal, "a/b")
