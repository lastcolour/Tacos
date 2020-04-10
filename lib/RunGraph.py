class RunState:
    NotStarted = 0
    InProgress = 1
    Failed = 2
    Succesed = 3

class RunNode:
    def __init__(self):
        self._state = RunState.NotStarted
        self._children = []

    def _getChildren(self):
        return self._children

    def setState(self, state):
        self._state = state

    def getState(self):
        return self._state

class RunSequence(RunNode):
    def __init__(self):
        super().__init__()

    def run(self):
        self.setState(RunState.InProgress)
        for item in self._getChildren():
            item.run()
            if item.getState() == RunState.Failed:
                self.setState(RunState.Failed)
                return
        self.setState(RunState.Succesed)

class RunGraph:
    def __init__(self):
        pass