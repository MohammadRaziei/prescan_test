import socket,json
import random
import numpy as np
from datetime import datetime





class vehicle:
    def __init__(self, name=" ", port = 0, UDP=None):
        self.name = name
        self.port = port
        
    def create(self):
        self.data = Reciver_UDP(self.port)
        self.data.build()


class Reciver_UDP:
    def __init__(self, name, port=0, this_socket=None):
        self.port = port
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def build(self):
        self.this_socket.bind(("", self.port))
        print("waiting on port:", self.port)

    def get(self):
        data, addr = self.this_socket.recvfrom(1024)
        if len(data) is not None:
            resp = json.loads(data.decode())
            return resp   
        else:
            return None





if __name__ == '__main__':  
        
    host = vehicle("host", 8084)
    host.create()

    Reward = Reciver_UDP(8081)
    Reward.build()

    
    # ## Creating UDP_ports to send the command of actions:    
    # off_set_UDP = Transmitter_UDP("off_set", 8072)
    # desired_velocity_UDP = Transmitter_UDP("desired_velocity", 8073)
    # throttle_flag_UDP = Transmitter_UDP("throttle_flag", 8074)
    # brake_flag_UDP = Transmitter_UDP("brake_flag", 8075)


    i=0
    while 1:


        print("________________________________")
        print("Iteration #", i)
        i = i+1

        t1 = host.data.get()['Time']
        t2 = Reward.get()['Time']
        print("Simulation time:", t1,t2,t2-t1,t2==t1)
        print('>>',host.data.get())

        
        #reward
        r = Reward.get()
        print('>>',r)


        time=datetime.now().time()
        print("Time:", time)


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
