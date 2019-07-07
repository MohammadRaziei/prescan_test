function udp_connect()
    root = ['cameraCar_cs' '_UDP']; root_main = 'cameraCar_cs';
    copyfile([root_main '.slx'] ,[root '.slx'])
    sys = load_system(root);
    block = '/Toyota_Yaris_Hatchback_1';
    name = 'test';
%     add_block('simulink/Commonly Used Blocks/Constant',[root block '/' name],'Value','5');
    add_block('dspsnks4/UDP Send',[root block '/' name '_UDP']);
    add_block('embeddedtargetslib/Host Communication/Byte Pack',[root block '/' name '_BytePack']);
%     add_block('xpcutilitieslib/Byte Packing ',[root block '/' name '_BytePack']);
    add_block('simulink/Discrete/Zero-Order Hold',[root block '/' name '_ZeroOrderHold']);
    add_line([root block],[name '_ZeroOrderHold/1'],[name '_BytePack/1']);
    add_line([root block],[name '_BytePack/1'],[name '_UDP/1']);
%     add_block('simulink/Sinks/Scope','vdp/Scope','MakeNameUnique','on')


% {'double'}
%     block2 = [root block '/' name '_BytePack']
%     s = get_param(block2, 'DialogParameters')
    pause(2)
    save_system(sys)
    close_system(sys)
end