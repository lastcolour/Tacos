from .Context import Context
from .Logger import Log

import pathlib
import timeit

class Project:
    def __init__(self, name):
        self._name = name
        self._ctx = Context()
        self._nodes = []
        self._parent = None
        self._depth = 0

    def addNode(self, nodeObj, nodeData):
        self._nodes.append( (nodeObj, nodeData) )

    def run(self):
        Log.info("Start run project: {0}".format(self._name))
        for idx in range(len(self._nodes)):
            node = self._nodes[idx]
            nodeObj = node[0]
            nodeData = node[1]
            res = self._runNode(nodeObj, nodeData, idx)
            if res is not True:
                return False
        return True

    def setProjectFile(self, projectFile):
        parentDirPath = pathlib.Path(projectFile).parent.__str__()
        self._ctx.addVariable("currentDir", parentDirPath)

    def setParent(self, parent):
        self._parent = parent
        self._depth = parent._depth + 1
        self._ctx.setParentContext(self._parent._ctx)

    def getContext(self):
        return self._ctx

    def _getLogOffset(self):
        return "  " * self._depth

    def _runNodeImpl(self, nodeObj, nodeData):
        if nodeObj.needUseSoftCtxFormat():
            nodeData = self._ctx.createStepNodeSoft(nodeData)
        else:
            nodeData = self._ctx.createStepNode(nodeData)

        nodeObj.setProject(self)
        nodeObj.serialize(nodeData)
        return nodeObj.run()

    def _printStepStart(self, nodeObj, nodeIdx):
        Log.info("{0}[{1}/{2}] Run step: {3} (Impl: {4})".format(
            self._getLogOffset(),
            nodeIdx + 1,
            len(self._nodes),
            nodeObj.getName(),
            type(nodeObj).__name__))

    def _printStepEnd(self, nodeRes, nodeDuration):
        durationScale = "s"
        if nodeDuration < 0.1:
            nodeDuration = nodeDuration * 100.0
            durationScale = "ms"
        resMsg = "Success."
        if nodeRes is False:
           resMsg = "Fail!"
        Log.info("{0}{1} Duration: {2:.2f}{3}".format(
            self._getLogOffset(),
            resMsg,
            nodeDuration,
            durationScale))

    def _runNode(self, nodeObj, nodeData, nodeIdx):
        self._printStepStart(nodeObj, nodeIdx)
        startT = timeit.default_timer()
        res = self._runNodeImpl(nodeObj, nodeData)
        self._printStepEnd(res, timeit.default_timer() - startT)
        return res