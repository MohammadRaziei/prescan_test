add_block('simulink/Commonly Used Blocks/Constant','connect_model/Constant');
set_param('connect_model/Constant','position',[140,80,180,120]);
add_block('simulink/Commonly Used Blocks/Gain','connect_model/Gain');
set_param('connect_model/Gain','position',[220,80,260,120]);
% Connect the blocks. Each block has one port, so specify port 1.
add_line('connect_model','Constant/1','Gain/1');
set_param(gcb,'AttributesFormatString','pri=%<priority>\ngain=%<Gain>')