import subprocess
import re
from src.model.FileManager import FileManager

class VagrantManager(object):

    def __init__(self):
        self.file_manager = FileManager()

    def createVagrantFiles(self, scenario_json):
        pass

    def getAvailableBoxes(self):
        # Variables
        boxes = {}
        boxNum = 0
        boxlist = subprocess.check_output("vagrant box list", shell=True)
        boxlist = str(boxlist)
        boxlist = re.sub(r"(^[b']|'|\s(.*?)\\n)", " ", boxlist)
        boxlist = boxlist.split(" ")
        boxlist = filter(None, boxlist)

        print("Loading available Vanilla VMs")

        for boxName in boxlist:
            boxNum = boxNum + 1
            boxes[boxNum] = boxName
            print("[ " + str(boxNum) + " ]" + boxName)
        return boxes