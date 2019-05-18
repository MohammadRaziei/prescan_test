# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:47:01 2019

@author: MohammadRaziei
"""
import os
port = 9620

#gcs = 'Experiment_3_cs/Audi_A8_Sedan_1'
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
    global prescanFile
    eng.eval("models = prescan.experiment.readDataModels('"+ExperimentName+".pd');",nargout=0)
    return int(eng.eval("prescan.worldmodel.objectsFindByName(models.worldmodel, '"+name+"')") )

class sim:
    def Update(self):
        global bdroot,eng
        eng.set_param(bdroot,'SimulationCommand','update',nargout=0)
    def Pause(self): 
        global bdroot,eng
        eng.set_param(bdroot,'SimulationCommand','pause',nargout=0)
    def Continue(self):
        global bdroot,eng
        eng.set_param(bdroot,'SimulationCommand','continue',nargout=0)
    def Stop():
        global bdroot,eng
        eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
    def Start():
        global bdroot,engs
        eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
    def Restart():
        global bdroot,eng
        eng.set_param(bdroot,'SimulationCommand','stop',nargout=0)
        eng.set_param(bdroot,'SimulationCommand','start',nargout=0)
    def Status():
        global bdroot,eng
        return eng.get_param(bdroot,'SimulationStatus')
        #The software returns 'stopped', 'initializing', 'running', 'paused', 'compiled', 'updating', 'terminating', or 'external' (used with the Simulink Coder™ product).
    def Time():
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
           





























def find_and_kill_port(port):
    result = os.popen("netstat -ano | findstr :{} | findstr ESTABLISHED".format(port)).read().strip()
    if result == '' :
        pid = result.split(" ")[-1]
        os.popen("taskkill /PID {} /F".format(pid))
if __name__ == '__main__':
    find_and_kill_port(port)