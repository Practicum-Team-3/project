import os
import json
from src.model.FileManager import FileManager
from src.model.Scenario import Scenario

class ScenarioManager(object):

    def __init__(self):
        self.file_manager = FileManager()

    def create_scenario(self, scenario_name):
        
        #Folder creation moved to FileManager
        self.file_manager.createScenarioFolders(scenario_name)
        scenario = Scenario(scenario_name)
        scenario.generateScenario(scenario_name)
        result = {"result": True}
        return result

    def get_scenarios(self):
        # Variables
        scenarios = os.listdir(self.file_manager.getScenarioPath())
        scenarios_dict = {"scenarios": scenarios}
        return scenarios_dict

