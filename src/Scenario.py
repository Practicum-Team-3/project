import json

class Scenario(object):
    def __init__(self, version=2):
        self.machines = dict()
        self.gui = False

    def addVM(self, VM):
        self.machines[VM.name] = VM

    def enableGUI(self, isVisible):
        self.gui = isVisible

    def _scenario2Dictionary(self):
        vf_dict = dict()
        vf_dict["machines"] = list()
        for name in self.machines:
          vf_dict["machines"].append(self.machines[name].virtualMachine2Dictionary())
        vf_dict["gui"] = self.gui
        return vf_dict
    
    def scenario2JSON(self , json_name):
        json_dict = self._scenario2Dictionary()
        with open(json_name, 'w') as outfile:
          json.dump(json_dict, outfile)
        json_string = json.dumps(json_dict , indent = 2)
        print(json_string)
        return json_string
  