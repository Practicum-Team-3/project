from src.model.ScenarioManager import ScenarioManager
import json
import os

scenario_manager = ScenarioManager()

with open('/Users/dannerpacheco/Development/Practicum/Practicum-Team-3/project/src/model/testInput/changes.json') as f:
  new_scenario = json.load(f)
  exploit_info = new_scenario['exploit_info']
  json_string = json.dumps(exploit_info , indent = 1)
  print(json_string + "\n")

  scenario_manager.changeScenario("Scenario_3", new_scenario)

  scenario = scenario_manager.getScenario("Scenario_3")
  print(scenario)

  exploit_info = scenario['exploit_info']
  json_string = json.dumps(exploit_info , indent = 1)
  print(json_string)

  









  
  