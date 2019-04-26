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
#eng = None
try:
    class Matlab(threading.Thread):
        def __init__(self,ExperimentName,sim_time):
            global eng
            super(Matlab,self).__init__()
            self.sim_time = sim_time
            self.ExperimentName = ExperimentName
        def sim(self):
            eng.sim(self.ExperimentName,self.sim_time)
    #    threading.Thread(target=)
        def show(self):
            print(self.sim_time)
            print(self.ExperimentName)
        def run(self):
#            time.sleep(5)
            self.sim()
#            self.show()
#            print('Hello')
            pass
        
    for i in range(4):   
        mat = Matlab(ExperimentName,10)
#        mat.show()
        mat.start()
        
    print('Next')
except:
    eng.quit()
    
eng.quit()
