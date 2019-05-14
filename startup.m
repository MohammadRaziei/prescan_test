if ~matlab.engine.isEngineShared
    matlab.engine.shareEngine('MATLAB_PRESCAN_engine')
end
ExperimentName = 'Experiment_3_cs';
% Experiment = load_system(ExperimentName);

% set_param('Experiment_3_cs','FastRestart','on')
sys = load_system('Experiment_3_cs');





RL = 0;
speed = 1;
% parfor i = 1:2  
%     if i == 1
%         sim('Experiment_3_cs',inf)
%     end
% end
%         
%         