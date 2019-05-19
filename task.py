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
    eng.eval("models = prescan.experiment.readDataModels('"+ExperimentName+".pb');",nargout=0)
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
    


def python2matlab(**args):
    for key,value in args.items():
        eng.workspace[key] = eng.double(value)
        
def matlab2python(*args):
    for arg in args:
        globals()[arg] = eng.workspace[arg]
        
def pysim_update(**args):
    python2matlab(**args)
    sim_update()

def prescan_regenerate():
    global bdroot,eng
    eng.generate_all(bdroot)
           




class Model():
    global ExperimentName,bdroot
#    __ExperimentName__  = ExperimentName
#    __bdroot__ = bdroot
    __shared_flags__ = {'create_model':False}
    def __init__(self, name, model):
        self.create_model_ones()
        self.name = name
        self.model = model
        self.id = Model.objectsFindByName(name)
        self.object = eng.eval("models.worldmodel.object{" + str( self.id ) + ", 1} ")
        self.position = self.object['pose']['position']
        self.orientation =  self.object['pose']['orientation']
#        self.items = {'name':self.name,'id':self.id, 
#                     'position':self.position,'orientation':self.orientation}

    def create_model():
        eng.eval("models = prescan.experiment.readDataModels('"+ ExperimentName +".pb');",nargout=0)
   
    def create_model_ones(self):
        if ( not Model.__shared_flags__['create_model'] ) and (eng.exist('models') != 1):
            Model.create_model()
            Model.__shared_flags__['create_model'] = True
    
    def objectsFindByName(name):
        return int(eng.eval("prescan.worldmodel.objectsFindByName(models.worldmodel, '"+name+"')") )
   
    def __str__(self):
        return self.name
    def __repr__(self):
        return '{}({!r})'.format(self.model,self.name)
    
    
class Road(Model):
    def __init__(self, name = 'StraightRoad_1'):
        Model.__init__(self,name,'Road')
        self.length = self.object['road']['straightRoad']['roadLength']
        self.numberOfLanes = len(self.object['road']['roadEnds'][0]['laneEnds'])
        self.laneWidth = self.object['road']['roadEnds'][0]['laneEnds'][0]['width']
#        items = {'length':self.length, 'numberOfLanes':self.numberOfLanes, 'laneWidth':self.laneWidth}
#        self.items = {**self.items,**items}
class Car(Model):
    def __init__(self, name,road = None):
        Model.__init__(self,name,'Car')
        self.road = road
#        items = {'road_name':road.name}
#        self.items = {**self.items,**items}       
    def get_position(self,runtime = True):
        if runtime == True:
#            if eng.exist('Positions') and ( sim_status() in ['paused','stopped'] ):
#                x = eng.eval('Positions.Data(1,end)')
#                y = eng.eval('Positions.Data(2,end)')
            if sim_status() == 'stopped':
                x = self.position['x']
                y = self.position['y']          
            else: 
                try:
                    block = bdroot+'/'+ self.name +'/To Workspace';
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
    def get_position_road(self,road = None):
        __road__ = road if road is not None else self.road 
        car_x, car_y = self.get_position()
        pos_x = car_x -  __road__.position['x']
        pos_y = car_y -  __road__.position['y']
        self.road_pos = pos_x, pos_y
        return self.road_pos 
    
    def is_in_road(self,road = None):
        __road__ = road if road is not None else self.road 
        pos_x, pos_y = self.get_position_road(__road__)
        if abs(pos_y) >= __road__.numberOfLanes * __road__.laneWidth / 2:
            return False
        if pos_x < 0 or pos_x > __road__.length:
            return False
        return True
        
    def examinLane(self,road = None):
        __road__ = road if road is not None else self.road        
        pos_y = self.get_position_road()[1] 
#        pos_y_offset = 1 if pos_y > 0 else 0
        pos_y_offset = __road__.laneWidth / 2 - 1
        lane = int(np.floor(pos_y/__road__.laneWidth) + pos_y_offset)
        return lane

        






#----------------------------------------------------------

def run_senario():
    global bdroot
    road = Road('StraightRoad_1')
    car = Car('Audi_A8_Sedan_1',road)
    print('{!r}\t{!r}'.format(car,road))
    
    sim_restart()
    print('>> Start')
    
    lane_start = car.examinLane() 
    print('lane_start : {}'.format(lane_start))
    for i in range(2):
        RL = 0
        while True:
            sleep(2)
            time = sim_time()
            print("time : {}".format(time) )
            x, y = car.get_position_road()
            lane = car.examinLane()
            RL /= road.laneWidth
            if lane == road.numberOfLanes - 1:
                RL += np.random.randint(-1,1)
            elif lane == 0:
                RL += np.random.randint(0,2)
            else :
                RL += np.random.randint(-1,2) 
            RL -= lane_start
            print('lane = {} -> RL = {}'.format(lane,RL))
            print('\tx = {}\n\ty = {}'.format(x,y))
            RL = RL * road.laneWidth
            pysim_update(RL=RL)
            if not car.is_in_road():
                sim_restart()
                print('>> Restart')
                continue
        
        sim_stop()  
        print('>> Stop')
###########################################################
import matlab.engine
try:
    eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')
except:
    try:
        eng = matlab.engine.connect_matlab()
    except:
        pass

try:

    
    run_senario()
    

    print('The End')
except:
#    eng.quit()
    pass
#eng.quit()

