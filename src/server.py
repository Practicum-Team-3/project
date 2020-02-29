import os
import json
from pathlib import Path
from flask import Flask, jsonify
import subprocess
import re
from src.model.Scenario import Scenario

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


@app.route('/boxes/all')
def get_available_boxes():
  #Variables
  current_path = Path.cwd()
  boxes_path = current_path / "boxes"
  boxes = {}
  boxNum = 0
  boxlist = subprocess.check_output("vagrant box list", shell=True)
  boxlist = str(boxlist)
  boxlist = re.sub(r"(^[b']|'|\s(.*?)\\n)", " " , boxlist)
  boxlist = boxlist.split(" ")
  boxlist = filter(None, boxlist)

  print("Loading available Vanilla VMs")

  for boxName in boxlist:
    boxNum = boxNum + 1
    boxes[boxNum] = boxName
    print("[ " + str(boxNum) + " ]" + boxName)
  return jsonify(boxes)

@app.route('/scenarios/new/<scenario_name>')
def create_scenario(scenario_name):
  #Variables
  folders = ["JSON" , "Exploit" , "Vulnerability" , "Machines" ]
  current_path = Path.cwd()
  scenario_path = current_path / "scenarios" / scenario_name
  try:
    os.makedirs(scenario_path )
  except OSError:
    print ("Creation of the directory %s failed" % scenario_path)
  else:
    print ("Successfully created the directory %s" % scenario_path)
  for f in folders:
    path = scenario_path / f
    try:
      os.makedirs(path)
    except OSError:
      print ("Creation of the directory %s failed" % path)
    else:
      print ("Successfully created the directory %s" % path)
  scenario = Scenario(scenario_name)
  scenario.generateScenario(scenario_name)
  result = { "result" : True}
  print(result)
  return jsonify(result)

if __name__=="__main__":
  #create_scenario("Scenario_1")
  app.run()
  
  