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


def estimate_instantaenous_heart_rate():
    """ estimate instantaneous heart rate
    
    :param signal: input signal from read_data()
    :returns: instantenous heart rate from 5 second interval
    """

    instantaneous_HR_temp = [] # Array which holds temporary values of heart rates as data is read
    i=0
    while i < y.size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            instantaneous_HR_temp.append(ECGData[i])
        if i % ECGSampFreqHz == 0: # Identifies everytime 1 second of data has passed
            instantaneous_HR_array = np.array(instantaneous_HR_temp)
            instantaenous_HR = instantaneous_HR_array.size * 20
            print(instantaenous_HR)
            if instantaenous_HR < 30:
                print("Bradycardia alert!")
            if instantaenous_HR > 240:
                print("Tachycardia alert!")
            instantaneous_HR_temp = instantaneous_HR_temp[1:5] #Shifts array by one to get a rolling five second average heart rate shifting each second
        i+=1    
    

def estimate_heart_rate_oneminute():
    """ estimate one minute average heart rate

    :param signal: input signal from read_data()
    :returns: one minute average heart rate
    """

    ECG_avg_HR_onemin = []  # Array which will hold value of each local maxima ECG values for a 60 second period
    one_min_avg_array = []  # Array which counts incidents in ECG_avg_HR_onemin array to be returned as one minute heart rate estimate
    i = 0
    while i < ECGData[1:].size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            ECG_avg_HR_onemin.append(ECGData[i])
        if i % (60 * ECGSampFreqHz) == 0: # Identifiying everytime 1 minute of data has passed
            array_ECG_avg_HR_onemin = np.array(ECG_avg_HR_onemin)
            one_min_avg_array.append(array_ECG_avg_HR_onemin.size) # Adds heart rate during 60 seconds to cumulative one minute heart rate array
            ECG_avg_HR_onemin = [] # Resets 60 second array
        i+=1
    return one_min_avg_array


def estimate_heart_rate_fiveminute():
    """ estimate five minute average heart rate

    :param signal: input signal from read_data()
    :returns: five minute average heart rate
    """

    ECG_avg_HR_fivemin = [] # Array which will hold value of each local maxima ECG values for a 300 second period
    five_min_avg_array = [] # Array which counts incidents in ECG_avg_HR_fivemin array to be returned as five minute heart rate estimate
    i = 0
    while i < ECGData[1:].size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            ECG_avg_HR_fivemin.append(ECGData[i])
        if i % (300 * ECGSampFreqHz) == 0:  # Identifiying everytime 5 minutess of data has passed
            array_ECG_avg_HR_fivemin = np.array(ECG_avg_HR_fivemin)
            five_min_avg.append(array_ECG_avg_HR_fivemin.size / 5) # Adds average heart rate during 300 seconds to cumulative five minute heart rate array
            ECG_avg_HR_fivemin = [] # Resets 300 second array 
        i+=1
    return five_min_avg_array



def test_estimate_heart_rate():
    import numpy as np
    import matplotlib.pyplot as plt

    Fs = 20
    sample = 5000
    f = 3
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))
    #print(y)

    inst_samples = 5*Fs
   
    #plt.plot(x/Fs,y)
    #plt.show()

    maxvalues_one = []
    maxvalues_one_array = []
    i = 0
    while i < y.size-1:
        if y[i] > y[i-1] and y[i] > y[i+1]:
            maxvalues_one.append(y[i])
        if i%(60*Fs) == 0:
            maxvaluesarray_one = np.array(maxvalues_one)
            maxvalues_one_array.append(maxvaluesarray_one.size)
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
    
    print(maxvalues_one_array)

    instantaneous_HR_temp = []
    i=0
    while i < y.size-1:
        if y[i] > y[i-1] and y[i] > y[i+1]:
            instantaneous_HR_temp.append(y[i])
        if i % Fs == 0:
            instantaneous_HR_array = np.array(instantaneous_HR_temp)
            instantaenous_HR = instantaneous_HR_array.size * 20
            #print(instantaenous_HR)
            if instantaenous_HR < 30:
                print("Bradycardia alert!")
            if instantaenous_HR > 240:
                print("Tachycardia alert!")
            instantaneous_HR_temp = instantaneous_HR_temp[1:5]
        i+=1

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

