#import _thread as thread
import threading
import re
from time import sleep

ExperimentName = "Experiment_3_cs"
bdroot = "Experiment_3_cs"
gcs = 'Experiment_3_cs/Audi_A8_Sedan_1'



def update_function(matlab_block,var_str=None):
    if type(matlab_block) is type([]):
        var_str = matlab_block[1]
        matlab_block = matlab_block[0]
    def __temp__(var_from_py):
        global ExperimentName,gcs
        if type(var_from_py) is type([]):
            var_from_py = var_from_py[0]
#        print([matlab_block,var,var_from_py])
        eng.workspace[var_str] = eng.double(var_from_py)
     ##   eng.set_param(eng.gcs() +'/'+ matlab_block,'Value',var)
        eng.set_param(gcs +'/'+ matlab_block,'Value',var_str,nargout=0)
    globals()['update_'+ var_str] = __temp__
	

import json
def save_json(data):
    with open(data + '.json', 'w') as f:
        json.dump(globals()[data], f, ensure_ascii=False)
        
#eng.prescan.experiment

def nargout(func):
    return int( eng.eval('nargout(@'+func+')') )


def getDefaultFilename():
    eng.prescan.experiment.getDefaultFilename
#
#def getFieldValue():
#    eng.prescan.experiment
#
#
#def readDataModels():
#    eng.prescan.experiment.readDataModels()
#
#def replaceWorldObjectByName():
#    eng.prescan.experiment.replaceWorldObjectByName()
#
#def run():
#    print('run')
#
#def runWithDataModels():
#    eng.prescan.experiment.runWithDataModels()
#
#def setFieldValue():
#    eng.prescan.experiment.setFieldValue()
#
#validate
#
#def worldObjectsDeleteByName():
#    eng.prescan.experiment.worldObjectsDeleteByName()
#
#def worldObjectsDeleteByTypeId():
#    eng.prescan.experiment.worldObjectsDeleteByTypeId()
#

#road_obj = models.worldmodel.object{prescan.worldmodel.objectsFindByName(models.worldmodel, 'StraightRoad_1') , 1}.road;
def objectsFindByName(name):
    eng.eval("models = prescan.experiment.readDataModels('Experiment_3.pb');",nargout=0)
    return int(eng.eval("prescan.worldmodel.objectsFindByName(models.worldmodel, '"+name+"')") )
 
def road_obj(name='StraightRoad_1'):
    return eng.eval("models.worldmodel.object{" + str(objectsFindByName(name) ) + ", 1}.road; ")
def road_position(name='StraightRoad_1'):
    return road_obj(name)['roadEnds'][0]['pose']['position']
def road_length(name='StraightRoad_1'):
    return road_obj(name)['straightRoad']['roadLength']
def numberOfLanes(name='StraightRoad_1'):
    return len (road_obj(name)['roadEnds'][0]['laneEnds'])


class Model():
    def __init__(self):
        eng.eval("models = prescan.experiment.readDataModels('Experiment_3.pb');",nargout=0)

class Road(Model):
    def __init__(self, name):
        Model.__init__(self)
        self.name = name
        self.id = objectsFindByName(self, name)
        self.object = eng.eval("models.worldmodel.object{" + str( self.id ) + ", 1}.road; ")
        self.position = self.object['roadEnds'][0]['pose']['position']
        self.orientation =  self.object['roadEnds'][0]['pose']['orientation']
        self.length = self.object['straightRoad']['roadLength']
        self.numberOfLanes = len(self.object['roadEnds'][0]['laneEnds'])
        self.laneWidth = self.object['roadEnds'][0]['laneEnds']['width']
        self.dict = {'name':self.name,'id':self.id, 
                     'position':self.position,'orientation':self.orientation, 
                     'length':self.length, 'numberOfLanes':self.numberOfLanes, 
                     'laneWidth':self.laneWidth}
 
class car(Model):
    def __init__(self, name,road):
        Model.__init__(self)
        self.name = name
        self.id = objectsFindByName(self, name)
        self.road = road
        
    def position(self,runtime = True):
        if runtime == True:
            if eng.exist('Positions') and ( sim_status() in ['paused','stopped'] ):
                x = eng.eval('Positions.Data(1,end)')
                y = eng.eval('Positions.Data(2,end)')
            else: 
                try:
                    block = 'Experiment_3_cs/Audi_A8_Sedan_1/To Workspace';
                    eng.eval("rto_positions = get_param('"+block+"','RuntimeObject');",nargout=0)
                    [[x],[y]] = eng.eval("rto_positions.InputPort(1).Data")
                except:
                    x = eng.eval('Positions.Data(1,end)')
                    y = eng.eval('Positions.Data(2,end)')
            return x,y
        else:
            if eng.exist('Positions') and ( sim_status() in ['paused','stopped'] ):
                data = eng.eval('Positions.Data')
                return data
    def examinLane(self,road = None):
        __road__ = road if road is not None else self.road        
       
#    
#    
    
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
    global bdroot,engs
    eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
def sim_restart():
    global bdroot,eng
    eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
    eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
def sim_status():
    global bdroot,eng
    return eng.get_param(bdroot,'SimulationStatus')
    #The software returns 'stopped', 'initializing', 'running', 'paused', 'compiled', 'updating', 'terminating', or 'external' (used with the Simulink Coder™ product).
def sim_time():
    global bdroot
    return eng.get_param(bdroot,'SimulationTime')
    


def python2matlab(*args):
    for arg in args:
        eng.workspace[arg] = matlab.double(globals()[arg])
        
def matlab2python(*args):
    for arg in args:
        globals()[arg] = eng.workspace[arg]
        
def pysim_update(*args):
    python2matlab(*args)
    sim_update()

def prescan_regenerate():
    global bdroot,eng
    eng.generate_all(bdroot)
           
def prescan_linechange(module,var):
    global bdroot,eng
#    eng.set_param(bdroot,)
    globals()['prescan_linechange_RL'] = var;
    pysim_update('prescan_linechange_RL')








def var(name,value=None):
    global eng
    if type(name) is type([]):
        value = name[1]
        name = name[0]
    eng.workspace[name] = eng.double(value)

'''
def Prescan_terminal(User_states=[]):
    __default_states__ = ['quit','exit','start','stop','restart','pause','resume','play','update','status']
    __supported_states__ = __default_states__ + User_states
    pattern = re.compile(r"[;,= ]+")
    while True:
        __complex__ = False
        __terminal_args__ = None
        __terminal_state__ = input('>> ').strip().casefold()
        if not(__terminal_state__ in __supported_states__):
            __terminal_args__ = pattern.split(__terminal_state__)
            __terminal_args__ = [float(i) if (i.replace('.','',1).isdigit()) else i for i in __terminal_args__ ] 
            __terminal_state__ = __terminal_args__.pop(0)

            if not(__terminal_state__ in __supported_states__):
                print('{} is not suported command, try again'.format(__terminal_state__))
                continue
            else :
                __complex__ = True
        try:
            if __terminal_state__ in ['quit','exit']:
                print('Terminal quit successfully')
                break
            if __terminal_state__ == 'start':
                print('Simulation started')
                sim_start()
                continue
            if __terminal_state__ == 'stop':
                print('Simulation stopped')
                sim_stop()
                continue
            if __terminal_state__ == 'restart':
                print('Simulation restarted')
                sim_restart()
                continue
            if __terminal_state__ == 'pause':
                print('Simulation paused')
                sim_pause()
                continue
            if __terminal_state__ in ['resume','play']:
                print('Simulation is running')
                sim_continue()
                continue
            if __terminal_state__ == 'update':
                print('Simulation updated')
                sim_update()
                continue
            if __terminal_state__ == 'status':
                print('Simulation status is {}'.format(sim_status()))
                continue
            ####### for user states : 
#            print('Good')
            if __complex__ :
                globals()[__terminal_state__](__terminal_args__)
                continue
                
            print('Please enter arg or args for {}'.format(__terminal_state__))
            user_args = input('{} args >> '.format(__terminal_state__)).strip()
            pattern.split(user_args) 
            user_args = pattern.split(user_args)
            user_args = [float(i) if (i.replace('.','',1).isdigit()) else i for i in user_args ]
            globals()[__terminal_state__](user_args)
            continue 
        except:
            print('An error occurred while running {}'.format(__terminal_state__))
            continue
'''
'''   
class Position:
    global eng
    def __init__(self):
        self.block = 'Experiment_3_cs/Audi_A8_Sedan_1/To Workspace';
        eng.eval("rto = get_param("+self.block+",'RuntimeObject');",nargout=0)

    def get(self):
        
        try:
            [[self.x],[self.y]] = eng.eval("rto.InputPort(1).Data")
        except:
            self.x = eng.eval('Positions.Data(1,end)')
            self.y = eng.eval('Positions.Data(2,end)')
    
        return self.x,self.y
'''
class Test:
    def __init__(self):
        print('hi')
    def run(self):
        print('run')
        print(eng.sqrt(4.0))

def get_position(): 
    
    if eng.exist('Positions') and ( sim_status() in ['paused','stopped'] ):
        x = eng.eval('Positions.Data(1,end)')
        y = eng.eval('Positions.Data(2,end)')
    else: 
        try:
            block = 'Experiment_3_cs/Audi_A8_Sedan_1/To Workspace';
            eng.eval("rto_positions = get_param('"+block+"','RuntimeObject');",nargout=0)
            [[x],[y]] = eng.eval("rto_positions.InputPort(1).Data")
        except:
            x = eng.eval('Positions.Data(1,end)')
            y = eng.eval('Positions.Data(2,end)')
    return x,y

def run_senario():
    global bdroot
#    pos = Position()
    sim_start()
    for at in range(10):
        sleep(2)
        time = sim_time()
        print("time : {}".format(time) )
#        x,y = pos.get()
        x, y = get_position()
        print('\tx = {}\n\ty = {}'.format(x,y))
    sim_stop()  
        
#import matlab.engine
#future = matlab.engine.connect_matlab(background=True)
#eng = future.result()
import matlab.engine
#future = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine',background=True)
#eng = future.result()
try:
    eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')
except:
    pass
#eng = matlab.engine.connect_matlab()

try:

    
#    run_senario()
    

    print('The End')
except:
#    eng.quit()
    pass

#eng.quit()

