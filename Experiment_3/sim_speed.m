% speed = 0.10;

set_param('Experiment_3_cs/Audi_A8_Sedan_1/InitialVelocity','Value','speed')
set_param('Experiment_3_cs','SimulationCommand','update')

set_param('Experiment_3_cs','SimulationCommand','pause')
set_param('Experiment_3_cs','SimulationCommand','continue')
set_param('Experiment_3_cs','SimulationCommand','stop')
set_param('Experiment_3_cs','SimulationCommand','start')

set_param('Experiment_3_cs','FastRestart','on')
GlobalParameterValue = get_param(0,'CurrentSystem');
BlockTypes = get_param(BlockPaths,'BlockType');

get_param('Experiment_3_cs/Audi_A8_Sedan_1/SELF_Demux','name')

experiment = load_system('Experiment_3_cs');
models = prescan.experiment.readDataModels('Experiment_3.pb');
% prescan.experiment.writeDataModels(models);
simOut = prescan.experiment.runWithDataModels(models);


filename = prescan.experiment.getDefaultFilename();
[value, result] = prescan.experiment.getFieldValue(inStruct, name)



block = 'Experiment_3_cs/Audi_A8_Sedan_1/To Workspace';

rto = get_param(block, 'RuntimeObject');
time = rto.OutputPort(1).Data;


block = 'Experiment_3_cs/Scope1';
s = get_param(block, 'DialogParameters')


block_2 = 'Experiment_3_cs/Audi_A8_Sedan_1/SELF_Demux';
rto_2 = get_param(block_2, 'RuntimeObject');


rto = get_param('Experiment_3_cs/Audi_A8_Sedan_1/', 'RuntimeObject');
get_param('Experiment_3_cs/Audi_A8_Sedan_1/','DialogParameters')
get_param(block,'DialogParameters')

get_param('Experiment_3_cs/Audi_A8_Sedan_1/Display','DialogParameters')
aa = get_param('Experiment_3_cs/Audi_A8_Sedan_1/Display','ObjectParameters')


% % % % % % % % % % % % % % % % % % % % % % % % 
% block = gcbh
block = 'Experiment_3_cs/Audi_A8_Sedan_1/Display';
rto = get_param(block,'RuntimeObject');
rto.InputPort(1).Data


block = 'Experiment_3_cs/Audi_A8_Sedan_1/To Workspace';
rto = get_param(block,'RuntimeObject');
rto.InputPort(1).Data


rto.InputPort(1).Data,  rto_2.InputPort(1).Data


% % % % % % % % % % % % % % % % % % % % % % 
block = 'Experiment_3_cs/Audi_A8_Sedan_1/Terminator_6';
rto = get_param(block,'RuntimeObject')
rto.OutputPort(1).Data

% % % % % % % % % % % % % % % % % % % % % % % % % % % % 
set_param('Experiment_3_cs/Audi_A8_Sedan_1/SELF_Demux/Bus Selector','OutputAsBus','on')
set_param('Experiment_3_cs/Audi_A8_Sedan_1/SELF_Demux/Bus Selector','OutputAsBus','on')

get_param('Experiment_3_cs/Audi_A8_Sedan_1/','DialogParameters')
aa = get_param('Experiment_3_cs/Audi_A8_Sedan_1/To Workspace','SaveFormat')



mdlWks = get_param(bdroot,'ModelWorkspace');
varList = whos(mdlWks)
varValue = getVariable(mdlWks,'simout_2');


