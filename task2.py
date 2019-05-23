# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:46:42 2019

@author: MohammadRaziei
"""

import numpy as np
from time import sleep



import json
def save_json(data):
    with open(data + '.json', 'w') as f:
        json.dump(globals()[data], f, ensure_ascii=False)
        

def nargout(func):
    return int( eng.eval('nargout(@'+func+')') )





#---------------------------------------------------------
def run_senario():
    road = prescan.Road('StraightRoad_1')
    car = prescan.Car('Audi_A8_Sedan_1',road)
    print('{!r}\t{!r}'.format(car,road))
    
    prescan.sim.Restart()
    print('>> Start')
    
    lane_start = car.examinLane() 
    print('lane_start : {}'.format(lane_start))
    for i in range(2):
        RL,RL2 = 0,0
        while True:
            sleep(2)
            time = prescan.sim.Time()
            print("time : {}".format(time) )
            x, y = car.get_position_road()
            lane = car.examinLane()
            if lane == road.numberOfLanes - 1:
                RL2 += np.random.randint(-1,1)
            elif lane == 0:
                RL2 += np.random.randint(0,2)
            else :
                RL2 += np.random.randint(-1,2) 
            RL = RL2 - lane_start
            print('lane = {} -> RL = {}'.format(lane,RL))
            print('\tx = {}\n\ty = {}'.format(x,y))
            RL = RL * road.laneWidth
            prescan.Model.Update(RL=RL)
            if not car.is_in_road():
                RL,RL2 = 0,0
                prescan.Model.Update(RL=RL)
                prescan.sim.Restart()
                print('>> Restart')
                break
        
        prescan.sim.Stop()  
        print('>> Stop')   
###########################################################
import matlab.engine
try:
    eng = matlab.engine.connect_matlab('MATLAB_PRESCAN_engine')
except:
    pass


import prescan
prescan.set_experimant("Experiment_3")
prescan.eng = eng


try:
    
    run_senario() 

    print('The End')
except:
    eng.quit()
    pass
eng.quit()

