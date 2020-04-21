from .Step import Step

class RunProcess(Step):
    def __init__(self):
        Step.__init__(self)
        self._cwd = None
        self._process = None
        self._args = None

    def serialize(self, jsonNode):
        self._process = jsonNode["process"]
        self._cwd = jsonNode["cwd"]
        self._args = jsonNode["args"]

    def run(self):
        return True