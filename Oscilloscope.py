# Signal Processing
from scipy import signal
from numpy.fft import fft
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np
import sys

# This code generates an oscilloscope that can perform a Fourier transform on sine, sawtooth and square waves.

class oscope_class:

    def __init__(self):

        self.fig = plt.figure(figsize=(18,9))
        self.ax1 = plt.axes([0.05,0.8,0.9,0.15])
        self.ax2 = plt.axes([0.05,0.5,0.9,0.25])
        self.axpow = plt.axes([0.125, 0.28, 0.05, 0.1])
        self.powerHandle = widgets.RadioButtons(self.axpow, ('On','Off'))
        self.axshape = plt.axes([0.2,0.28,0.08,0.12])
        self.shapeHandle = widgets.RadioButtons(self.axshape, ('Sine','Sawtooth','Square'))
        self.axpoint = plt.axes([0.1,0.07,0.8,0.05])
        self.pointHandle  = widgets.Slider(self.axpoint,'Number of points',10,2000,valstep=1,valinit = 300)
        self.N = int(self.pointHandle.val)
        self.axfreq = plt.axes([0.1,0.19,0.8,0.05])
        self.freqHandle = widgets.Slider(self.axfreq,'Frequency (Hz)',0.5,100,valinit = 30)
        self.f = self.freqHandle.val
        self.axtime = plt.axes([0.1,0.13,0.8,0.05])
        self.timeHandle = widgets.Slider(self.axtime,'Time (s)',1,10,valinit=1)
        self.t = self.timeHandle.val
        self.time = np.linspace(0,self.t,self.N)
        self.axphase = plt.axes([0.1,0.01,0.8,0.05])
        self.phaseHandle = widgets.Slider(self.axphase,'Phase',0,2*np.pi,valinit=0)
        self.p_shift = self.phaseHandle.val
        self.axnoise = plt.axes([0.4,0.36,0.15,0.05])
        self.noiseHandle = widgets.Slider(self.axnoise,'Noise',0,1,valinit = 0)
        self.deviation = self.noiseHandle.val
        self.noise = np.random.normal(0,self.deviation,self.N)
        self.axleft = plt.axes([0.4,0.28,0.15,0.05])
        self.leftHandle = widgets.Slider(self.axleft,'Left cut',0,1,valinit = 0)
        self.t0 = self.leftHandle.val
        self.axright = plt.axes([0.65,0.28,0.15,0.05])
        self.rightHandle = widgets.Slider(self.axright,'Right cut',0,1,valinit = self.t)
        self.t1 = self.rightHandle.val
        self.shape = "Sine"
        self.status = "On"
        self.max = 0
        self.max_pos = 0
        self.leftcut = self.ax1.plot([self.t0,self.t0],[-1,1],'r--')
        self.rightcut = self.ax1.plot([self.t1,self.t1],[-1,1],'r--')
        self.sigsin = np.sin(2*np.pi*self.f*self.time + self.p_shift)
        self.sigsaw = signal.sawtooth(2*np.pi*self.f*self.time + self.p_shift)
        self.sigsq = signal.square(2*np.pi*self.f*self.time + self.p_shift)
        self.sig = self.sigsin
        self.Fourier = fft(self.sig)
        self.f_array = np.linspace(1/self.t,int(self.N//2)/self.t,int(self.N//2))
        self.pow_spec = self.Fourier*np.conj(self.Fourier)/self.N
        self.max = np.where(self.pow_spec == np.amax(self.pow_spec))
        self.max_pos = self.max[0]
        self.f_max = self.f_array[self.max_pos[0]]
        self.f_diff = self.f_max-self.f
        self.f_array_correct = self.f_array - self.f_diff
        self.ax1.set_xlim([0,self.t])
        self.ax2.set_xlim(0,2*self.f_array_correct[int(self.max_pos[0])])
        self.sigplot = self.ax1.plot(self.time,self.sig)
        self.fplot = self.ax2.plot(self.f_array_correct,self.pow_spec[0:int(self.N//2)])


    def update(self):
        """Each widget change function then calls this function to update the 
        calculations and plots."""

        self.ax1.cla()
        self.ax1.set_xlim([0,self.t])
        """This if statement chooses the shape of the signal based on the 
        radiobutton selection."""
        if self.shape == 'Sine':
            self.sig = np.sin(2*np.pi*self.f*self.time + self.p_shift) + self.noise
        elif self.shape == 'Sawtooth':
            self.sig = signal.sawtooth(2*np.pi*self.f*self.time + self.p_shift) + self.noise
        elif self.shape == 'Square':
            self.sig = signal.square(2*np.pi*self.f*self.time + self.p_shift) + self.noise
        self.sigplot = self.ax1.plot(self.time[(self.time>self.t0) & (self.time<self.t1)],self.sig[(self.time>self.t0) & (self.time<self.t1)])
        self.leftcut = self.ax1.plot([self.t0,self.t0],[-1,1],'r--')
        self.rightcut = self.ax1.plot([self.t1,self.t1],[-1,1],'r--')
        self.ax2.cla()
        self.Fourier = fft(self.sig)
        self.f_array = np.linspace(1/(self.t1-self.t0),int(self.N//2)/(self.t1-self.t0),int(self.N//2))
        """The new sigplot will only be plotted for time values that are within 
        the window made by the left and right cuts."""
        self.pow_spec = self.Fourier*np.conj(self.Fourier)/self.N
        self.max = np.where(self.pow_spec == np.amax(self.pow_spec))
        self.max_pos = self.max[0]
        self.f_max = self.f_array[self.max_pos[0]]
        self.f_diff = self.f_max-self.f
        self.f_array_correct = self.f_array - self.f_diff
        self.ax2.set_xlim(self.f_array_correct[self.max_pos[0]]-30,self.f_array_correct[self.max_pos[0]]+30)
        """Adjusting the x-axis limit means that the peak of the Fourier
        transform is plotted in the middle of the plot no matter how it 
        changes."""
        self.fplot = self.ax2.plot(self.f_array_correct,self.pow_spec[0:self.N//2])


    def timeslide(self,val):
        self.t = self.timeHandle.val
        self.time = np.linspace(0,self.t,self.N)
        self.update()


    def freqslide(self,val):
        self.f = self.freqHandle.val
        self.update()


    def pointslide(self,val):
        self.N = int(self.pointHandle.val)
        self.time = np.linspace(self.t0,self.t1,self.N)
        self.noise = np.random.normal(0,self.deviation,self.N)
        """Time and noise needed updating in this callback because they are 
        dependent on N."""
        self.update()


    def phaseslide(self,val):
        self.p_shift = self.phaseHandle.val
        self.update()


    def leftslide(self,val):
        if self.leftHandle.val < self.rightHandle.val:
            self.t0 = self.leftHandle.val*self.t
        else:
            self.t1 = self.leftHandle.val*self.t
            self.t0 = self.rightHandle.val*self.t
        """The if statement takes into account if the left cut slider has a 
        higher value than the right cut slider so the same amount of signal is 
        displayed as if their slider values were switched."""
        self.time = np.linspace(self.t0,self.t1,self.N)
        self.update()


    def rightslide(self,val):
        if self.rightHandle.val > self.leftHandle.val:
            self.t1 = self.rightHandle.val*self.t
        else:
            self.t0 = self.rightHandle.val*self.t
            self.t1 = self.leftHandle.val*self.t
        self.time = np.linspace(self.t0,self.t1,self.N)
        self.update()


    def noiseslide(self,val):
        self.deviation = self.noiseHandle.val
        self.noise = np.random.normal(0,self.deviation,self.N)
        """This callback updates the amount of noise added to the signal which
        is generated using a normal distribution of N points with a mean of 0
        and a standard deviation equal to the value of the noise slider."""
        self.update()


    def shapebut(self,label):
        self.shape = label
        self.update()


if __name__ == "__main__":

    oscope = oscope_class()
    oscope.timeHandle.on_changed(oscope.timeslide)
    oscope.freqHandle.on_changed(oscope.freqslide)
    oscope.pointHandle.on_changed(oscope.pointslide)
    oscope.phaseHandle.on_changed(oscope.phaseslide)
    oscope.leftHandle.on_changed(oscope.leftslide)
    oscope.rightHandle.on_changed(oscope.rightslide)
    oscope.noiseHandle.on_changed(oscope.noiseslide)
    oscope.shapeHandle.on_clicked(oscope.shapebut)

    while oscope.powerHandle.value_selected == 'On':

        plt.pause(0.01)

    plt.close('all')
    sys.exit()
    """I didn't need a callback function for the power button I just needed it
    to not be "on" for the programme to switch off."""










