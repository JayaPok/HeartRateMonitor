import numpy as np
import collections

def read_data(filename, SampFreq, iteration):
    """ read in raw data from binary file inputted by user

    :param: binary file, sampling frequency, and iteration number of loop in main method
    :returns: ten second data of binary file based on iteration """ 
    import numpy as np
    
    f = open(filename, "rb")
    f.seek(2*(10*iteration))
    tensec_data = []
    i = 0

    while(i < 20):
        data = f.read(2)
        tensec_data.append(int.from_bytes(data, byteorder = 'little'))
        f.seek(0, 1)
        i+=1
    
    return tensec_data


def find_sampfreq(filename):
    """ find sampling frequency from the first values of the binary file

    :param: binary file
    :returns: ECG and Pulse sampling frequency  """ 
    f = open(filename, "rb")
    SampFreqPulse = f.read(2)
    SampFreqECG = f.read(2)
    
    SampFreq = int.from_bytes(SampFreqPulse, byteorder = 'little')

    return SampFreq


def obtain_ECG(tensec_data):
    """ obtain ECG values of ten second data

    :param: multiplexed ECG and Pleth data
    :returns: ECG data  """
    ECGData= np.array(tensec_data[1::2])

    return ECGData

def obtain_Pleth(tensec_data):
    """ obtain Pulse Pleth values of ten second data

    :param: multiplexed ECG and Pleth data
    :returns: Pleth data  """
    PlethData = np.array(tensec_data[0::2])

    return PlethData


def heart_rate_ECG_insta(ECGData):
    """ estimate number of peaks in 10 second ECG data
    
    :param signal: 10 second ECG data
    :returns: 10 second ECG heart rate
    """

    instantaneous_HR_indicies_ECG = [] # Array which holds temporary values of heart rates as data is read
    i=1
    while i < ECGData.size-1:
        if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
            instantaneous_HR_indicies_ECG.append(i)
        i+=1
    
    ten_sec_info_ECG = len(instantaneous_HR_indicies_ECG)
   
    return ten_sec_info_ECG


def heart_rate_Pleth_insta(PlethData):
    """ estimate number of peaks in 10 second Pleth data
    
    :param signal: 10 second Pleth data
    :returns: 10 second Pleth heart rate
    """

    instantaneous_HR_indicies_Pleth = [] # Array which holds temporary values of heart rates as data is read
    i=1
    while i < PlethData.size-1:
        if PlethData[i] > PlethData[i-1] and PlethData[i] > PlethData[i+1]:
            instantaneous_HR_indicies_Pleth.append(i)
        i+=1

    ten_sec_info_Pleth = len(instantaneous_HR_indicies_Pleth)
    
    return ten_sec_info_Pleth

def estimate_instantaneous_HR(ten_sec_info_avg):
    """ estimate 10 second instantaneous heart rate

    :param signal: 10 second average of ECG and Pulse HR data
    :returns: instantaneous averaged heart rate
    """
    import numpy as np

    instantaneous_HR = ten_sec_info_avg * 6

    return instantaneous_HR

def alert_brady(tenmin_log):
    """ bradycardia alert

    :param signal: ten minute heart rate back log
    :returns: ten minute heart rate back log
    """
    
    tenmin_log_brady = list(tenmin_log)

    return tenmin_log_brady

def alert_tachy(tenmin_log):
    """ tachycardia alert

    :param signal: ten minute heart rate back log
    :returns: ten minute heart rate back log
    """
    
    tenmin_log_tachy = list(tenmin_log)

    return tenmin_log_tachy

def some_min_avg(somemin_avg_log):
    """ some minute average heart rate calculation

    :param signal: some minute heart rate back log
    :returns: some minute heart rate
    """
    
    somemin_avg = sum(somemin_avg_log) / len(somemin_avg_log)

    return somemin_avg




    
