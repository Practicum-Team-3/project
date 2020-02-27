from model.VagrantFile import VagrantFile
import os
import json
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/scenarios/all')
def get_scenarios():
  #Variables
  current_path = Path.cwd()
  scenarios_path = current_path / "scenarios"
  scenarios = os.listdir(scenarios_path )
  result = list()
  #Get scenarios names
  for scenario in scenarios:
      with open( scenarios_path / scenario) as json_file:
        scenario_json = json.load(json_file)
      result.append(scenario_json["scenario_name"])
  scenarios_dict = { "scenarios" : result}
  return jsonify(scenarios_dict)
    
if __name__=="__main__":
  app.run()
  
  