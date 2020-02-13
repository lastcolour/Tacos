from lib.ProjectBuilder import ProjectBuilder

def run():
    builder = ProjectBuilder()
    project = builder.build("")
    project.run()

if __name__ == "__main__":
    run()