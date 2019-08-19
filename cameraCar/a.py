main_Q_Network = Q_network("mainQN")
# Creating traffic
road = Road('StraightRoad_1')
road.create()
car = Vehicle('Toyota_Yaris_Hatchback_1', 8091, road)
car.create()

Reward = Reciver_UDP(8081)
Reward.build()

# Creating UDP_ports to send the command of actions:
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
i = 0
timeVector = []

while 1:
    experience = np.array([])

    print("________________________________")
    print("Iteration #", i)
    i = i + 1

    # state
    state = get_state()
    # experience.append(state)

    experience = np.append(experience, state)

    # action
    action_vec = main_Q_Network.feed(state)
    # experience.append(action_vec)
    experience = np.append(experience, action_vec)

    # sendig commands to PreScan
    action_vec_to_commands(action_vec, state)

    # reward
    r = Reward.get()
    # experience.append(r)
    experience = np.append(experience, r)

    # next state
    next_state = get_state()
    # experience.append(next_state)
    experience = np.append(experience, next_state)

    print("Experience: ", experience)
    # print("Experience_shape:", experience.shape())
    Replay_memory.append(experience)

    time = datetime.now().time()
    print("Time:", time)
    timeVector.append(time)

    print(repr(car.data.get_str()))









