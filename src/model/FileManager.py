from pathlib import Path

class FileManager(object):

    def __init__(self):
        #Paths
        self.current_path = Path.cwd()
        self.scenarios_path = self.current_path / "scenarios"

    def getCurrentPath(self):
        return self.current_path

    def getScenarioPath(self):
        return self.scenarios_path