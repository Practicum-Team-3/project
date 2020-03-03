from flask import Flask, jsonify
from model.ScenarioManager import ScenarioManager
from model.VagrantManager import VagrantManager

app = Flask(__name__)
scenario_manager = ScenarioManager()
vagrant_manager = VagrantManager()

@app.route('/scenarios/all')
def get_scenarios():
  return jsonify(scenario_manager.get_scenarios())


@app.route('/boxes/all')
def get_available_boxes():
  return jsonify(vagrant_manager.get_available_boxes())

@app.route('/scenarios/new/<scenario_name>')
def create_scenario(scenario_name):
  return jsonify(scenario_manager.create_scenario(scenario_name))

if __name__=="__main__":
  app.run()
  
  