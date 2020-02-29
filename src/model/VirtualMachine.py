from src.model.NetworkSettings import NetworkSettings
from src.model.Provision import Provision


class VirtualMachine(object):
  def __init__(self, name, os):
    self.name = name
    self.os = os
    self.shared_folders = tuple() #tuples of (hostPath, guestPath)
    self.network_settings = NetworkSettings("" , "" , "" , True)
    self.gui = False
    self.provision = Provision("pingVictim")

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