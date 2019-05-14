% % RL = 10
% % % set_param('Experiment_3_cs/Audi_A8_Sedan_1/RL','Value','RL')
% % set_param('Experiment_3_cs','SimulationCommand','update')
% % 
% % 
% % 
% % 
% % get_param('Experiment_3_cs/Audi_A8_Sedan_1','Value')

% printFieldValue.m
% read data models from the default file
models = prescan.experiment.readDataModels();
% get the name of the first object in worldmodel
objectName = prescan.experiment.getFieldValue(models.worldmodel.object, 'name');
%print the found field content
disp('The content of the field "name" is:');
disp(objectName)

