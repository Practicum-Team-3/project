from VagrantFile import VagrantFile

if __name__=="__main__":
  

  vfile = VagrantFile()
  test = vfile.vagrantFileFromJSON('scenario_1.json')  
  test_2 = vfile.vagrantFileFromJSON('scenario_2.json')  
  test_3 = vfile.vagrantFileFromJSON('scenario_3.json')
  
  
  