from src.model.ScenarioManager import ScenarioManager
from src.model.VagrantManager import VagrantManager

if __name__ == "__main__":
    scenario_manager = ScenarioManager()
    vagrant_manager = VagrantManager()
    json_file = scenario_manager.getScenario("Scenario_3")
    scenario_manager.editScenario("Scenario_3", json_file)
    vagrant_manager.createVagrantFiles(json_file)