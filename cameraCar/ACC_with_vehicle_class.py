import socket
import struct
import random
import numpy as np
from datetime import datetime


#import torch
#print (torch.cuda.is_available())


class vehicle:
    
    def __init__(self, name=" ", pose_port = 0, speed_port = 0, UDP_pose=None, UDP_speed=None):
        self.name = name
        self.pose_port = pose_port
        self.speed_port = speed_port
        
    def create(self):
        self.UDP_pose = Reciver_UDP("UDP_pose", self.pose_port)
        self.UDP_pose.build()
        self.UDP_speed = Reciver_UDP("UDP_speed", self.speed_port)
        self.UDP_speed.build()

class Reciver_UDP:

    def __init__(self, name, port_number=0, this_socket=None):
        self.name = name
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def build(self):
        self.this_socket.bind(("", self.port_number))
        print("waiting on port:", self.port_number)

    def get_data(self):
        data, addr = self.this_socket.recvfrom(1024)
        x = struct.unpack('d', data)
        #if x[0] >= 0:
        #print(self.name,": ", x[0])
        return x[0]    


class Transmitter_UDP:
    
    def __init__(self, name, port_number=0, host ='localhost', this_socket=None):
        self.name = name
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        print("Sending data to port: ")
    
    def send_data(self, ac):
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
        best_action = [(3.5*ran), True, False]
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
    
    off_set_UDP.send_data(off_set)
    desired_velocity_UDP.send_data(desired_velocity)
    throttle_flag_UDP.send_data(throttle_flag)
    brake_flag_UDP.send_data(brake_flag)
    
    

def get_state():
    state = []                
    for i in traffic:
            x = i.UDP_pose.get_data()
            v = i.UDP_speed.get_data()
            state.append(x)
            state.append(v)            
            print(i.name, "position: ", x)
            print(i.name, "speed: ", v, end="\n\n")
    return state


def reset_environment():
    
    host_pose_reset.send_data(1)
    host_speed_reset.send_data(1)
    other1_pose_reset.send_data(1)
    other1_speed_reset.send_data(1)
    
    

if __name__ == '__main__':  
    
    main_Q_Network = Q_network("mainQN") 
    
    #Creating traffic
    traffic = []
    host = vehicle("host", 8084, 8085)
    host.create()
    traffic.append(host)    
    
    #other1 = vehicle("other1", 8086, 8087)
    #other1.create()
    #traffic.append(other1)
    
    #other2 = vehicle("other2", 8088, 8089)
    #other2.create()
    #traffic.append(other2)
    
    #other3 = vehicle("other3", 8090, 8091)
    #other3.create()
    #traffic.append(other3)

    Reward = Reciver_UDP("Reward", 8081)
    Reward.build()

    SimTime = Reciver_UDP("SimTime", 8020)
    SimTime.build()
    
    #Creating UDP_ports to send the command of actions:    
    off_set_UDP = Transmitter_UDP("off_set", 8072)
    desired_velocity_UDP = Transmitter_UDP("desired_velocity", 8073)
    throttle_flag_UDP = Transmitter_UDP("throttle_flag", 8074)
    brake_flag_UDP = Transmitter_UDP("brake_flag", 8075)

    '''
    #Creating UDP_ports to send the command of reset the environment:
    host_pose_reset = Transmitter_UDP("host_pose_reset", 8000)
    host_speed_reset = Transmitter_UDP("host_speed_reset", 8001)
    other1_pose_reset = Transmitter_UDP("other1_pose_reset", 8002)
    other1_speed_reset = Transmitter_UDP("other1_speed_reset", 8003)
    '''
    a = [0, False, False]
    print("initial action: ", a)
    Replay_memory = []
    i=0
    timeVector=[]

    while 1:

        #experience = []
        experience = np.array([])

        print("________________________________")
        print("Iteration #", i)
        i = i+1

        # SimTime
        t = SimTime.get_data()
        print("Simulation time:", t)

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
        r = Reward.get_data()
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


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
