from .Step import Step

class CopyFile(Step):
    def __init__(self):
        self._from = None
        self._to = None

    def serialize(self, jsonNode):
        self._from = jsonNode["from"]
        self._to = jsonNode["to"]

    def run(self):
        return True