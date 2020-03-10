from flask import Flask, jsonify, request
from model.ScenarioManager import ScenarioManager
from model.VagrantManager import VagrantManager

app = Flask(__name__)
scenario_manager = ScenarioManager()
vagrant_manager = VagrantManager()

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
  Create a new scenario as well as the folders for that scenario
  :param scenario_name: String with the scenario name
  :return: True if the new scenario was successfully created
  """
  return jsonify(scenario_manager.createScenario(scenario_name))

@app.route('/boxes/all')
def getAvailableBoxes():
  """
  Gets the available boxes in the Vagrant context
  :return: A list of string with the available boxes
  """
  return jsonify(vagrant_manager.getAvailableBoxes())

@app.route('/vagrantFiles/<scenario_name>/all')
def createVagrantFiles(scenario_name):
  """
  Create the vagrant files for the existing machines in the scenario
  :param scenario_name: String with the sceanrio name
  :return: True if the files were successfully created
  """
  return jsonify(vagrant_manager.createVagrantFiles(scenario_name))

@app.route('/vagrantFiles/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name:
  :return: True if the vagrant up commands were successfully executed
  """
  return jsonify(vagrant_manager.runVagrantUp(scenario_name))

if __name__=="__main__":
  app.run()