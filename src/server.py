from model.VagrantFile import VagrantFile
import os
import json
from pathlib import Path
from flask import Flask, jsonify
import subprocess
import re

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


@app.route('/boxes')
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
    
if __name__=="__main__":
  app.run()
  
  