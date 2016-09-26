def read_data(filename):
    """ read in raw data from binary file inputted by user

    :param filename: filename = ""
    :returns: ECG Sampling Frequency, Pulse Plethysmograph Sampling Frequency, ECG sampling values array, Pulse Plethysmograph sampling values array """ 
    import numpy as np

    data = np.fromfile(filename, dtype = 'uint16')


    ECGAllData = np.array(data[0::2])
    PlethAllData = np.array(data[1::2])
    
    ECGSampFreqHz = ECGAllData[0]
    PlethSampFreqHz = PlethAllData[0]
    
    ECGData = np.array(data[2::2])
    PlethData = np.array(data[3::2])

    return ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData   


def heart_rate_indicies_ECG(ECGData):
    """ estimate indicies of ECG peaks
    
    :param signal: ECG sampling values array from read_data()
    :returns: indicies of peaks in ECG sampling values array
    """

    instantaneous_HR_indicies_ECG = [] # Array which holds temporary values of heart rates as data is read
    i=1
    while i < ECGData.size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            instantaneous_HR_indicies_ECG.append(i)
        i+=1
    
    return instantaneous_HR_indicies_ECG

def heart_rate_indicies_Plethysmograph(PlethData):
    """ estimate indicies of Plethysmograph peaks
    
    :param signal: Plethysmograph sampling values array from read_data()
    :returns: indicies of peaks in Plethysmograph sampling values array
    """

    instantaneous_HR_indicies_Pleth = [] # Array which holds temporary values of heart rates as data is read
    i=1
    while i < PlethData.size-1:
        if PlethData[i] > PlethData[i-1] and PlethData[i] > PlethData[i+1]:
            instantaneous_HR_indicies_Pleth.append(i)
        i+=1
    
    return instantaneous_HR_indicies_Pleth


def estimate_instantaneous_HR(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate instantaneous heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: instantaneous HR, alert, and 10 minute log of instantaneous heart rate
    """
    import numpy as np

    all_HR_Pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        instantaenous_HR_Pleth = ((60 * PlethSampFreqHz) / (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k])) # calculates instantaenous HR for each beat
        all_HR_Pleth.append(instantaenous_HR_Pleth)
        if instantaenous_HR_Pleth < 30: # detects for Bradycardia where heart rate is below 30 bpm
            invertedHR_Pleth = np.array(all_HR_Pleth[::-1])
            invertedHRseconds_Pleth = 1 / (invertedHR_Pleth / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum_Pleth = HR_sum_Pleth + invertedHRseconds_Pleth[x]
                ten_min_invert_Pleth = invertedHR_Pleth[0:x]
                ten_min_real_Pleth = np.array(ten_min_invert_Pleth[::-1])
                if np.sum(ten_min_real_Pleth) > 600:
                    print("Bradycardia alert! Here is 10 minute trace of heart rate:")
                    return ten_min_real_Pleth
                    break
        if instantaenous_HR_Pleth > 240: # detects for Bradycardia where heart rate is above 240 bpm
            invertedHR_Pleth = np.array(all_HR_Pleth[::-1])
            invertedHRseconds_Pleth = 1 / (invertedHR_Pleth / 60)
            HR_sum_Pleth = 0
            for x in range(0, k):
                HR_sum_Pleth = HR_sum_Pleth + invertedHRseconds_Pleth[x]
                ten_min_invert_Pleth = invertedHR_Pleth[0:x]
                ten_min_real_Pleth = np.array(ten_min_invert_Pleth[::-1])
                if np.sum(ten_min_real_Pleth) > 600:
                    print("Tachycardia alert! Here is 10 minute trace of heart rate:")
                    return ten_min_real_Pleth
                    break
        return instantaenous_HR_Pleth
        k+=1        

    
def estimate_heart_rate_oneminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate one minute average heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: one minute average heart rate
    """
    one_minute_HR_Pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        time_between_beats_Pleth = (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k]) / PlethSampFreqHz
        one_minute_HR_Pleth.append(time_between_beats_Pleth)
        one_minute_HR_sum_Pleth = sum(one_minute_HR_Pleth)
        if one_minute_HR_sum_Pleth > 60:
            one_minute_total_HR_Pleth =  len(one_minute_HR_Pleth)
            one_minute_HR_Pleth = []
            return one_minute_total_HR_Pleth
        k+=1
    

def estimate_heart_rate_fiveminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate five minute average heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: five minute average heart rate
    """

    five_minute_HR_Pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        time_between_beats_Pleth = (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k]) / PlethSampFreqHz
        five_minute_HR_Pleth.append(time_between_beats_Pleth)
        five_minute_HR_sum_Pleth = sum(five_minute_HR_Pleth)
        if five_minute_HR_sum_Pleth > 300:
            five_minute_total_HR_Pleth =  len(five_minute_HR_Pleth) / 5
            five_minute_HR_Pleth = []
            return five_minute_total_HR_Pleth
        k+=1


def test_instantaneous_HR():

    import numpy as np
    Fs = 8000
    sample = 8000
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))
    a = 0

    instantaneous_HR_indicies = [] # Array which holds temporary values of heart rates as data is read
    i=6
    while i < y.size-6:
        #if y[i] > np.mean(y[i-1:i-5]) and y[i] > np.mean(y[i+1:i+5]):
        if y[i] > y[i-1] and y[i] > y[i+1]:
            instantaneous_HR_indicies.append(i)
            #print(y[i])
        i+=1
    # assert instantaneous_HR_indicies == [1, 1, 1, 1, 1]


    one_minute_HR = []
    k = 0
    while k < len(instantaneous_HR_indicies)-1:
        time_between_beats = (instantaneous_HR_indicies[k+1] - instantaneous_HR_indicies[k]) / Fs
        one_minute_HR.append(time_between_beats)
        one_minute_HR_sum = sum(one_minute_HR)
        if one_minute_HR_sum > 300:
            one_minute_total_HR = len(one_minute_HR) / 5
            one_minute_HR = []
            print(one_minute_total_HR)
        k+=1

    #print(instantaneous_HR_indicies)
    all_HR = []
    k = 0
    while k < len(instantaneous_HR_indicies)-1:
        instantaenous_HR = ((60 * Fs) / (instantaneous_HR_indicies[k+1] - instantaneous_HR_indicies[k])) # calculates instantaenous HR for each beat
        all_HR.append(instantaenous_HR)
        print(instantaenous_HR)
        if instantaenous_HR < 30: # detects for Bradycardia where heart rate is below 30 bpm
            #print("Bradycardia alert! Here is 10 minute trace of heart rate:")
            invertedHR = np.array(all_HR[::-1])
            invertedHRseconds = 1 / (invertedHR / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum = HR_sum + invertedHRseconds[x]
                ten_min_invert = invertedHR[0:x]
                ten_min_real = np.array(ten_min_invert[::-1])
                if np.sum(ten_min_real) > 600:
                    print(ten_min_real)
                    break
        if instantaenous_HR > 240: # detects for Bradycardia where heart rate is above 240 bpm
            #print("Tachycardia alert! Here is 10 minute trace of heart rate:")
            invertedHR = np.array(all_HR[::-1])
            invertedHRseconds = 1 / (invertedHR / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum = HR_sum + invertedHRseconds[x]
                ten_min_invert = invertedHR[0:x]
                ten_min_real = np.array(ten_min_invert[::-1])
                if np.sum(ten_min_real) > 600:
                    print(ten_min_real)
                    break
        k+=1

test_instantaneous_HR()


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

    # maxvalues_one = []
    # maxvalues_one_array = []
    # i = 0
    # while i < y.size-1:
    #     if y[i] > y[i-1] and y[i] > y[i+1]:
    #         maxvalues_one.append(y[i])
    #     if i%(60*Fs) == 0:
    #         maxvaluesarray_one = np.array(maxvalues_one)
    #         maxvalues_one_array.append(maxvaluesarray_one.size)
    #         #print(one_min_avg)
    #         #return one_min_avg
    #         maxvalues_one = []

    #     i+=1

    # maxvalues_five = []
    # maxvalues_five_array = []
    # i = 0
    # while i < y.size-1:
    #     if y[i] > y[i-1] and y[i] > y[i+1]:
    #         maxvalues_five.append(y[i])
    #     if i%(300*Fs) == 0:
    #         maxvaluesarray_five = np.array(maxvalues_five)
    #         maxvalues_five_array.append(maxvaluesarray_five.size / 5)
    #         #print(five_min_avg)
    #         #return five_min_avg
    #         maxvalues_five = []

    #     i+=1
    
    # print(maxvalues_one_array)


    # instantaneous_HR_temp = [] # Array which holds temporary values of heart rates as data is read
    # instantaenous_HR_TenMin = []
    # i=0
    # while i < y.size-1:
    #     if y[i] > y[i-1] and y[i] > y[i+1]:
    #         instantaneous_HR_temp.append(y[i])
    #     if i % (2 * Fs) == 0: # Identifies everytime 2 seconds of data has passed
    #         instantaneous_HR_array = np.array(instantaneous_HR_temp)
    #         instantaenous_HR = instantaneous_HR_array.size * 30
    #         instantaenous_HR_TenMin.append(instantaenous_HR)
    #         print(instantaenous_HR)
    #         if instantaenous_HR < 30:
    #             print("Bradycardia alert!")
    #         if instantaenous_HR > 240:
    #             print("Tachycardia alert!")
    #     #if i > (600 * ECGSampFreqHz):
    #         #instantaenous_HR_TenMin = instantaenous_HR_TenMin[1:len(instantaenous_HR_TenMin)]
    #     i+=1 


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

