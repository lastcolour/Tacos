from .Context import Context
from .Logger import Log

import pathlib
import timeit

def _convertDuration(duration):
    if duration < 0.1:
        scaledDuration = duration * 100.0
        scaledDuration = "{0:.1f} ms".format(scaledDuration)
    elif duration > 100:
        scaledDurationMin = int(duration // 60)
        scaledDurationSec = int((duration % 60))
        scaledDuration = "{0} min {1} s".format(scaledDurationMin, scaledDurationSec)
    else:
        scaledDuration = "{0:.2f} s".format(duration)
    return scaledDuration

class _NodeStats:
    def __init__(self):
        self._skipped = 0
        self._successed = 0
        self._failed = 0

class Project:
    def __init__(self, name):
        self._name = name
        self._ctx = Context()
        self._nodes = []
        self._parent = None
        self._depth = 0
        self._nodeStats = _NodeStats()
        self._nodesRunRes = {}

    def addNode(self, nodeObj, nodeData):
        self._nodes.append( (nodeObj, nodeData) )

    def run(self):
        Log.info("{0}Start run project: '{1}'".format(self._getLogOffset(), self._name))
        startT = timeit.default_timer()
        for idx in range(len(self._nodes)):
            node = self._nodes[idx]
            nodeObj = node[0]
            nodeData = node[1]
            res = self._runNode(nodeObj, nodeData, idx)
            self._nodesRunRes[nodeObj.getName()] = res
        Log.info("{0}Successed: {1}, Skipped: {2}, Failed: {3}".format(
            self._getLogOffset(), self._nodeStats._successed, self._nodeStats._skipped, self._nodeStats._failed))
        Log.info("{0}Project Completed. (Duration: {1})".format(
            self._getLogOffset(),
            _convertDuration(timeit.default_timer() - startT)))
        return True

    def setProjectFile(self, projectFile):
        if projectFile is None:
            Log.debug("Create internal project")
            return
        parentDirPath = pathlib.Path(projectFile).parent.__str__()
        self._ctx.addVariable("currentDir", parentDirPath)

    def setCurrentPlatform(self, currentPlatform):
        self._ctx.addVariable("currentPlatform", currentPlatform)

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
        Log.info("{0}[{1}/{2}] Run step: '{3}' (Impl: '{4}')".format(
            self._getLogOffset(),
            nodeIdx + 1,
            len(self._nodes),
            nodeObj.getName(),
            type(nodeObj).__name__))

    def _printStepEnd(self, nodeRes, nodeDuration):
        resMsg = "Step Successed."
        if nodeRes is False:
           resMsg = "Step Failed!"
        Log.info("{0}{1} (Duration: {2})".format(
            self._getLogOffset(),
            resMsg,
            _convertDuration(nodeDuration)))

    def _printSkipNode(self, nodeObj, nodeIdx, depNodeName):
        Log.info("{0}[{1}/{2}] Skip step: '{3}' (Impl: '{4}')".format(
            self._getLogOffset(),
            nodeIdx + 1,
            len(self._nodes),
            nodeObj.getName(),
            type(nodeObj).__name__))
        Log.info("{0}Dependecy failed: {1}".format(
            self._getLogOffset(),
            depNodeName))

    def _trySkipNode(self, nodeObj, nodeIdx):
        for depNodeName in nodeObj.getDependecies():
            if depNodeName not in self._nodesRunRes:
                raise RuntimeError("Step depend on node that runs after")
            depRes = self._nodesRunRes[depNodeName]
            if depRes is not True:
                self._printSkipNode(nodeObj, nodeIdx, depNodeName)
                return True
        return False

    def _runNode(self, nodeObj, nodeData, nodeIdx):
        if self._trySkipNode(nodeObj, nodeIdx):
            self._nodeStats._skipped += 1
            return None
        self._printStepStart(nodeObj, nodeIdx)
        startT = timeit.default_timer()
        res = self._runNodeImpl(nodeObj, nodeData)
        if res:
            self._nodeStats._successed += 1
        else:
            self._nodeStats._failed += 1
        self._printStepEnd(res, timeit.default_timer() - startT)
        return res