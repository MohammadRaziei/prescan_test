% findObjects.m
% read data models from the default file
models = prescan.experiment.readDataModels();
% find DAF_95_XF_1 and DAF_95_XF_2 trucks
vehicles = {'DAF_95_XF_1', 'DAF_95_XF_2'};
indices = prescan.worldmodel.objectsFindByName(models.worldmodel, vehicles);
% print info of the found objects
if ~isempty(indices)
    objects = models.worldmodel.object(indices);
    for i = 1 : numel(objects)
        disp('Found vehicle: ');
        disp(objects{i});
    end
end