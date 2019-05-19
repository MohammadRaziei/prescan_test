# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:47:01 2019

@author: MohammadRaziei
"""
import os,numpy as np
port = 9620

def find_and_kill_port(port):
    result = os.popen("netstat -ano | findstr :{} | findstr ESTABLISHED".format(port)).read().strip()
    if result != '' :
        pid = result.split(" ")[-1]
        os.popen("taskkill /PID {} /F".format(pid))
if __name__ == '__main__':
    find_and_kill_port(port)
else:
    eng = None
    
    ExperimentName = ''
    bdroot = ''
    prescanFile = ''
    def set_experimant(ExpName):
        global ExperimentName,bdroot,prescanFile
        ExperimentName = ExpName
        bdroot = ExperimentName+"_cs"
        prescanFile = ExperimentName+".pb"
    
    
    def getDefaultFilename():
        eng.prescan.experiment.getDefaultFilename
    
    
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
            The software returns 'stopped', 'initializing', 'running', 'paused', 'compiled', 'updating', 'terminating', or 'external' (used with the Simulink Coder™ product).
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
        __shared_flags__ = {'create_model':False}
        def __init__(self, name, model):
            self.create_model_ones()
            self.name = name
            self.model = model
            self.id = Model.objectsFindByName(name)
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
        def __init__(self, name = 'StraightRoad_1'):
            Model.__init__(self,name,'Road')
            self.length = self.object['road']['straightRoad']['roadLength']
            self.numberOfLanes = len(self.object['road']['roadEnds'][0]['laneEnds'])
            self.laneWidth = self.object['road']['roadEnds'][0]['laneEnds'][0]['width']
    
    class Car(Model):
        def __init__(self, name,road = None):
            Model.__init__(self,name,'Car')
            self.road = road
        
        def get_position(self,runtime = True):
            if runtime == True:
                if sim.Status() == 'stopped':
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
                if eng.exist('Positions') and ( sim.Status() in ['paused','stopped'] ):
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
            pos_y = self.get_position_road()[1] / __road__.laneWidth
            pos_y_offset = __road__.numberOfLanes / 2 
            lane = int(np.floor(pos_y/__road__.numberOfLanes) + pos_y_offset)
            return lane
    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        