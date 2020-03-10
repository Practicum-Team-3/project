from flask import Flask, jsonify, request
from model import ScenarioManager, VagrantManager

app = Flask(__name__)
scenario_manager = ScenarioManager()
vagrant_manager = VagrantManager()

@app.route('/scenarios/all')
def getScenarios():
  """

  :return:
  """
  return jsonify(scenario_manager.getScenarios())

@app.route('/scenarios/<scenario_name>')
def getScenario(scenario_name):
  """

  :param scenario_name:
  :return:
  """
  return jsonify(scenario_manager.getScenario(scenario_name))

@app.route('/scenarios/edit/<scenario_name>', methods = ['POST'])
def editScenario(scenario_name ):
  """

  :param scenario_name:
  :return:
  """
  return jsonify(scenario_manager.editScenario(scenario_name ,  request.get_json()))

@app.route('/scenarios/new/<scenario_name>')
def createScenario(scenario_name):
  """

  :param scenario_name:
  :return:
  """
  return jsonify(scenario_manager.createScenario(scenario_name))

@app.route('/boxes/all')
def getAvailableBoxes():
  """

  :return:
  """
  return jsonify(vagrant_manager.getAvailableBoxes())

@app.route('/vagrantFiles/<scenario_name>/all')
def createVagrantFiles(scenario_name):
  """

  :param scenario_name:
  :return:
  """
  return jsonify(vagrant_manager.createVagrantFiles(scenario_name))

@app.route('/vagrantFiles/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """

  :param scenario_name:
  :return:
  """
  return jsonify(vagrant_manager.runVagrantUp(scenario_name))

@app.route('/scenarios/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  return jsonify(vagrant_manager.testNetworkPing(scenario_name, source, destination))



if __name__=="__main__":
  app.run()