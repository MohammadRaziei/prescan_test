%     Experiment_cs = 'C:\Users\Public\Documents\Experiments\mohammad\Experiment_1\Experiment_1_cs';
% % % % % 
% % % % % prescan = @(file) run(['C:\Program Files\PreScan\PreScan_8.4.0\' file]);
% % % % % old_dir = pwd;
% % % % % 
% % % % % prescan('prescan_startup.p')
% % % % % prescan( 'SimCore_startup_common.p')
% % % % % prescan('prescan_Settings.p')
% % % % % prescan('prescan_version.p')
% % % % % cd(old_dir);
% % % % % disp('Done!');
Simulation_Time = 5;%seconds
%while 1

%    speed = input('Speed :  ');
%    if speed == 0
%        break
%    end
    speed = 0.1;
    sim("Experiment_3_cs",Simulation_Time)
    disp('Done!')
%    close all;
%end
disp(gcs);
paramValue = get_param('Experiment_3_cs/Audi_A8_Sedan_1/InitialVelocity','Value');