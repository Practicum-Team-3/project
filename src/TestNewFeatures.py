from model.ScenarioManager import ScenarioManager
from model.VagrantManager import VagrantManager

if __name__ == "__main__":
    scenario_manager = ScenarioManager()
    test= scenario_manager.getScenarios()
    vagrant_manager = VagrantManager()
    #scenario_name = "Scenario_1"
    #json_file = scenario_manager.getScenario(scenario_name)
    #scenario_manager.editScenario(scenario_name, json_file)
    #vagrant_manager.createVagrantFiles(scenario_name)
    #vagrant_manager.runVagrantUp(scenario_name)
