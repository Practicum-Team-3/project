from flask import Flask, jsonify, request, url_for
from model.ScenarioManager import ScenarioManager
from model.VagrantManager import VagrantManager

from celery import Celery

app = Flask(__name__)
scenario_manager = ScenarioManager()
vagrant_manager = VagrantManager()

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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
  :param scenario_name: String with the scenario name
  :return: True if the files were successfully created
  """
  return jsonify(vagrant_manager.createVagrantFiles(scenario_name))

@app.route('/vagrantFiles/<scenario_name>/run')
def runVagrantUp(scenario_name):
  """
  Executes the vagrant up command for each machine in the scenario
  :param scenario_name: String with the scenario name
  :return: True if the vagrant up commands were successfully executed
  """
  return jsonify(vagrant_manager.runVagrantUp(scenario_name))

@celery.task(bind=True)
def testCelery(self,scenario_name, source, destination):
  return vagrant_manager.testNetworkPing(scenario_name, source, destination)
  


@app.route('/scenarios/<scenario_name>/ping/<source>/<destination>')
def testPing(scenario_name, source, destination):
  """
  Tests network connectivity between two virtual machines
  :param scenario_name: String with the scenario name
  :param source: Source virtual machine
  :param destination: Destination virtual machine
  :return:
  """
  task = testCelery.apply_async(scenario_name, source, destination)
  return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}
  
@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)




if __name__=="__main__":
  app.run()