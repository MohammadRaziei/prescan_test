function json = fcn(input) %BY @MohammadRaziei
coder.extrinsic('num2str','bdroot','get_param');
p = 15;
pt = 10;
input(isnan(input)) = 0;
u = zeros(9,p);
m = num2str(input(:), ['%0.' num2str(p) 'g ']);
sss = 1:p;
u(1,sss) = m(1,sss);    
u(2,sss) = m(2,sss);
u(3,sss) = m(3,sss);
u(4,sss) = m(4,sss);
u(5,sss) = m(5,sss);
u(6,sss) = m(6,sss);
u(7,sss) = m(7,sss);
u(8,sss) = m(8,sss);
u(9,sss) = m(9,sss);

t = num2str(round(get_param(bdroot,'SimulationTime'),pt),['%0.' num2str(pt) 'g ']);
ts = (32*ones(1,pt));
ts(1:pt) = t(1,1:pt);

len = (89 + 9*p) + (8 + pt);
json = uint8(32*ones(1,len));
json(1:end) = uint8(['{"Time":' ts ',"Position":{"x":' u(1,:) ',"y":' u(2,:) ',"z":' u(3,:) '},' ...
        '"Velocity":{"x":' u(4,:) ',"y":' u(5,:) ',"z":' u(6,:) '},' ...
        '"Acceleration":{"x":' u(7,:) ',"y":' u(8,:) ',"z":' u(9,:) '}}']);
json = uint8(json);