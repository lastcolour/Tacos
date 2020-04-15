from .Step import Step

class ImportProject(Step):
    def __init__(self):
        Step.__init__(self)
        self._projectFile = None

    def serialize(self, jsonData):
        self._projectFile = jsonData["project_file"]

    def run(self):
        from lib.ProjectBuilder import ProjectBuilder
        builder = ProjectBuilder()
        project = builder.build(self._projectFile, None)
        if not project:
            return False
        project.setParent(self._project)
        return project.run()