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
eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')



class Matlab(threading):
    sim_time = 10

    def __init__(self):
        self.eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')
#        super(Matlab,self).__init__()
        self.sim_time = simtime
    def sim(self):
        self.eng.sim()
#    threading.Thread(target=)
    print(s)
    def run(self):
        pass
    
update_function('InitialVelocity','speed')

try:
    
    #eng.matlab_aa(nargout=0);
    #print(eng.sqrt(4.0))

    print(eng.path())
    
    print('XXXXXXXXXXXXXXXXXXXXXXX')
#    print(eng.matlab_aa(nargout=0))
    speed = 1   
    eng.workspace['speed'] = float(speed)
#    eng.eval('speed = 80;')
#    print(eng.eval('(speed)'))
#    eng.sim("Experiment_3_cs",10.0)
    print('simulation')
    eng.sim("Experiment_3_cs",15.0) 
#    eng.workspace['speed'] = float(speed)
#    eng.set_param('Experiment_3_cs/Audi_A8_Sedan_1/InitialVelocity','Value','speed')
    update_speed(speed)

#    time.sleep(5)
    print('5 seconds')
#    thread.start_new_thread(print( eng.sqrt(4.0))
#    x = 4.0
#    eng.workspace['y'] = x
#    print(eng.eval('sqrt(y)'))

except:
    eng.quit()
eng.quit()