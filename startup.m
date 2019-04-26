if ~matlab.engine.isEngineShared
    matlab.engine.shareEngine('MATLAB_PRESCAN_engine')
end