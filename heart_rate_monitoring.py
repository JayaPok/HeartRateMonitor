def read_data(filename = "test.bin"):
    """ read in raw data from binary file

    :param filename: default = ""
    :returns: """ 
    import numpy as np
    Freqs = np.fromfile(filename, dtype = 'uint16')

    ECGData = np.array(Freqs[::2])
    PlethData = np.array(Freqs[1::2])
    
    ECGSampFreqHz = ECGData[0]
    PlethSampFreqHz = PlethData[0]

    return {'ECG_SampFreq':ECGSampFreqHz, 'Pleth_SampFreq':PlethSampFreqHz, 'ECG_Data':ECGData, 'Pleth_Data':PlethData}


with open('test.bin', 'rb') as filename:
    import numpy as np
    Freqs = np.fromfile(filename, dtype = 'uint16')
    print(Freqs)

    ECGData = np.array(Freqs[::2])
    PlethData = np.array(Freqs[1::2])
    print(ECGData)
    print(PlethData)
    
    ECGSampFreqHz = ECGData[0]
    PlethSampFreqHz = PlethData[0]
    print(ECGSampFreqHz)
    print(PlethSampFreqHz)
    

def estimate_heart_rate_oneminute():
    """ estimate one minute average heart rate

    :param signal: input signal from read_data()
    :returns: one minute average heart rate
    """

    ECG_avg_HR_onemin = []
    one_min_avg_array = []
    i = 0
    while i < ECGData[1:].size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            ECG_avg_HR_onemin.append(ECGData[i])
        if i % (60 * ECGSampFreqHz):
            array_ECG_avg_HR_onemin = np.array(ECG_avg_HR_onemin)
            one_min_avg_array.append(array_ECG_avg_HR_onemin.size)
            ECG_avg_HR_onemin = []
        i+=1
    return one_min_avg_array


def estimate_heart_rate_fiveminute():
    """ estimate five minute average heart rate

    :param signal: input signal from read_data()
    :returns: five minute average heart rate
    """

    ECG_avg_HR_fivemin = []
    five_min_avg_array = []
    i = 0
    while i < ECGData[1:].size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            ECG_avg_HR_fivemin.append(ECGData[i])
        if i % (300 * ECGSampFreqHz):
            array_ECG_avg_HR_fivemin = np.array(ECG_avg_HR_fivemin)
            five_min_avg.append(array_ECG_avg_HR_fivemin.size / 5)
            ECG_avg_HR_fivemin = []
        i+=1
    return five_min_avg_array



def test_estimate_heart_rate():
    import numpy as np
    import matplotlib.pyplot as plt

    #read_data()

    Fs = 20
    sample = 100000
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))
    #print(y)

    inst_samples = 5*Fs
   
    #plt.plot(x/Fs,y)
    #plt.show()

    maxvalues_one = []
    i = 0
    while i < y.size-1:
        if y[i] > y[i-1] and y[i] > y[i+1]:
            maxvalues_one.append(y[i])
        if i%(60*Fs) == 0:
            maxvaluesarray_one = np.array(maxvalues_one)
            one_min_avg = maxvaluesarray_one.size
            #print(one_min_avg)
            #return one_min_avg
            maxvalues_one = []

        i+=1

    maxvalues_five = []
    maxvalues_five_array = []
    i = 0
    while i < y.size-1:
        if y[i] > y[i-1] and y[i] > y[i+1]:
            maxvalues_five.append(y[i])
        if i%(300*Fs) == 0:
            maxvaluesarray_five = np.array(maxvalues_five)
            maxvalues_five_array.append(maxvaluesarray_five.size / 5)
            #print(five_min_avg)
            #return five_min_avg
            maxvalues_five = []

        i+=1
    
    print(maxvalues_five_array)

test_estimate_heart_rate()

def output_instaneous_heart_rate(signal):
    """ output estimate instanteous heart rate

    :param signal: input signal from read_data()
    :returns: instanteous heart rate
    """

def output_avg_heart_rate():
    """ output estimate 1 and 5 min average heart rate

    :param signal: input signal from read_data()
    :returns: 1 and 5 min average heart rate
    """
def avg_heart_rate():
    """ estimate 1 and 5 min average heart rate

    :param signal: input signal from read_data()
    :returns: 1 and 5 min average heart rate
    """

