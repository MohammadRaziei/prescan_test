# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:47:01 2019

@author: MohammadRaziei
"""



import socket
import struct, json
import random
from datetime import datetime


import os, numpy as np
port = 9620

def find_and_kill_port(port):
    result = os.popen("netstat -ano | findstr :{} | findstr ESTABLISHED".format(port)).read().strip()
    if result != '' :
        pid = result.split(" ")[-1]
        os.popen("taskkill /PID {} /F".format(pid))


ExperimentName = ''
bdroot = ''
prescanFile = ''
def set_experimant(ExpName):
    global ExperimentName,bdroot,prescanFile
    ExperimentName = ExpName
    bdroot = ExperimentName+"_cs"
    prescanFile = ExperimentName+".pb"


def getDefaultFilename():
    eng.prescan.experiment.getDefaultFilename()


def objectsFindByName(name):
    global ExperimentName
    eng.eval(ExperimentName+"_models = prescan.experiment.readDataModels('"+ExperimentName+".pd');",nargout=0)
    return int(eng.eval("prescan.worldmodel.objectsFindByName("+ExperimentName+"_models.worldmodel, '"+name+"')") )

class sim:
    global bdroot
    def Update():
        eng.set_param(bdroot,'SimulationCommand','update',nargout=0)
    def Pause(): 
        eng.set_param(bdroot,'SimulationCommand','pause',nargout=0)
    def Continue():
        eng.set_param(bdroot,'SimulationCommand','continue',nargout=0)
    def Stop():
        eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
    def Start():
        eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
    def Restart():
        eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
        eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
    def Status():
        '''
        The software returns 'stopped', 'initializing', 'running', 'paused', 'compiled', 'updating', 'terminating', or 'external'.
        '''
        return eng.get_param(bdroot,'SimulationStatus')
    def Time():
        return eng.get_param(bdroot,'SimulationTime')
    


def python2matlab(**args):
    for key,value in args.items():
        eng.workspace[key] = eng.double(value)
        
def matlab2python(*args):
    for arg in args:
        globals()[arg] = eng.workspace[arg]
        
def pysim_update(**args):
    python2matlab(**args)
    sim.Update()

def prescan_regenerate():
    global bdroot,eng
    eng.generate_all(bdroot)
            





class Model():
    global ExperimentName,bdroot
    __shared_flags__ = {'create_model':False,'objects':[]}
    def __init__(self, name, model):
        Model.__shared_flags__['objects'].append(self)
        self.name = name
        self.model = model
    def create(self):
        self.create_model_ones()
        self.id = Model.objectsFindByName(self.name)
        self.object = eng.eval(ExperimentName+"_models.worldmodel.object{" + str( self.id ) + ", 1} ")
        self.position = self.object['pose']['position']
        self.orientation =  self.object['pose']['orientation']

    def create_model():
        eng.eval(ExperimentName+"_models = prescan.experiment.readDataModels('"+ ExperimentName +".pb');",nargout=0)
    
    def create_model_ones(self):
        if ( not Model.__shared_flags__['create_model'] ) and (eng.exist(ExperimentName+'_models') != 1):
            Model.create_model()
            Model.__shared_flags__['create_model'] = True
    
    def objectsFindByName(name):
        return int(eng.eval("prescan.worldmodel.objectsFindByName("+ExperimentName+"_models.worldmodel, '"+name+"')") )
    def Update(**args):
        python2matlab(**args)
        sim.Update()
        
    def __str__(self):
        return self.name
    def __repr__(self):
        return '{}({!r})'.format(self.model,self.name)
    
    
class Road(Model):
    __shared_flags__ = {'objects':[]}
    def __init__(self, name = 'StraightRoad_1'):
        Road.__shared_flags__['objects'].append(self)
        Model.__init__(self,name,'Road')
    def create(self):
        super().create()
        self.length = self.object['road']['straightRoad']['roadLength']
        self.numberOfLanes = len(self.object['road']['roadEnds'][0]['laneEnds'])
        self.laneWidth = self.object['road']['roadEnds'][0]['laneEnds'][0]['width']

class Vehicle(Model):
    __shared_flags__ = {'objects':[]}
    def __init__(self, name, data_port = None,road = None):
        Vehicle.__shared_flags__['objects'].append(self)
        Model.__init__(self,name,'Vehicle')
        self.road = road
        self.port = data_port

    def create(self,data_port = None):
        super().create()
        port = data_port if data_port is not None else self.port
        self.data = Reciver_UDP2(port)
        self.data.build()





    # def get_position_road(self,road = None):
    #     __road__ = road if road is not None else self.road 
    #     car_x, car_y = self.get_position()
    #     pos_x = car_x -  __road__.position['x']
    #     pos_y = car_y -  __road__.position['y']
    #     self.road_pos = pos_x, pos_y
    #     return self.road_pos 
    
    # def is_in_road(self,road = None):
    #     __road__ = road if road is not None else self.road 
    #     pos_x, pos_y = self.get_position_road(__road__)
    #     if abs(pos_y) >= __road__.numberOfLanes * __road__.laneWidth / 2:
    #         return False
    #     if pos_x < 0 or pos_x > __road__.length:
    #         return False
    #     return True
        
    # def examinLane(self,road = None):
    #     __road__ = road if road is not None else self.road        
    #     pos_y = self.get_position_road()[1] / __road__.laneWidth
    #     pos_y_offset = __road__.numberOfLanes / 2 
    #     lane = int(np.floor(pos_y) + pos_y_offset)
    #     return lane


        


class Reciver_UDP:

    def __init__(self, port_number=0, this_socket=None):
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def build(self):
        self.this_socket.bind(("", self.port_number))
        print("waiting on port:", self.port_number)

    def get(self):
        data, addr = self.this_socket.recvfrom(1024)
        x = struct.unpack('d', data)
        #if x[0] >= 0:
        #print(self.name,": ", x[0])
        return x[0]    
        

class Reciver_UDP2:
    def __init__(self, port_number=0, this_socket=None):
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def build(self):
        self.this_socket.bind(("", self.port_number))
        print("waiting on port:", self.port_number)

    def get(self):
        data, addr = self.this_socket.recvfrom(1024)
        data = json.loads(data.decode("utf-8"))
        return  data
    def get_str(self):
        data, addr = self.this_socket.recvfrom(1024)
        return  data.decode("utf-8")


class Transmitter_UDP:
    
    def __init__(self, port_number=0, host ='localhost', this_socket=None):
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        print("Sending data to port: ")
    
    def send(self, ac):
        y = struct.pack("d",ac)
        self.this_socket.sendto(y, (self.host, self.port_number))
        print("The Action is: ", ac)


       
class Q_network:
    
    def __init__(self, name):
        self.name = name
        
    def feed(self, state):
        best_action = []
        
        # Neural network out put is the Q-values for all available actions.
        # All available actions are 9 actions; Each of them is a vector of 3 values : [off_set, speed_up, speed_down]
        # We need to select the action with max Q-value
        #Assume this action is a4 = [3.5, True, False]
        #ran = 1
        ran = random.randint(-2, 3)
        laneWidth = car.road.laneWidth
        best_action = [(laneWidth*ran), True, False]
        print(best_action)
        return best_action
    

def action_vec_to_commands(action, state):
    
    off_set = action[0]
    
    if (action[1]==False) and (action[2]==False) :
        desired_velocity = state[1] #speed is not changed
        throttle_flag = 0
        brake_flag = 0        
        
    elif (action[1]==True) and (action[2]==False) :
        #desired_velocity = state[1] + 5
        desired_velocity = 20
        throttle_flag = 1
        brake_flag = 0
        
    elif (action[1]==False) and (action[2]==True) :
        desired_velocity = state[1] - 5
        throttle_flag = 0
        brake_flag = 1        
        
    else:
        print("ERROR!")
    
    off_set_UDP.send(off_set)
    desired_velocity_UDP.send(desired_velocity)
    throttle_flag_UDP.send(throttle_flag)
    brake_flag_UDP.send(brake_flag)
    

    

def get_state():
    state = []                
    for i in Vehicle.__shared_flags__['objects']:
            data = i.data.get()
            x = data["Position"]["x"]
            v = data["Velocity"]["x"]
            state.append(x)
            state.append(v)            
            print("Time: ",data["Time"])
            print(i.name, "position: ", x)
            print(i.name, "speed: ", v, end="\n\n")
    return state

'''
def reset_environment():
    
    car_pose_reset.send(1)
    car_speed_reset.send(1)
    other1_pose_reset.send(1)
    other1_speed_reset.send(1)
''' 

import matlab.engine
eng = matlab.engine.connect_matlab()   
set_experimant('cameraCar')
if __name__ == '__main__':  
    main_Q_Network = Q_network("mainQN") 
    #Creating traffic
    road = Road('StraightRoad_1')
    road.create()
    car = Vehicle('Toyota_Yaris_Hatchback_1', 8091,road)
    car.create()


    Reward = Reciver_UDP(8081)
    Reward.build() 
    


    #Creating UDP_ports to send the command of actions:    
    off_set_UDP = Transmitter_UDP(8072)
    desired_velocity_UDP = Transmitter_UDP(8073)
    throttle_flag_UDP = Transmitter_UDP(8074)
    brake_flag_UDP = Transmitter_UDP(8075)

    '''
    #Creating UDP_ports to send the command of reset the environment:
    car_pose_reset = Transmitter_UDP("car_pose_reset", 8000)
    car_speed_reset = Transmitter_UDP("car_speed_reset", 8001)
    other1_pose_reset = Transmitter_UDP("other1_pose_reset", 8002)
    other1_speed_reset = Transmitter_UDP("other1_speed_reset", 8003)
    '''
    a = [0, False, False]
    print("initial action: ", a)
    Replay_memory = []
    i=0
    timeVector=[]

    while 1:

        experience = np.array([])

        print("________________________________")
        print("Iteration #", i)
        i = i+1

        #state
        state = get_state() 
        #experience.append(state)
        
        experience = np.append(experience, state)

        #action
        action_vec = main_Q_Network.feed(state)          
        #experience.append(action_vec)
        experience = np.append(experience, action_vec)

        #sendig commands to PreScan
        action_vec_to_commands(action_vec, state)
        
        #reward
        r = Reward.get()
       # experience.append(r)
        experience = np.append(experience, r)

        #next state
        next_state = get_state()
        #experience.append(next_state)
        experience = np.append(experience, next_state)

        print("Experience: ",experience)
        #print("Experience_shape:", experience.shape())
        Replay_memory.append(experience)
        
        time=datetime.now().time()
        print("Time:", time)
        timeVector.append(time)

        print(repr(car.data.get_str()))

        
        
        
        
        
        
        
        
        
        
    
