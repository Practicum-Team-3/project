import os
import json
import shutil
from .FileManager import FileManager
from Entities.Scenario import Scenario

class ScenarioManager(object):

    def __init__(self):
        self.file_manager = FileManager()
        self.scenarios_dict = self._initializeScenarios()

    def _initializeScenarios(self):
        # Variables
        scenarios_dict = dict()
        scenarios = os.listdir(self.file_manager.getScenariosPath())
        for scenario_name in scenarios:
            json_name = ''.join([scenario_name , ".json"])
            with open(self.file_manager.getJSONPath(scenario_name) / json_name) as outfile:
                scenario_dict = json.load(outfile)
            scenario = Scenario(scenario_name).objectFromDictionary(scenario_dict)
            scenarios_dict[scenario_name] = scenario
        return scenarios_dict

    def newEmptyScenario(self, scenario_name):
        """
        Creates a new scenario which includes the folders and the scenario JSON file
        :param scenario_name: String with the scenario name
        :return: True if the new scenario was successfully created
        """
        #Folder creation moved to FileManager
        if scenario_name not in self.scenarios_dict:
            self.file_manager.createScenarioFolders(scenario_name)
            scenario = Scenario(scenario_name)
            self.scenarios_dict[scenario_name] = scenario
            self._saveScenarioAsJSON(scenario)
            return {"Response": True, "Note": "Operation successful", "Body": scenario.dictionary()}
        else:
            return {"Response": False, "Note": "Scenario already exist" , "Body": dict()}

    def getScenarios(self):
        """
        Gets the available scenarios
        :return: A list of strings with the available scenarios
        """
        # Variables
        scenarios_dict = {"scenarios": [self.scenarios_dict[s].scenario_name for s in self.scenarios_dict]}
        return {"Response": True, "Note": "Operation successful",
                "Body": scenarios_dict}

    def getScenario(self, scenario_name):
        """
        Gets the scenario as a JSON file
        :param scenario_name: String with the scenario name
        :return: JSON file with the scenario info
        """
        if scenario_name in self.scenarios_dict:
            return {"Response": True, "Note": "Operation successful",
                    "Body": self.scenarios_dict[scenario_name].dictionary()}
        else:
            return {"Response": False, "Note": "Scenario doesn't exist" , "Body": dict()}

    def editScenario(self, new_scenario):
        """
        Edits a current scenario with a JSON file
        :param scenario_name: String with the scenario name
        :param scenario_json: JSON file with the new scenario
        :return: True if the scenario has been successfully edited, otherwise False
        """
        scenario_name = new_scenario["scenario_name"]
        if scenario_name in self.scenarios_dict:
            new_scenario = Scenario(scenario_name).objectFromDictionary(new_scenario)
            self.scenarios_dict[scenario_name] = new_scenario
            self._saveScenarioAsJSON(new_scenario)
            return {"Response": True, "Note": "Operation successful", "Body": dict()}
        else:
            return {"Response": False, "Note": "Scenario doesn't exist", "Body": dict()}

    def deleteScenario(self, scenario_name):
        if scenario_name in self.scenarios_dict:
            deleted_scenario = self.scenarios_dict.pop(scenario_name)
            scenario_path = self.file_manager.getScenariosPath() / scenario_name
            try:
                shutil.rmtree(scenario_path)
            except OSError as e:
                print("Error: %s : %s" % (scenario_path, e.strerror))
            return {"Response": True, "Note": "Operation successful",
                    "Body": deleted_scenario.dictionary()}
        else:
            return {"Response": False, "Note": "Scenario doesn't exist" , "Body": dict()}

    def scenarioExists(self, scenario_name):
        """
        Check if a scenario exists
        :param scenario_name: String with the scenario name
        :return: False if the scenario JSON file does not exist and the path to the JSON file if it exist
        """
        scenario_dir_path = self.file_manager.getScenariosPath() / scenario_name / "JSON"
        if not os.path.isdir(scenario_dir_path):
            print("Scenario %s directory not found" % scenario_name)
            return False
        else:
            scenario_json_path = scenario_dir_path /  ''.join([scenario_name, ".json"])
            if not os.path.exists(scenario_json_path):
                print("Scenario %s json not found" % scenario_name)
                return None
            else:
                return scenario_json_path

    def _saveScenarioAsJSON(self, scenario):
        scenario_json_path = self.file_manager.getJSONPath(scenario.scenario_name) /  ''.join([scenario.scenario_name, ".json"])
        if scenario_json_path:
            with open(scenario_json_path, 'w+') as outfile:
                outfile.write(json.dumps(scenario.dictionary(), indent=2))
                outfile.close()
