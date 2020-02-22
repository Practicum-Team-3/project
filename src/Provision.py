class Provision(object):
    def __init__(self, name):
        self.name = name
        self.command = None
        self.type = None
    
    def setShellCommand(self, commandString):
        self.type = "shell"
        self.command = commandString