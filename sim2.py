#import _thread as thread
import threading
import time

ExperimentName = "Experiment_3_cs"
gcs = 'Experiment_3_cs/Audi_A8_Sedan_1'
def update_function(matlab_block,var):
    global ExperimentName,gcs
    def __temp__(var_from_py):
        eng.workspace[var] = float(var_from_py)
     #   eng.set_param(eng.gcs() +'/'+ matlab_block,'Value',var)
        eng.set_param(gcs +'/'+ matlab_block,'Value',var)
    globals()['update_'+ var] = __temp__
	

    
#import matlab.engine
#future = matlab.engine.connect_matlab(background=True)
#eng = future.result()
import matlab.engine
#future = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine',background=True)
#eng = future.result()
eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')
#eng = None

update_function('InitialVelocity','speed')


try:
        
#    print( eng.get_param(gcs +'/InitialVelocity','Value') )
#    update_speed(5)
    eng.workspace['speed'] = eng.double(8)
#    eng.set_param(gcs +'/'+ 'InitialVelocity','Value','speed')
#    eng.sim_speed(nargout=0)
    eng.set_param('Experiment_3_cs/Audi_A8_Sedan_1/InitialVelocity','Value','speed',nargout=0)

    print('Next')
except:
    eng.quit()
    
eng.quit()
# -*- coding: utf-8 -*-

