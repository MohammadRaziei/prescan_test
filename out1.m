%The GUI handles are by default hidden, turn them on
set(0,'ShowHiddenHandles','on');
%Set up the arguments that will go into the gain block event callback listener
% blk = 'mytestmdl/Gain';
blk = 'Experiment_3_cs/Audi_A8_Sedan_1/SELF_Demux';
event = 'PostOutputs';
listener = @updategui;
%Create the listener
h = add_exec_event_listener(blk, event, listener);