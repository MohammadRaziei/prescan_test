# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:47:01 2019

@author: MohammadRaziei
"""

import socket
import struct, json
import random
from datetime import datetime
from time import sleep

import os, numpy as np

port = 9620


def find_and_kill_port(port):
    result = os.popen("netstat -ano | findstr :{} | findstr ESTABLISHED".format(port)).read().strip()
    if result != '':
        pid = result.split(" ")[-1]
        os.popen("taskkill /PID {} /F".format(pid))


ExperimentName = ''
bdroot = ''
prescanFile = ''


def set_experimant(ExpName):
    global ExperimentName, bdroot, prescanFile
    ExperimentName = ExpName
    bdroot = ExperimentName + "_cs"
    prescanFile = ExperimentName + ".pb"


def getDefaultFilename():
    eng.prescan.experiment.getDefaultFilename()


def objectsFindByName(name):
    global ExperimentName
    eng.eval(ExperimentName + "_models = prescan.experiment.readDataModels('" + ExperimentName + ".pd');", nargout=0)
    return int(
        eng.eval("prescan.worldmodel.objectsFindByName(" + ExperimentName + "_models.worldmodel, '" + name + "')"))


class sim:
    global bdroot

    @staticmethod
    def Update():
        eng.set_param(bdroot, 'SimulationCommand', 'update', nargout=0)

    @staticmethod
    def Pause():
        eng.set_param(bdroot, 'SimulationCommand', 'pause', nargout=0)

    @staticmethod
    def Continue():
        eng.set_param(bdroot, 'SimulationCommand', 'continue', nargout=0)

    @staticmethod
    def Stop():
        eng.set_param(bdroot, 'SimulationCommand', 'stop', nargout=0)

    @staticmethod
    def Start():
        eng.set_param(bdroot, 'SimulationCommand', 'start', nargout=0)

    @staticmethod
    def Restart():
        eng.set_param(bdroot, 'SimulationCommand', 'stop', nargout=0)
        eng.set_param(bdroot, 'SimulationCommand', 'start', nargout=0)

    @staticmethod
    def Status():
        '''
        The software returns 'stopped', 'initializing', 'running', 'paused', 'compiled', 'updating', 'terminating', or 'external'.
        '''
        return eng.get_param(bdroot, 'SimulationStatus')

    @staticmethod
    def Time():
        return eng.get_param(bdroot, 'SimulationTime')


def python2matlab(**args):
    for key, value in args.items():
        eng.workspace[key] = eng.double(value)


def matlab2python(*args):
    for arg in args:
        globals()[arg] = eng.workspace[arg]


def pysim_update(**args):
    python2matlab(**args)
    sim.Update()


def prescan_regenerate():
    global bdroot, eng
    eng.generate_all(bdroot)


class Model():
    global ExperimentName, bdroot
    __shared_flags__ = {'create_model': False, 'objects': []}

    def __init__(self, name, model):
        Model.__shared_flags__['objects'].append(self)
        self.name = name
        self.model = model

    def create(self):
        self.create_model_ones()
        self.id = Model.objectsFindByName(self.name)
        self.object = eng.eval(ExperimentName + "_models.worldmodel.object{" + str(self.id) + ", 1} ")
        self.position = self.object['pose']['position']
        self.orientation = self.object['pose']['orientation']

    def __del__(self):
        self.close()

    def close(self):
        Model.__shared_flags__['objects'].remove(self.name)
        print('{} closed!'.format(self.name))
    @staticmethod
    def create_model():
        eng.eval(ExperimentName + "_models = prescan.experiment.readDataModels('" + ExperimentName + ".pb');",
                 nargout=0)

    def create_model_ones(self):
        if (not Model.__shared_flags__['create_model']) and (eng.exist(ExperimentName + '_models') != 1):
            Model.create_model()
            Model.__shared_flags__['create_model'] = True

    @staticmethod
    def objectsFindByName(name):
        return int(
            eng.eval("prescan.worldmodel.objectsFindByName(" + ExperimentName + "_models.worldmodel, '" + name + "')"))

    @staticmethod
    def Update(**args):
        python2matlab(**args)
        sim.Update()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{}({!r})'.format(self.model, self.name)


class Road(Model):
    __shared_flags__ = {'objects': []}

    def __init__(self, name=None):
        __name__ = name if name is not None else 'StraightRoad_1'
        Road.__shared_flags__['objects'].append(self)
        Model.__init__(self, __name__, 'Road')

    def create(self):
        super().create()
        self.length = self.object['road']['straightRoad']['roadLength']
        self.numberOfLanes = len(self.object['road']['roadEnds'][0]['laneEnds'])
        self.laneWidth = self.object['road']['roadEnds'][0]['laneEnds'][0]['width']

    def close(self):
        Vehicle.__shared_flags__['objects'].remove(self.name)
        super().close()

class Vehicle(Model):
    __shared_flags__ = {'objects': []}

    def __init__(self, name, data_port=None, road=None):
        Vehicle.__shared_flags__['objects'].append(self)
        Model.__init__(self, name, 'Vehicle')
        self.road = road
        self.port = data_port

    def create(self, data_port=None):
        super().create()
        self.port = data_port if data_port is not None else self.port
        self.data = Reciver_UDP_json(self.port)
        self.data.build()
    def close(self):
        self.data.close()
        Vehicle.__shared_flags__['objects'].remove(self.name)
        super().close()

class Discrete:
    r"""A discrete space in :math:`\{ 0, 1, \\dots, n-1 \}`.
    Example::
        >>> Discrete(2)
    """
    def __init__(self, n):
        assert n >= 0
        self.n = n

    def __repr__(self):
        return "Discrete(%d)" % self.n


#############################################################
class Environment:
    delay = 0.05#s
    def __init__(self, car_name=None, car_port=None, reward_port=None, road_name=None,
                 off_set_port=None, desired_velocity_port=None, throttle_flag_port=None, brake_flag_port=None):
        self.road = Road(road_name)
        self.car = Vehicle(car_name, car_port, self.road)
        self.Reward = Reciver_UDP(reward_port)

        # Creating UDP_ports to send the command of actions:
        self.off_set_UDP = Transmitter_UDP(off_set_port)#8072)
        self.desired_velocity_UDP = Transmitter_UDP(desired_velocity_port)#8073)
        self.throttle_flag_UDP = Transmitter_UDP(throttle_flag_port)#8074)
        self.brake_flag_UDP = Transmitter_UDP(brake_flag_port)#8075)

        self.action_space = Discrete(3)

    def create(self):
        self.road.create()
        self.car.create()
        self.Reward.build()

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        sim.Restart()
        start_state = [self.car.position["x"], 0]
        return start_state

    def step(self, action):
        sleep(Environment.delay)

        car_data = self.car.data.get()
        observation = [car_data["Position"]["x"], car_data["Position"]["y"]]
        reward = self.Reward.get()
        done = False
        info = ''
        return observation, reward, done, info

    def __del__(self):
        self.close()

    def close(self):
        for model in Model.__shared_flags__['objects']:
            model.close()
        eng.quit()

    def render(self):
        pass

    def seed(self):
        pass

    @staticmethod
    def __get_state__():
        state = []
        for i in Vehicle.__shared_flags__['objects']:
            data = i.data.get()
            x = data["Position"]["x"]
            v = data["Velocity"]["x"]
            state.append(x)
            state.append(v)
            print("Time: ", data["Time"])
            print(i.name, "position: ", x)
            print(i.name, "speed: ", v, end="\n\n")
        return state

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
            raise("ERROR!")

        self.off_set_UDP.send(off_set)
        self.desired_velocity_UDP.send(desired_velocity)
        self.throttle_flag_UDP.send(throttle_flag)
        self.brake_flag_UDP.send(brake_flag)

def make(experimant_name):
    globals()['eng'] = matlab.engine.connect_matlab()
    set_experimant(experimant_name)
    env = Environment(car_name='Toyota_Yaris_Hatchback_1', car_port=8091,
                      reward_port=8081,
                      road_name='StraightRoad_1',
                      off_set_port=8072, desired_velocity_port=8073, throttle_flag_port=8074, brake_flag_port=8075
                      )
    env.create()
    return env



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
        # if x[0] >= 0:
        # print(self.name,": ", x[0])
        return x[0]

    def __del__(self):
        self.close()

    def close(self):
        self.this_socket.close()


class Reciver_UDP_json:
    def __init__(self, port_number=0):
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def build(self):
        self.this_socket.bind(("", self.port_number))
        print("waiting on port:", self.port_number)

    def get(self):
        data, addr = self.this_socket.recvfrom(1024)
        data = json.loads(data.decode("utf-8"))
        return data

    def get_str(self):
        data, addr = self.this_socket.recvfrom(1024)
        return data.decode("utf-8")

    def __del__(self):
        self.close()

    def close(self):
        self.this_socket.close()


class Transmitter_UDP:

    def __init__(self, port_number=0, host='localhost', this_socket=None):
        self.port_number = port_number
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        print("Sending data to port: ")

    def send(self, ac):
        y = struct.pack("d", ac)
        self.this_socket.sendto(y, (self.host, self.port_number))
        print("The Action is: ", ac)

    def close(self):
        self.this_socket.close()


class Q_network:

    # Set learning parameters
    lr = .8
    y = .95
    num_episodes = 2000

    def __init__(self, env):
        self.env = env
        # Initialize table with all zeros
        self.Q = np.array([env.observation_space.n, env.action_space.n])
        self.index = 0

    def feed(self, state):
        best_action = []

        # Neural network out put is the Q-values for all available actions.
        # All available actions are 9 actions; Each of them is a vector of 3 values : [off_set, speed_up, speed_down]
        # We need to select the action with max Q-value
        # Assume this action is a4 = [3.5, True, False]
        # ran = 1
        ran = random.randint(-2, 3)
        laneWidth = env.car.road.laneWidth
        best_action = [(laneWidth * ran), True, False]
        print(best_action)
        return best_action

    def feed2(self,state,episode_num=1):


        # create lists to contain total rewards and steps per episode
        # jList = []

        self.epoch = episode_num
        # Choose an action by greedily (with noise) picking from Q table
        self.action = np.argmax(self.Q[self.state, :] + np.random.randn(1, self.env.action_space.n) * (1. / (self.epoch + 1)))
        return self.action

    def update(self,next_state):
        # Update Q-Table with new knowledge
        self.Q[self.state, self.action] = self.Q[self.state, self.action] + lr * (r + y * np.max(self.Q[self.next_state, :]) - self.Q[self.state, self.action])




'''
def reset_environment():
    
    car_pose_reset.send(1)
    car_speed_reset.send(1)
    other1_pose_reset.send(1)
    other1_speed_reset.send(1)
'''

import matlab.engine
if __name__ == '__main__':
    env = make('cameraCar')
    QNet = Q_network(env)
    # Creating enviroment



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
    i = 0
    timeVector = []

    start_state = env.reset()
    # while True:
    #     experience = np.array([])
    #
    #     print("________________________________")
    #     print("Iteration #", i)
    #     i = i + 1
    #
    #     # state
    #     state = get_state()
    #     # experience.append(state)
    #
    #     experience = np.append(experience, state)
    #
    #     # action
    #     action_vec = main_Q_Network.feed(state)
    #     # experience.append(action_vec)
    #     experience = np.append(experience, action_vec)
    #
    #     # sendig commands to PreScan
    #     action_vec_to_commands(action_vec, state)
    #
    #     # reward
    #     r = Reward.get()
    #     # experience.append(r)
    #     experience = np.append(experience, r)
    #
    #     # next state
    #     next_state = get_state()
    #     # experience.append(next_state)
    #     experience = np.append(experience, next_state)
    #
    #     print("Experience: ", experience)
    #     # print("Experience_shape:", experience.shape())
    #     Replay_memory.append(experience)
    #
    #     time = datetime.now().time()
    #     print("Time:", time)
    #     timeVector.append(time)
    #
    #     print(repr(car.data.get_str()))

    # -------------------------------------------------------

    lr = Q_network.lr
    y = Q_network.y
    num_episodes = Q_network.num_episodes
    rList = []
    for i in range(num_episodes):
        print("________________________________")
        print("Iteration #", i)
        # Reset environment and get first new observation
        state = env.reset()
        rAll = 0
        done = False
        j = 0
        # The Q-Table learning algorithm
        while j < 99:
            j += 1
            action = QNet.feed2(state, i)
            # Get new state and reward from environment
            next_state, reward, done, _ = env.step(action)
            print()
            QNet.update(state)
            rAll += reward*y
            state = next_state
            if done:
                break
        # jList.append(j)
        rList.append(rAll)

    print("Score over time: " + str(sum(rList) / num_episodes))

    print("Final Q-Table Values")
    print(Q)