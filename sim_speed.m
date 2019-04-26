% speed = 0.10;

set_param('Experiment_3_cs/Audi_A8_Sedan_1/InitialVelocity','Value','speed')
set_param('Experiment_3_cs','SimulationCommand','update')

set_param('Experiment_3_cs','SimulationCommand','pause')
set_param('Experiment_3_cs','SimulationCommand','continue')
set_param('Experiment_3_cs','SimulationCommand','stop')
set_param('Experiment_3_cs','SimulationCommand','start')

set_param('Experiment_3_cs','FastRestart','on')

