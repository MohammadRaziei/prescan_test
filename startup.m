if ~matlab.engine.isEngineShared
    matlab.engine.shareEngine('MATLAB_PRESCAN_engine')
end
speed = 0.1;
% parfor i = 1:2  
%     if i == 1
%         sim('Experiment_3_cs',inf)
%     end
% end
%         
%         