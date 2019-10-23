%%

% This script takes the data acquired from the other script and manipulates it so that Planck's constant can be determined.

y = dlmread('yellow.txt'); % Load in the data for each frequency of light
g = dlmread('green.txt');
b = dlmread('blue.txt');
v = dlmread('Violet.txt');
uv = dlmread('UltraViolet.txt');

%% Method 1 - Low fractional current

% Make an array containing the stopping potentials
Vs1 = -[y(1,end) g(1,end) b(1,end) v(1,end) uv(1,end)] ; 
% Do the same for the frequencies
freq = [5.19 5.5 6.88 7.41 8.22]*10^(14) ;
% Open curve fitting tool and obatin a fittd plot
plot(fittedmodel1)
hold on
% Plot the points as well as the fitted line
plot(freq,Vs1,'rx')
fx = linspace(7.5e14,9e14,400);
% Plot an extrapolated line on the same plot to see where the UV point was
% expected to be using the data from the curve fitting tool
plot(fx,4.125*10^-15*fx-1.466,'b--')
xlabel('Frequency, $\nu$ (Hz)','Interpreter','latex','FontSize',14)
ylabel('Stopping potential, $V_s$ (V)','Interpreter','latex','FontSize',14)
coeff = coeffvalues(fittedmodel1) ;
% Obtain h from multiplying the gradient by the charge of an electron
h = coeff(1)*1.6e-19 ;
% Calculate the standard deviation on the gradient
sd = confint(fittedmodel1,0.68) ;
sdh = (sd(2,1)-sd(1,1))*1.6e-19 ;
plot(8.22e14,1.9245,'ko')
% The error on the stopping potentials was taken as the spacing between the
% points given that 500 points were taken for each.
errorbar(freq,Vs1,0.04*ones(size(freq)),'bx')
%% Method 2 - Sqaure root graph

figure
% Put the voltage values for each frequency into a variable
uvV = uv(1,:);
% Do the same for the current but calculate the normalised current and take
% its square root
uvsqrtI = sqrt(uv(2,:)/0.006227);
hold on
xlim([-2 1])
x = linspace(-2,1,400) ;
% Line equation using the coefficients from the curve fitting tool
uvy = fittedmodeluv.p1*x + fittedmodeluv.p2 ;
% Calculate the stopping potential by rearranging the line equation at zero
% current (x=0)
uvVs = -fittedmodeluv.p2/fittedmodeluv.p1 ;
erruvVs = uvVs*sqrt((0.016975/fittedmodeluv.p1).^2 + ...
    (0.013975/fittedmodeluv.p2).^2);
plot(x,uvy,'m--')
% Do the same for all the other frequencies
vV = v(1,:) ;
vsqrtI = sqrt(v(2,:)/0.02317) ;
vy = fittedmodelv.p1*x + fittedmodelv.p2 ;
vVs = -fittedmodelv.p2/fittedmodelv.p1 ;
errvVs = vVs*sqrt((0.023/fittedmodelv.p1).^2 + ...
    (0.0143/fittedmodelv.p2).^2);
plot(x,vy,'m')

bV = b(1,:) ;
bsqrtI = sqrt(b(2,:)/0.06841) ;
by = fittedmodelb.p1*x + fittedmodelb.p2 ;
bVs = -fittedmodelb.p2/fittedmodelb.p1 ;
errbVs = bVs*sqrt((0.032425/fittedmodelb.p1).^2 + ...
    (0.019325/fittedmodelb.p2).^2);
plot(x,by,'b')

gV = g(1,:) ;
gsqrtI = sqrt(g(2,:)/0.08981) ;
gy = fittedmodelg.p1*x + fittedmodelg.p2 ;
gVs = -fittedmodelg.p2/fittedmodelg.p1 ;
errgVs = gVs*sqrt((0.0665/fittedmodelg.p1).^2 + ...
    (0.031625/fittedmodelg.p2).^2);
plot(x,gy,'g')

yV = y(1,:) ;
ysqrtI = sqrt(y(2,:)/0.04929) ;
yy = fittedmodely.p1*x + fittedmodely.p2 ;
yVs = -fittedmodely.p2/fittedmodely.p1 ;
erryVs = yVs*sqrt((0.08475/fittedmodely.p1).^2 + ...
    (0.03585/fittedmodely.p2).^2);
plot(x,yy,'y')
legend('Ultra violet','Violet','Blue','Green','Yellow')
% Add the stopping potentials to the graph as red circles but make them
% invisible to the legend on the figure
plot(uvVs,0,'rx','HandleVisibility','off')
plot(vVs,0,'rx','HandleVisibility','off')
plot(bVs,0,'rx','HandleVisibility','off')
plot(gVs,0,'rx','HandleVisibility','off')
plot(yVs,0,'rx','HandleVisibility','off')

% Add errorbars to the stopping potential points
Vs2 = -[yVs gVs bVs vVs uvVs] ;
err = [erryVs errgVs errbVs errvVs erruvVs] ;
errorbar(-Vs2,zeros(size(Vs2)),err,'horizontal','r','HandleVisibility','off')

ylim([0,2])
xlabel('Applied potential, $V$ (V)','Interpreter','latex','FontSize',14)
ylabel('Square root normalised current, $\sqrt{I}$','Interpreter',...
    'latex','FontSize',14)

%%

% Plot the stopping potential-frequency graph for the new stopping
% potentials
fx1 = linspace(5e14,9e14,400) ;
m2y = fittedmodel2.p1*fx1 + fittedmodel2.p2 ;
plot(fx1,m2y,'r-')
hold on
plot(freq,Vs2,'bx')
errorbar(freq,Vs2,err,'bx')
xlabel('Frequency, $\nu$ (Hz)','Interpreter','latex','FontSize',14)
ylabel('Stopping potential, $V_s$ (V)','Interpreter','latex','FontSize',14)

coeff2 = coeffvalues(fittedmodel2) ;
h2 = coeff2(1)*1.6e-19 ;
sd2 = confint(fittedmodel2,0.68) ;
sdh2 = (sd2(2,1)-sd2(1,1))*1.6e-19 ;
