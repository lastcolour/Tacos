class Step:
    def __init__(self):
        self._name = None
        self._project = None
        self._dependecies = []

    def serialize(self, node):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def setProject(self, project):
        self._project = project

    def setName(self, name):
        self._name = name

    def addDependecy(self, dependecy):
        self._dependecies.append(dependecy)

    def getName(self):
        return self._name

    def getDependecies(self):
        return self._dependecies

    @property
    def context(self):
        return self._project.getContext()

    def needUseSoftCtxFormat(self):
        return False