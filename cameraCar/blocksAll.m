 blocksAll_ = find_system('simulink');
 blocksAll_s = jsonencode(blocksAll_);
 
 fid = fopen('BlocksAll.json','w');
 fwrite(fid,blocksAll_s,'char');
 fclose(fid);
