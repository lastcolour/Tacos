from lib.ProjectBuilder import ProjectBuilder
from lib.ParseArgs import ParseArgs

def run():
    projectName, inputVariables = ParseArgs()
    if projectName is None:
        return
    builder = ProjectBuilder()
    project = builder.build(projectName, inputVariables)
    if project is None:
        return
    project.run()

if __name__ == "__main__":
    run()