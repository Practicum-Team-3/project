import sys
import os
from pathlib import Path

class FileManager(object):

    def __init__(self):
        #Paths
        self.current_path = Path.cwd()
        self.scenarios_path = self.current_path / "scenarios"

    def getCurrentPath(self):
        return self.current_path

    def getScenariosPath(self):
        return self.scenarios_path

    def createScenarioFolders(self, scenario_name):
        # Variables
        folders = ["JSON", "Exploit", "Vulnerability", "Machines"]
        scenario_path = self.getScenariosPath() / scenario_name
        try:
            os.makedirs(scenario_path)
        except OSError:
            print("Creation of the directory %s failed" % scenario_path)
        else:
            print("Successfully created the directory %s" % scenario_path)
        for f in folders:
            path = scenario_path / f
            try:
                os.makedirs(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s" % path)
        result = {"result": True}
        return result

    def createMachines(self, scenario):
        #Response message for the requester
        reponse = {"result": True, "reason": ""}
        try:
            machines = scenario['machines']
            scenario_name = scenario['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                path = machines_path / machine_name

                if os.path.isdir(path):
                    print("Folder already exists")
                else:
                    os.makedirs(path)
            
        except KeyError as key_not_found:
            print("%s has not been defined" % key_not_found)
            reponse["result"] = False
            reponse["reason"] = key_not_found + " has not been defined" 

        except OSError:
            print("Creation of machines directory failed")
            reponse["result"] = False
            reponse["reason"] = "OS Error" 
        except:
            print("Unexpected error:", sys.exc_info()[0])
        else:
            print("Creation of machines directory succesful")
        
        return reponse