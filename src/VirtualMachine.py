class VirtualMachine(object):
    def __init__(self, Name, OS):
        self.os = OS
        self.name = Name
        self.shared_folders = [] #tuples of (hostPath, guestPath)
        self.ipAddress = None
        self.provision = None #will be populated by provision objects

    def setOS(self, os):
        self.os = os

    def setName(self, name):
        self.name = name

    def addSharedFolder(self, hostPath, guestPath):
        self.shared_folders.append((hostPath, guestPath))

    def setIPAddress(self, address):
        self.ipAddress = address

    def setProvision(self, provision):
        self.provision = provision
        
    def virtualMachine2Dictionary(self):
        vm_dict = dict()
        vm_dict["os"] = self.os
        vm_dict["name"] = self.name
        vm_dict["shared_folders"] = self.shared_folders
        vm_dict["ipAddress"] = self.ipAddress
        #vm_dict["provision"] = self.provision
        return vm_dict