from .Context import Context

import pathlib

class Project:
    def __init__(self, name):
        self._name = name
        self._ctx = Context()
        self._nodes = []

    def addNode(self, nodeObj, nodeData):
        self._nodes.append( (nodeObj, nodeData) )

    def run(self):
        for nodeObj, nodeData in self._nodes:
            nodeObj.setProject(self)
            nodeData = self._ctx.createStepNode(nodeData)
            nodeObj.serialize(nodeData)
            nodeObj.run()
        return True

    def setProjectFile(self, projectFile):
        parentDirPath = pathlib.Path(projectFile).parent.__str__()
        self._ctx.addVariable("currentDir", parentDirPath)

    def setParentContext(self, parentCtx):
        self._ctx.setParentContext(parentCtx)

    def getContext(self):
        return self._ctx
