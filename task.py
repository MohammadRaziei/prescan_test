import numpy as np
import re
from time import sleep

ExperimentName = "Experiment_3"
bdroot = ExperimentName+"_cs"
gcs = 'Experiment_3_cs/Audi_A8_Sedan_1'



import json
def save_json(data):
    with open(data + '.json', 'w') as f:
        json.dump(globals()[data], f, ensure_ascii=False)
        

def nargout(func):
    return int( eng.eval('nargout(@'+func+')') )


def getDefaultFilename():
    eng.prescan.experiment.getDefaultFilename


def objectsFindByName(name):
    eng.eval("models = prescan.experiment.readDataModels('Experiment_3.pb');",nargout=0)
    return int(eng.eval("prescan.worldmodel.objectsFindByName(models.worldmodel, '"+name+"')") )

    
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
           




class Model():
    global ExperimentName,bdroot
    
    def __init__(self, name):
        eng.eval("models = prescan.experiment.readDataModels('"+ExperimentName+".pb');",nargout=0)
        self.name = name
        self.id = objectsFindByName(self, name)
        self.object = eng.eval("models.worldmodel.object{" + str( self.id ) + ", 1} ")
        self.position = self.object['pose']['position']
        self.orientation =  self.object['pose']['orientation']
        self.dict = {'name':self.name,'id':self.id, 
                     'position':self.position,'orientation':self.orientation, 
                     'length':self.length, 'numberOfLanes':self.numberOfLanes, 
                     'laneWidth':self.laneWidth}
        self.__str__ = self.name
        self.__repr__ = self.name
    def objectsFindByName(self,name):
        return int(eng.eval("prescan.worldmodel.objectsFindByName(models.worldmodel, '"+name+"')") )

class Road(Model):
    def __init__(self, name):
        Model.__init__(self)
        self.length = self.object['road']['straightRoad']['roadLength']
        self.numberOfLanes = len(self.object['road']['roadEnds'][0]['laneEnds'])
        self.laneWidth = self.object['road']['roadEnds'][0]['laneEnds']['width']
        self.dict = {'length':self.length, 'numberOfLanes':self.numberOfLanes, 'laneWidth':self.laneWidth}
        self.dict = {**Model.dict,**self.dict}
class Car(Model):
    def __init__(self, name,road = None):
        Model.__init__(self,name)
        self.road = road
        self.dict = {'road_name':road.name}
        self.dict = {**Model.dict,**self.dict}       
    def position(self,runtime = True):
        if runtime == True:
            if eng.exist('Positions') and ( sim_status() in ['paused','stopped'] ):
                x = eng.eval('Positions.Data(1,end)')
                y = eng.eval('Positions.Data(2,end)')
            else: 
                try:
                    block = self.bdroot+'/'+ self.name +'/To Workspace';
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
    def position_road(self,road = None):
        __road__ = road if road is not None else self.road 
        car_x, car_y = self.position()
        pos_x = car_x -  __road__.position['x']
        pos_y = car_y -  __road__.position['y']
        self.road_pos = pos_x, pos_y
        return self.road_pos 
    
    def is_in_road(self,road = None):
        __road__ = road if road is not None else self.road 
        pos_x, pos_y = self.position_road(__road__)
        if abs(pos_y) >= __road__.numberOfLanes * __road__.laneWidth / 2:
            return False
        if pos_x < 0 or pos_x > __road__.length:
            return False
        return True
        
    def examinLane(self,road = None):
        __road__ = road if road is not None else self.road        
        pos_y = self.position_road()[1] 
        pos_y_offset = 1 if pos_y > 0 else 0
        lane = np.floor(pos_y/__road__.laneWidth) + pos_y_offset
        return lane

        








def run_senario():
    global bdroot
    road = Road()
    car = Car('Audi_A8_Sedan_1',road)
    print(car,road)
    
    sim_start()
    for i in range(2):
        while True:
            sleep(2)
            time = sim_time()
            print("time : {}".format(time) )
            x, y = car.position_road()
            lane = car.examinLane()
            if lane == road.numberOfLanes / 2:
                RL = np.random.randint(-1,1)
            elif lane == -road.numberOfLanes / 2:
                RL = np.random.randint(0,2)
            else :
                RL = np.random.randint(-1,2)            
            print('lane = {} -> RL = {}'.format(lane,RL))
            pysim_update('RL')
            if not car.is_in_road():
                sim_restart()
            
            print('\tx = {}\n\ty = {}'.format(x,y))
        sim_stop()  
        
####################################################
import matlab.engine
try:
    eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')
except:
    pass

try:

    
    run_senario()
    

    print('The End')
except:
    eng.quit()
eng.quit()

