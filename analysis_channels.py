import scipy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class STMTVAC():
    def __init__(self, files):
        self.files = files
        self.stelaheader = ['DateTime', 'P1', 'P2', 'SetTable', 'SetShield',
                            'InternalHuber1', 'InternalHuber2', 'InternalHuber3',
                            'TableAvg', 'ShieldAvg', 'AdditionalSens',
                            'TableTemp1', 'TableTemp2', 'TableTemp3', 'TableTemp4', 'TableTemp5',
                            'ShieldTemp1', 'ShieldTemp2', 'ShieldTemp3', 'ShieldTemp4', 'ShieldTemp5']
    
    def load_data(self, which = None):
            """
            Function to load STELA data, it is developed to be able to read and 
            concatinate n number of STELA files. The user just passes a list of the
            filenames in the correct order in STMTVAC()
            """
            if which == "thermusb":
                self.thermusb = pd.read_csv(self.files[0],
                                            sep = ' ',
                                            skiprows = 3,
                                            skipfooter = 1,
                                            index_col = False,
                                            engine = "python") 
 

    def slicedata(self, starttime, endtime):
        self.msk = (self.thermusb.iloc[:,0] >= starttime)&(self.thermusb.iloc[:,0] <= endtime)
        self.sliced = self.thermusb[self.msk]
        self.sliced.time = np.linspace(1, endtime-starttime, len(self.sliced.iloc[:,0]))

    def plotdt(self, channels, figname):
        startvalue = [self.sliced.iloc[0][ch] for ch in channels]
        (fig, ax) = plt.subplots(1)
        for idx, ch in enumerate(channels):
            ax.plot(self.sliced.iloc[:,0],
                    self.sliced[ch] - startvalue[idx],
                    label = ch)
        ax.set_title("Biased")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(r"$\Delta T^{\circ}C$")
        ax.legend(loc = "upper right")
        fig.tight_layout()
        fig.savefig(figname)


        
        

channels = ["dev1ch0", "dev1ch1",
            "dev1ch2", "dev1ch4", "dev1ch6"]

therm = STMTVAC(["therm_delta_table/tmp_sens_data.txt"])
therm.load_data(which = "thermusb")
therm.slicedata(starttime = 120, endtime =17000)
therm.plotdt(channels = channels, figname= "full_biased.pdf")

"""
(fig, ax) = plt.subplots(1)
for idx,ch in enumerate(channels):
    ax.plot(therm.sliced.time,
            therm.sliced[ch] - startvalue[idx], label = ch)
ax.set_title('Biased ')
ax.set_ylabel(r'$\Delta T$')
ax.set_xlabel(r'Time')
ax.legend(loc = "best") 
fig.savefig("biased.pdf")
"""