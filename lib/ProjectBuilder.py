from .Project import Project
from .Logger import Log

from .CmakeGenerate import CmakeGenerate
from .CreateVariables import CreateVariables
from .CreateVariables import SwtichCaseCreateVariable
from .ImportProject import ImportProject

import json
import sys

class ProjectBuilder:
    def __init__(self):
        self._stepImpl = {}
        self.addStepClass(CmakeGenerate)
        self.addStepClass(CreateVariables)
        self.addStepClass(SwtichCaseCreateVariable)
        self.addStepClass(ImportProject)

    def addStepClass(self, stepClass):
        clName = stepClass.__name__
        if clName in self._stepImpl:
            msg = "Double registration of step class: {0}".format(clName)
            raise RuntimeError(msg)
        self._stepImpl[clName] = stepClass

    def build(self, projectFile):
        if len(projectFile) == 0:
            Log.error("Emtpy name of project file")
            return None
        node = None
        with open(projectFile, 'r') as fin:
            try:
                node = json.load(fin)
            except Exception as ex:
                Log.error("Can't parse project file {0}. Error: {1}".format(projectFile, repr(ex)))
                return None
            else:
                pass
        project = self._buildTree(node, projectFile)
        if project is None:
            Log.error("Can't load project from: {0}".format(projectFile))
            return None
        Log.info("Loaded project from: {0}".format(projectFile))
        return project

    def _createInputVariables(self, project, jsonNode):
        if "InputVariables" not in jsonNode:
            Log.error("Can't create input variable for project")
            return False
        inputVars = jsonNode["InputVariables"]
        ctx = project.getContext()
        for varName in inputVars.keys():
            ctx.addVariable(varName, inputVars[varName])
        return True

    def _createNode(self, stepName):
        if stepName not in self._stepImpl:
            return None
        return self._stepImpl[stepName]()

    def _createProject(self, jsonNode, projectFile):
        if "Project" not in jsonNode:
            Log.error("Can't find require node - 'Project'")
            return None
        projectName = jsonNode["Project"]
        if len(jsonNode["Project"]) == 0:
            Log.error("Empty name of project")
            return None
        project = Project(projectName)
        project.setProjectFile(projectFile)
        if not self._createInputVariables(project, jsonNode):
            return None
        return project

    def _createStep(self, jsonNode, projectContext):
        if "type" not in jsonNode:
            Log.error("Can't find required project's step 'type' node")
            return None
        stepType = jsonNode["type"]
        if "data" not in jsonNode:
            Log.error("Can't find required project's step 'data' node for step: {0}".format(stepType))
            return None
        node = self._createNode(stepType)
        if node is None:
            Log.error("Can't find implementation for step node type: {0}".format(stepType))
        return node, jsonNode["data"]

    def _buildTree(self, jsonNode, projectFile):
        project = self._createProject(jsonNode, projectFile)
        if project is None:
            return None
        if "Steps" not in jsonNode:
            Log.error("Can't find required 'Steps' node in project file")
            return None
        if len(jsonNode["Steps"]) == 0:
            Log.error("Empty steps list")
            return None
        ctx = project.getContext()
        for stepNode in jsonNode["Steps"]:
            stepNode, stepData = self._createStep(stepNode, ctx)
            if stepNode is None or stepData is None:
                return None
            else:
                project.addNode(stepNode, stepData)
        return project
