def read_data(filename = "test.bin"):
    """ read in raw data from binary file

    :param filename: filename = "test.bin"
    :returns: ECG Sampling Frequency, Pulse Plethysmograph Sampling Frequency, ECG sampling values array, Pulse Plethysmograph Sampling values array """ 
    import numpy as np
    data = np.fromfile(filename, dtype = 'uint16')

    ECGData = np.array(data[::2])
    PlethData = np.array(data[1::2])
    
    ECGSampFreqHz = ECGData[0]
    PlethSampFreqHz = PlethData[0]
    
    return ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData
   # return {'ECG_SampFreq':ECGSampFreqHz, 'Pleth_SampFreq':PlethSampFreqHz, 'ECG_Data':ECGData, 'Pleth_Data':PlethData}    


def test_read_data():
    """ read in raw data from binary file

    :param filename: filename = "test.bin"
    :returns: """    
    read_data()
    import numpy as np
    
    assert read_data() == (770, 1284, [770], [1284])



with open('test.bin', 'rb') as filename:
    import numpy as np
    data = np.fromfile(filename, dtype = 'uint16')
    print(data)

    ECGData = np.array(data[::2])
    PlethData = np.array(data[1::2])
    print(ECGData)
    print(PlethData)
    
    ECGSampFreqHz = ECGData[0]
    PlethSampFreqHz = PlethData[0]
    print(ECGSampFreqHz)
    print(PlethSampFreqHz)


def heart_rate_indicies():
    """ estimate instantaneous heart rate
    
    :param signal: input signal from read_data()
    :returns: instantenous heart rate from 5 second interval
    """
    read_data()

    instantaneous_HR_indicies = [] # Array which holds temporary values of heart rates as data is read
    i=0
    while i < ECGData.size:
        if ECGData[i] > np.median(ECGData[(i-2-int(ECGSampFreqHz/16)):(i+5-int(ECGSampFreqHz/16))]) and ECGData[i] > np.median(ECGData[(i-2+int(ECGSampFreqHz/16)):(i+5+int(ECGSampFreqHz/16))]):
            instantaneous_HR_indicies.append(i)
        i+=1
    
    return instantaneous_HR_indicies


def estimate_instantaneous_HR():
    """ estimate instantaneous heart rate

    :param signal: input signal from read_data() and input peak index values from heart_rate_indicies()
    :returns: one minute average heart rate
    """
    read_data()
    heart_rate_indicies()
    
    all_HR = []
    k = 0
    while k < len(instantaneous_HR_indicies):
        instantaenous_HR = ((60 * ECGSampFreqHz) / (instantaneous_HR_indicies[k+1] - instantaneous_HR_indicies[k])) # calculates instantaenous HR for each beat
        all_HR.append(instantaenous_HR)
        return instantaenous_HR
        if instantaenous_HR < 30: # detects for Bradycardia where heart rate is below 30 bpm
            print("Bradycardia alert! Here is 10 minute trace of heart rate:")
            invertedHR = np.array(all_HR[::-1])
            invertedHRseconds = 1 / (invertedHR / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum = HR_sum + invertedHRseconds[x]
                if HR_sum > 600:
                    ten_min_invert = invertedHR[0:x]
                    ten_min_real = ten_min_invert[::-1]
                    print(ten_min_real)
                    break
        if instantaenous_HR > 240: # detects for Bradycardia where heart rate is above 240 bpm
            print("Tachycardia alert! Here is 10 minute trace of heart rate:")
            invertedHR = np.array(all_HR[::-1])
            invertedHRseconds = 1 / (invertedHR / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum = HR_sum + invertedHRseconds[x]
                if HR_sum > 600:
                    ten_min_invert = invertedHR[0:x]
                    ten_min_real = ten_min_invert[::-1]
                    print(ten_min_real)
                    break
        k+=1
    

def estimate_heart_rate_oneminute():
    """ estimate one minute average heart rate

    :param signal: input signal from read_data()
    :returns: one minute average heart rate
    """
    read_data()

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
    read_data()
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



def test_instantaneous_HR():
    read_data()

    import numpy as np
    Fs = 20
    sample = 5000
    f = 3
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))

    instantaneous_HR_indicies = [] # Array which holds temporary values of heart rates as data is read
    i=0
    while i < y.size:
        if y[i] > np.median(y[(i-2-int(Fs/16)):(i+5-int(Fs/16))]) and y[i] > np.median(y[(i-2+int(Fs/16)):(i+5+int(Fs/16))]):
            instantaneous_HR_indicies.append(i)
            #print(y[i])
        i+=1

    #print(instantaneous_HR_indicies)
    all_HR = []
    k = 0
    while k < len(instantaneous_HR_indicies):
        instantaenous_HR = ((60 * Fs) / (instantaneous_HR_indicies[k+1] - instantaneous_HR_indicies[k])) # calculates instantaenous HR for each beat
        all_HR.append(instantaenous_HR)
        #print(instantaenous_HR)
        if instantaenous_HR < 30: # detects for Bradycardia where heart rate is below 30 bpm
            print("Bradycardia alert! Here is 10 minute trace of heart rate:")
            invertedHR = np.array(all_HR[::-1])
            invertedHRseconds = 1 / (invertedHR / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum = HR_sum + invertedHRseconds[x]
                if HR_sum > 600:
                    ten_min_invert = invertedHR[0:x]
                    ten_min_real = ten_min_invert[::-1]
                    print(ten_min_real)
                    break
        if instantaenous_HR > 240: # detects for Bradycardia where heart rate is above 240 bpm
            #print("Tachycardia alert! Here is 10 minute trace of heart rate:")
            invertedHR = np.array(all_HR[::-1])
            invertedHRseconds = 1 / (invertedHR / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum = HR_sum + invertedHRseconds[x]
                if HR_sum > 600:
                    ten_min_invert = invertedHR[0:x]
                    ten_min_real = ten_min_invert[::-1]
                    print(ten_min_real)
                    break
        k+=1

#test_instantaneous_HR()


def test_estimate_heart_rate():
    read_data()    
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


    instantaneous_HR_temp = [] # Array which holds temporary values of heart rates as data is read
    instantaenous_HR_TenMin = []
    i=0
    while i < y.size-1:
        if y[i] > y[i-1] and y[i] > y[i+1]:
            instantaneous_HR_temp.append(y[i])
        if i % (2 * Fs) == 0: # Identifies everytime 2 seconds of data has passed
            instantaneous_HR_array = np.array(instantaneous_HR_temp)
            instantaenous_HR = instantaneous_HR_array.size * 30
            instantaenous_HR_TenMin.append(instantaenous_HR)
            print(instantaenous_HR)
            if instantaenous_HR < 30:
                print("Bradycardia alert!")
            if instantaenous_HR > 240:
                print("Tachycardia alert!")
        #if i > (600 * ECGSampFreqHz):
            #instantaenous_HR_TenMin = instantaenous_HR_TenMin[1:len(instantaenous_HR_TenMin)]
        i+=1 


#test_estimate_heart_rate()

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

