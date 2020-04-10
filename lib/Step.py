class Step:
    def __init__(self):
        self._name = None
        self._project = None

    def serialize(self, node):
        raise NotImplementedError

    def setProject(self, project):
        self._project = project

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    @property
    def context(self):
        return self._project.getContext()

    def needUseSoftCtxFormat(self):
        return False