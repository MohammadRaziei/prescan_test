# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:47:01 2019

@author: MohammadRaziei
"""

from mygymPrescan.PrescanEnviroment import *
from time import sleep



class PrescanEnv:
    delay = 0.05  # s

    def __init__(self, enviroment): #, off_set_port=None, desired_velocity_port=None, throttle_flag_port=None, brake_flag_port=None):
        # self.road = Road(road_name)
        # self.car = Vehicle(car_name, self.road)
        ##self.Reward = Reciver_UDP(reward_port)

        # Creating UDP_ports to send the command of actions:
        ##self.off_set_UDP = Transmitter_UDP(off_set_port)  # 8072)
        ##self.desired_velocity_UDP = Transmitter_UDP(desired_velocity_port)  # 8073)
        # self.throttle_flag_UDP = Transmitter_UDP(throttle_flag_port)  # 8074)
        # self.brake_flag_UDP = Transmitter_UDP(brake_flag_port)  # 8075)
        self.enviroment = enviroment
        self.action_space = Discrete(3)
        self.__close__window__ = False
        self.reward_function = None
        self.__render__ = 0



    def create(self, car_name=None, road_name=None):
        self.enviroment.create_model(car_name, road_name)

        ##self.Reward.build()

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        # sim.Restart()
        self.enviroment.reset()
        while True:
            self.render()
            # if self.agent['data']['Position']['x'] < 5:
            if not self.done:
                break
        start_state = [self.agent['data']['Position']["x"], 0]
        return start_state

    def step(self, action):
        if PrescanEnv.delay > 0 :
            sleep(PrescanEnv.delay)
        self.send(action)
        self.render()

        car = self.agent
        observation = [car['data']["Position"]["x"], car['data']["Position"]["y"]]
        reward = self.calc_reward()
        done = self.done
        info = ''
        return observation, reward, done, info



    def render(self):
        self.__render__ += 1
        data = self.enviroment.get()
        self.agent = self.enviroment.agent
        self.time = self.enviroment.data['Time']
        self.done = bool(self.enviroment.data['done'])
            
        return data

    def calc_reward(self):
        reward_T = self.agent['data']['Velocity']





        return reward_T

    def seed(self):
        pass

    def send(self,action):
        self.enviroment.send(action)


    def __del__(self):
        self.close()


    def close(self):
        try:
            sim.Stop()
        except:
            pass
        self.enviroment.close()
        if self.__close__window__:
            sim.Close_window()

  
    @staticmethod
    def __get_state__():
        state = []
        for i in Vehicle.objects:
            data = i.data.get()
            x = data["Position"]["x"]
            v = data["Velocity"]["x"]
            state.append(x)
            state.append(v)
            print("Time: ", data["Time"])
            print(i.name, "position: ", x)
            print(i.name, "speed: ", v, end="\n\n")
        return state
  
'''
    def action_vec_to_commands(self, action, state):
        off_set = action[0]

        if (action[1] == False) and (action[2] == False):
            desired_velocity = state[1]  # speed is not changed
            throttle_flag = 0
            brake_flag = 0

        elif (action[1] == True) and (action[2] == False):
            # desired_velocity = state[1] + 5
            desired_velocity = 20
            throttle_flag = 1
            brake_flag = 0

        elif (action[1] == False) and (action[2] == True):
            desired_velocity = state[1] - 5
            throttle_flag = 0
            brake_flag = 1

        else:
            raise ("ERROR!")

        # self.off_set_UDP.send(off_set)
        # self.desired_velocity_UDP.send(desired_velocity)
        # self.throttle_flag_UDP.send(throttle_flag)
        # self.brake_flag_UDP.send(brake_flag)
'''


def make(experimant_name):
    set_experimant(experimant_name)
    enviroment = Enviroment(outport=8031,inport=(8072,8073,8075))
    # enviroment = Enviroment(outport=8031,inport=8070)
    enviroment.create_model('Toyota_Yaris_Hatchback_1','StraightRoad_22')
    env = PrescanEnv(enviroment)
    sim.Restart()

    return env








__all__ = ['PrescanEnv','sim','Model']






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
