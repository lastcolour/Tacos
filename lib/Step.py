class Step:
    def __init__(self):
        self._project = None

    def serialize(self, node):
        raise NotImplementedError

    def setProject(self, project):
        self._project = project

    def _getContext(self):
        return self._project.getContext()

    def _getProject(self):
        return self._project

    def needUseSoftCtxFormat(self):
        return False