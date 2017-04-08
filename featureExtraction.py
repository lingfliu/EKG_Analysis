import wave # this is the wave.py file in the local folder
import matplotlib.pyplot as plt
import pywt
# np.set_printoptions(threshold=np.nan) # show full arrays, dataframes, etc. when printing
import warnings
warnings.simplefilter("error") # Show warning traceback

class Signal(object):
    """
    An ECG/EKG signal

    Attributes:
        name: A string representing the record name.
        data : 1-dimensional array with input signal data 
    """

    def __init__(self, name, data):
        """Return a Signal object whose record name is *name*,
        signal data is *data*,
        R peaks array of coordinates [(x1,y1), (x2, y2),..., (xn, yn)]  is *RPeaks*"""
        self.name = name
        self.data = data
        self.sampleFreq = 1/300
        
        RPeaks = wave.getRPeaks(self.data, 150)
        self.RPeaks = RPeaks[1]
        self.inverted = RPeaks[0]
        if self.inverted: # flip the inverted signal
            self.data = -data
        
        Pwaves = wave.getPWaves(self)
        self.PPintervals = Pwaves[0] * self.sampleFreq
        self.Ppeaks = Pwaves[1]
        
        self.baseline = wave.getBaseline(self)
        
        self.QSPoints = wave.getQS(self)
        
        #RR interval
        self.RRintervals = wave.wave_intervals(self.RPeaks)
        
        baseline = wave.getBaseline(self)
        self.baseline = baseline[0]
        self.RRIntervalMeanStd = baseline[1] # Standard deviation of all RR interval means
            
    def plotRPeaks(self):
        fig = plt.figure(figsize=(9.7, 6)) # I used figures to customize size
        ax = fig.add_subplot(111)
        ax.plot(self.data)
        # ax.axhline(self.baseline)
        ax.plot(*zip(*self.RPeaks), marker='o', color='r', ls='')
        ax.set_title(self.name)
        plt.show()
        
        
    # TODO: add error handling for crazy cases of data i.e. A04244, A00057
    # Wrap the whole thing in a try catch, assign as AF if there's an error
    # Set everything to N in the beginning
    
    # TODO: Write bash script including pip install for pywavelets

records = wave.getRecords('~') # N O A ~

for i in records:
    data = wave.load(i)
    print ('working on Record:' + i)
    sig = Signal(i,data)

# Imperatively grabbing features
#data = wave.load('A00057')
#signal = Signal('A00057', data)
#signal.plotRPeaks()


records = wave.getRecords('N') # N O A ~
data = wave.load(records[7])
sig = Signal(records[7],data)

#sig.plotRPeaks()
#
#wave.getQS(sig)

#RR interval stuff
#error_list = []
#for i in records:



        

#records = wave.getRecords('A') # N O A ~
#data = wave.load(records[7])
#sig = Signal(records[7],data)




