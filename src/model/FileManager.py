import sys
import os
from pathlib import Path

class FileManager(object):

    def __init__(self):
        #Paths
        self.current_path = Path.cwd()
        self.scenarios_path = self.current_path / "src" /"scenarios"

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

    def createMachineFolders(self, scenario_json):
        #Response message for the requester
        reponse = {"result": True, "reason": ""}
        try:
            machines = scenario_json['machines']
            scenario_name = scenario_json['scenario_name']
            machine_names = machines.keys()
            machines_path = self.getScenariosPath() / scenario_name / "Machines"
            for machine_name in machine_names:
                machine_path = machines_path / machine_name
                machine = scenario_json["machines"][machine_name]
                if os.path.isdir(machine_path):
                    print("Folder already exists")
                else:
                    os.makedirs(machine_path)
                shared_folder = machine["shared_folders"][0]
                shared_folder_path = machine_path / shared_folder
                if os.path.isdir(shared_folder_path):
                    print("Shared folder already exists")
                else:
                    os.makedirs(shared_folder_path)
            
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