class Provision(object):
    def __init__(self, name):
        self.name = name
        self.commands = list()
    
    def setShellCommand(self, command , provision_type = "shell"):
        self.commands.append((provision_type, command))
        
    def dictionary(self):
        prov_dict = dict()
        prov_dict["name"] = self.name
        prov_dict["commands"] = self.commands
        return prov_dict