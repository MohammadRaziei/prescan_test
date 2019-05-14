% experiment_system = load_system('Experiment_3_cs');
models = prescan.experiment.readDataModels('Experiment_3.pb');
% % prescan.experiment.writeDataModels(models);
% simOut = prescan.experiment.runWithDataModels(models);
% 



% prescan.worldmodel.articulatedActorsFindByObjectName(models.worldmodel, 'Audi_A8_Sedan_1')
% prescan.worldmodel.objectsFindByName(models.worldmodel, 'Audi_A8_Sedan_1')

road_obj = models.worldmodel.object{prescan.worldmodel.objectsFindByName(models.worldmodel, 'StraightRoad_1') , 1}.road;

laneEnds = road_obj.roadEnds{1, 1}.laneEnds;
numberOfLanes = length(laneEnds);
laneWidth = laneEnds{1}.width;
roadLength = road_obj.straightRoad.roadLength;

pos_RL =  randi(4,1,100);  
def_rl = [1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1 1 -1];


% simOut = prescan.experiment.run(models);
sys = load_system('Experiment_3_cs');
set_param('Experiment_3_cs','SimulationCommand','start')
rto.CurrentTime

block = 'Experiment_3_cs/Audi_A8_Sedan_1/To Workspace';
rto = get_param(block, 'RuntimeObject');



for i=1:30
   pause(5);
   RL = def_rl(i);
   set_param('Experiment_3_cs','SimulationCommand','update'); 
   rto
%    models = prescan.experiment.readDataModels('Experiment_3.pb');
%    x = models.worldmodel.object{1, 1}.pose.position.x;
%    y = models.worldmodel.object{1, 1}.pose.position.y;
   disp(['x = ' num2str(x) ' ; y = ' num2str(y)])
   
end






