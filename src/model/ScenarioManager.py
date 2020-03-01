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
        scenarios_dict = {"scenarios": scenarios}
        return scenarios_dict


    def scenarioExists(self, scenario_name):

        #quickFix = scenario_name + "/JSON"
        scenario_dir_path = self.file_manager.getScenarioPath() / scenario_name / "JSON"
        print("TEST: %s " % scenario_dir_path)
        if not os.path.isdir(scenario_dir_path):
            print("Scenario %s directory not found" % scenario_name)
            return False
        else:
            scenario_json_path = scenario_dir_path /  scenario_name / ".json"
            if not os.path.exists(scenario_json_path):
                print("Scenario %s json not found" % scenario_name)
                return False
            else:
                return scenario_json_path


    def getScenario(self, scenario_name):
        
        scenario_json_path = self.scenarioExists(scenario_name)
        scenario_json = dict()
        try:
            with open(scenario_json_path) as json_file:
                scenario_json = json.load(json_file)
                return scenario_json

        except:
            print("Something went wrong while retrieving Scenario JSON")

    
    def changeScenario(self, scenario_name, new_scenario_json):
        scenario_json_path = self.scenarioExists(scenario_name)
        with open(scenario_json_path, 'w+') as outfile:
          json.dump(scenario_json_path, outfile)


