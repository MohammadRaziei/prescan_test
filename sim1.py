#import _thread as thread
import threading
import time

ExperimentName = "Experiment_3_cs"
gcs = 'Experiment_3_cs/Audi_A8_Sedan_1'
def update_function(matlab_block,var):
    global ExperimentName,gcs
    def temp(var_from_py):
        eng.workspace[var] = float(var_from_py)
     #   eng.set_param(eng.gcs() +'/'+ matlab_block,'Value',var)
        eng.set_param(gcs +'/'+ matlab_block,'Value',var)
    globals()['update_'+ var] = temp
	

    
#import matlab.engine
#future = matlab.engine.connect_matlab(background=True)
#eng = future.result()
import matlab.engine
future = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine',background=True)
eng = future.result()
#eng = None

update_function('InitialVelocity','speed')


try:
        
    eng.sim(ExperimentName,20.0)
        
    print('Next')
except:
    eng.quit()
    
eng.quit()
# -*- coding: utf-8 -*-
a = [1,2,3]

