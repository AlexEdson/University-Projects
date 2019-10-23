%% Equipement configuration

% This script can be used to configure the equipment required and acquire the data need to calculate Planck's constant using
% the photoelectric effect.

daq.reset       % Reset the device and clear the workspace
clear, close all
s = daq.createSession('ni');
s.addAnalogInputChannel('Dev1',0,'Voltage'); 
s1 = daq.createSession('ni');
s1.addAnalogOutputChannel('Dev1',0,'Voltage'); 
% Set up input and output channels

s.Rate = 1000; s.NumberOfScans = 500; % Set scan rate and number of scans

%% Defining variables for the loop and calculating constants


V = -9; % Apply LARGE reverse bias current to zero the input signal
outputSingleScan(s1,V)
pause(7) % Gives system time to adjust to new applied voltage
[data] = startForeground(s);
I_bias = mean(data);  % Small reverse bias current

V = 0; % Obatin zero potential current to normalise input signal
outputSingleScan(s1,V)
pause(7)
[data] = startForeground(s);
I0 = mean(data) - I_bias; % Take mean of 500 scans

I_new = 50 ; % Arbitrary current
I = [] ;
V = 0.2; 
Volt = V; % First value of voltage array for graph later

%% Data collection loop

while I_new > 0.001*I0
    outputSingleScan(s1,V)
    pause(7)
    data = startForeground(s);
    I_new = mean(data)-I_bias ;
    I = [I I_new] ; % Adds new current value to array for graphing later
    plot(Volt,I) % Replots graph for every loop iteration so outcome of loop could be seen and experiment progress could be monitored
    
    if I_new > 0.25*I(1) % Comparing current with initial current
        V = V-0.2; % Take points more sparsely at higher voltages
    else
        V = V-0.04; % Take points closer together on approach to stopping potential
    end
    
    Volt = [Volt V];
end

%% Saving data

data = [Volt(1:numel(Volt)-1); I];
dlmwrite('UltraViolet.txt',data) % Saves data for each frequency of light to a text file
daq.reset % Now recalibrate experimental setup for next frequency of light
