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
        elif instantaenous_HR_Pleth > 240: # detects for Bradycardia where heart rate is above 240 bpm
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
        else:
            return all_HR_Pleth
        k+=1        

    
def estimate_heart_rate_oneminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate one minute average heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: one minute average heart rate
    """
    one_minute_HR_Pleth = []
    total_one_minute_HR_pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        time_between_beats_Pleth = (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k]) / PlethSampFreqHz
        one_minute_HR_Pleth.append(time_between_beats_Pleth)
        one_minute_HR_sum_Pleth = sum(one_minute_HR_Pleth)
        if one_minute_HR_sum_Pleth > 60:
            one_minute_total_HR_Pleth =  len(one_minute_HR_Pleth)
            total_one_minute_HR_pleth.append(one_minute_total_HR_Pleth)
            one_minute_HR_Pleth = []
            return total_one_minute_HR_pleth
        k+=1
    

def estimate_heart_rate_fiveminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate five minute average heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: five minute average heart rate
    """

    five_minute_HR_Pleth = []
    total_five_minute_HR_pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        time_between_beats_Pleth = (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k]) / PlethSampFreqHz
        five_minute_HR_Pleth.append(time_between_beats_Pleth)
        five_minute_HR_sum_Pleth = sum(five_minute_HR_Pleth)
        if five_minute_HR_sum_Pleth > 300:
            five_minute_total_HR_Pleth =  len(five_minute_HR_Pleth) / 5
            total_five_minute_HR_pleth.append(five_minute_total_HR_Pleth)
            five_minute_HR_Pleth = []
            return total_five_minute_HR_pleth
        k+=1

  