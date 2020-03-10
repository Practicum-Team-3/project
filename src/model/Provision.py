class Provision(object):
    def __init__(self, name, provision_type = "shell"):
        """

        :param name: The name
        :param provision_type:
        """
        self.name = name
        self.provision_type = provision_type
        self.commands = list()
    
    def setShellCommand(self, command ):
        """

        :param command:
        """
        self.commands.append(command)
        
    def dictionary(self):
        """

        :return:
        """
        prov_dict = dict()
        prov_dict["name"] = self.name
        prov_dict["provision_type"] = self.provision_type
        prov_dict["commands"] = self.commands
        return prov_dict