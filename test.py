import matlab.engine
future = matlab.engine.connect_matlab(background=True)
eng = future.result()

eng.matlab_aa(nargout=0)