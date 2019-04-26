#import _thread as thread
import threading
import time

ExperimentName = "Experiment_3_cs"
bdroot = "Experiment_3_cs"
gcs = 'Experiment_3_cs/Audi_A8_Sedan_1'
def update_function(matlab_block,var):
    global ExperimentName,gcs
    def __temp__(var_from_py):
        eng.workspace[var] = float(var_from_py)
     #   eng.set_param(eng.gcs() +'/'+ matlab_block,'Value',var)
        eng.set_param(gcs +'/'+ matlab_block,'Value',var,nargout=0)
    globals()['update_'+ var] = __temp__
	

    
def sim_update():
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','update',nargout=0)
def sim_pause(): 
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','pause',nargout=0)
def sim_continue():
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','continue',nargout=0)
def sim_stop():
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
def sim_start():
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
def sim_restart():
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
    eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
def sim_status():
    global bdroot,eng
    eng.get_param(bdroot,'SimulationStatus',nargout=0)
    #The software returns 'stopped', 'initializing', 'running', 'paused', 'compiled', 'updating', 'terminating', or 'external' (used with the Simulink Coder™ product).



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

