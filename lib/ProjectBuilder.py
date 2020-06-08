from .Project import Project
from .Logger import Log

from .steps.CmakeGenerate import CmakeGenerate
from .steps.CreateVariables import CreateVariables
from .steps.CreateVariables import SwtichCaseCreateVariable
from .steps.ImportProject import ImportProject
from .steps.CopyFile import CopyFile, CopyCompiledBinaries
from .steps.IfVariable import IfVariableEqual, IfVariableInSet
from .steps.RunExecutable import RunExecutable
from .steps.PyTests import PyTests

import json
import sys
import os
from collections import OrderedDict
import platform

class ProjectBuilder:
    def __init__(self):
        self._stepImpl = {}
        self._stepNames = set()
        self.addStepClass(CmakeGenerate)
        self.addStepClass(CreateVariables)
        self.addStepClass(SwtichCaseCreateVariable)
        self.addStepClass(ImportProject)
        self.addStepClass(CopyFile)
        self.addStepClass(CopyCompiledBinaries)
        self.addStepClass(IfVariableEqual)
        self.addStepClass(IfVariableInSet)
        self.addStepClass(RunExecutable)
        self.addStepClass(PyTests)

    def addStepClass(self, stepClass):
        clName = stepClass.__name__
        if clName in self._stepImpl:
            msg = "Double registration of step class: {0}".format(clName)
            raise RuntimeError(msg)
        self._stepImpl[clName] = stepClass

    def build(self, projectFile, inputVariables):
        if len(projectFile) == 0:
            Log.error("Emtpy name of project file")
            return None
        if not os.path.isabs(projectFile):
            projectFile = "{0}/{1}".format(os.getcwd(), projectFile)
        projectFile = projectFile.replace("\\", "/")
        if not os.path.exists(projectFile):
            Log.error("Can't find specified project file: {0}".format(projectFile))
            return None
        Log.info("Load project from: {0}".format(projectFile))
        node = None
        with open(projectFile, 'r') as fin:
            try:
                node = json.load(fin, object_pairs_hook=OrderedDict)
            except Exception as ex:
                Log.error("Can't parse project file. Error: {0}".format(repr(ex)))
                return None
            else:
                pass
        return self.buildFromData(node, projectFile)

    def buildFromData(self, data, dataFile):
        project = self._buildTree(data, dataFile)
        if project is None:
            Log.error("Can't build project")
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

    def _createNode(self, stepType, stepName):
        if stepType not in self._stepImpl:
            return None
        stepCls = self._stepImpl[stepType]
        stepNode = stepCls()
        stepNode.setName(stepName)
        return stepNode

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
        project.setCurrentPlatform(platform.system())
        if not self._createInputVariables(project, jsonNode):
            return None
        return project

    def _createStep(self, jsonNode):
        if "name" not in jsonNode:
            Log.error("Can't find required project's step 'name' node")
            return None
        stepName = jsonNode["name"]
        if len(stepName) == 0:
            Log.error("Step name can't be empty")
            return None
        if stepName in self._stepNames:
            Log.error("Found dublicate step name: {0}".format(stepName))
            return None
        if "type" not in jsonNode:
            Log.error("Can't find required project's step 'type' node")
            return None
        stepType = jsonNode["type"]
        if "data" not in jsonNode:
            Log.error("Can't find required project's step 'data' node for step: {0}".format(stepType))
            return None
        node = self._createNode(stepType, stepName)
        if node is None:
            Log.error("Can't find implementation for step node type: {0}".format(stepType))
        if "dependOn" in jsonNode:
            for depStepName in jsonNode["dependOn"]:
                if depStepName == stepName:
                    Log.error("Step can't depend on self: {0}".format(stepName))
                    return None
                if len(depStepName) == 0:
                    Log.error("Step dependency name can't be empty")
                    return None
                if depStepName not in self._stepNames:
                    Log.error("Can't find dependecy: '{0}' for step: {1}".format(depStepName, stepName))
                    return None
                node.addDependecy(depStepName)
        self._stepNames.add(stepName)
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
        for stepNode in jsonNode["Steps"]:
            stepNode, stepData = self._createStep(stepNode)
            if stepNode is None or stepData is None:
                Log.error("Step: {0}".format(stepNode))
                return None
            else:
                project.addNode(stepNode, stepData)
        return project
