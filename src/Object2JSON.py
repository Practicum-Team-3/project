import json

class Object2JSON():      
    
  def VirtualMachine2JSON(VM):
    vm_dict = VM.virtualMachine2Dictionary()
    vm_JSON = json.dumps(vm_dict)
    print(vm_JSON)
    return vm_JSON
    