class VirtualMachine(object):
  def __init__(self, name, os):
    self.name = name
    self.os = os
    self.shared_folders = None #tuples of (hostPath, guestPath)
    self.network_settings = None
    self.gui = False
    self.provision = None #will be populated by provision objects

  def setOS(self, os):
    self.os = os

  def setName(self, name):
    self.name = name

  def addSharedFolder(self, hostPath, guestPath):
    self.shared_folders = (hostPath, guestPath)

  def setNetworkSettings(self , network_settings):
    self.network_settings = network_settings
    
  def enableGUI(self, isVisible):
    self.gui = isVisible

  def setProvision(self, provision):
    self.provision = provision
      
  def dictionary(self):
    vm_dict = dict()
    vm_dict["os"] = self.os
    vm_dict["name"] = self.name
    vm_dict["shared_folders"] = self.shared_folders
    vm_dict["network_settings"] = self.network_settings.dictionary() if self.network_settings else dict()
    vm_dict["provisions"] = self.provision.dictionary() if self.provision else dict()
    vm_dict["gui"] = self.gui
    return vm_dict