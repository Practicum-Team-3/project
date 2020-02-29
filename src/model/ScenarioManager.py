import os
import json
from src.model.FileManager import FileManager
from src.model.Scenario import Scenario

class ScenarioManager(object):

    def __init__(self):
        self.file_manager = FileManager()

    def create_scenario(self, scenario_name):
        # Variables
        folders = ["JSON", "Exploit", "Vulnerability", "Machines"]
        scenario_path = self.file_manager.getScenarioPath() / scenario_name
        try:
            os.makedirs(scenario_path)
        except OSError:
            print("Creation of the directory %s failed" % scenario_path)
        else:
            print("Successfully created the directory %s" % scenario_path)
        for f in folders:
            path = scenario_path / f
            try:
                os.makedirs(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s" % path)
        scenario = Scenario(scenario_name)
        scenario.generateScenario(scenario_name)
        result = {"result": True}
        return result

    def get_scenarios(self):
        # Variables
        scenarios = os.listdir(self.file_manager.getScenarioPath())
        result = list()
        # Get scenarios names
        for scenario in scenarios:
            with open(self.file_manager.getScenarioPath() / scenario) as json_file:
                scenario_json = json.load(json_file)
            result.append(scenario_json["scenario_name"])
        scenarios_dict = {"scenarios": result}
        return scenarios_dict

