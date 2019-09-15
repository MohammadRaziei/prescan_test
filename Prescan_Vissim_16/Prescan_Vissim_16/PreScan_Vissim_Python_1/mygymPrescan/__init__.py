# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:47:01 2019

@author: MohammadRaziei
"""

from mygymPrescan.PrescanEnv import *

def make(experimant_name):
    set_experimant(experimant_name)
    enviroment = Enviroment(outport=8031,inport=8070)
    enviroment.create_model('Toyota_Yaris_Hatchback_1','StraightRoad_22')
    env = PrescanEnv(enviroment)
    sim.Restart()

    return env



# class Time:
#     step = 0.005
#     @staticmethod
#     def Range(t_end,steps=Time.step):
#         return range(int(t_end/steps))

#     @staticmethod
#     def At(t,steps=Time.step):
#         return int(t/steps)



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
