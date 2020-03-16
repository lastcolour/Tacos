from .Step import Step

class ImportProject(Step):
    def __init__(self):
        Step.__init__(self)
        self._projectFile = None

    def serialize(self, jsonData):
        self._projectFile = jsonData["project_file"]
        return True

    def run(self):
        from .ProjectBuilder import ProjectBuilder
        builder = ProjectBuilder()
        project = builder.build(self._projectFile)
        if not project:
            return False
        project.setParentContext(self._getContext())
        return project.run()