from .Context import Context

class Project:
    def __init__(self, name):
        self._name = name
        self._ctx = Context()
        self._nodes = []

    def addNode(self, node):
        node.setProject(self)
        self._nodes.append(node)

    def run(self):
        for node in self._nodes:
            node.run()

    def setProjectFile(self, projectFile):
        self._ctx.addVariable("currentFile", projectFile)

    def getContext(self):
        return self._ctx
