from src.model.ScenarioManager import ScenarioManager
from src.model.VagrantManager import VagrantManager

if __name__ == "__main__":
    scenario_manager = ScenarioManager()
    vagrant_manager = VagrantManager()
    print(scenario_manager.scenarioExists("Scenario_3"))
    print(scenario_manager.getScenario("Scenario_3"))
    print(scenario_manager.editScenario("Scenario_3"))