from flask import Flask, jsonify, request
from .Managers import ScenarioManager

app = Flask(__name__)
scenario_manager = ScenarioManager()

@app.route('/scenarios/all')
def getScenarios():
  """
  Gets the available scenarios
  :return: A list of strings with the available scenarios
  """
  return jsonify(scenario_manager.getScenarios())

@app.route('/scenarios/<scenario_name>')
def getScenario(scenario_name):
  """
  Gets the scenario as a JSON file
  :param scenario_name: String with the scenario name
  :return: JSON file with the scenario info
  """
  return jsonify(scenario_manager.getScenario(scenario_name))

@app.route('/scenarios/edit/<scenario_name>', methods = ['POST'])
def editScenario(scenario_name ):
  """
  Edits a current scenario with a JSON file
  :param scenario_name: String with the scenario name
  :return: True if the scenario has been successfully edited, otherwise False
  """
  return jsonify(scenario_manager.editScenario(scenario_name ,  request.get_json()))

@app.route('/scenarios/new/<scenario_name>')
def createScenario(scenario_name):
  """
  Creates a new scenario which includes the folders and the scenario JSON file
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(scenario_manager.createScenario(scenario_name))

if __name__=="__main__":
  app.run(port=5000)