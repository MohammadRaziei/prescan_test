import os
prescan_dir = r"C:\Users\Public\Documents\Experiments\mohammad"
Experiment_name = "Experiment_1"
Experiment_cs = os.path.join(prescan_dir,Experiment_name,Experiment_name+"_cs")
print(Experiment_cs);


#prescan = 'C:\Program Files\PreScan\PreScan_8.4.0\bin\prescanrun.bat'

#import subprocess
#subprocess.run([prescan, ""])
#
#import os
#os.system(prescan+" --setup-only")  


import matlab.engine
eng = matlab.engine.start_matlab()
############################
Simulation_Time = 10 #seconds
#eng.sim(Experiment_cs,Simulation_Time)
eng.matlab_aa(nargout=0)
############################
eng.quit()
# -*- coding: utf-8 -*-



