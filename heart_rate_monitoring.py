import numpy as np
import collections
import logging

def parse_cli():
    """ argparse capabilites that enables user to input values to change output
    
    :param: user inputed values for one or more of filename, bradycardia threshold, tachycardia threshold, signal type, and desired minute HR average
    :returns: returns args arguments for main method() """ 
    import argparse as ap

    par = ap.ArgumentParser(description = "run program for inputted binary file", formatter_class = ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("--file", dest = "file", help="input binary file", type = str)
    par.add_argument("--brady", dest = "brady", help="input bradycardia starting heart rate", type = int, default = 30)
    par.add_argument("--tachy", dest = "tachy", help="input tachycardia starting heart rate", type = int, default = 240)
    par.add_argument("--signal", dest = "signal", help="input ECG for ECG signal HR estimation, PLETH for Plethysmograph HR estimation, \
     or BOTH for an average of both signals HR estimation", type = str, default = "BOTH")
    par.add_argument("--usermin", dest = "usermin", help="input desired multi-minute heart rate average", type = int, default = 2)

    args = par.parse_args()

    return args

def main_arg():
    """ run all functions of heart_rate_monitoring file
    
    :param: arg arguments from argparse
    :returns: user inputed variables to be inputed into code for specific responses """ 
    args = parse_cli()

    file = args.file
    brady = args.brady
    tachy = args.tachy
    signal = args.signal
    usermin = args.usermin

    return file, brady, tachy, signal, usermin

def file_size(file):
    import os
    from scipy.io import loadmat 
    import h5py 
    try:
        f = loadmat(file)
        d = dict(f)
        ECGvals = d.get('ecg')
        size = len(ECGvals[0])*2
        return size
    except:
        try: 
            f = h5py.File(file)
            d = dict(f)
            ECGvals = d.get('ecg')
            size = len(ECGvals)*2
            return size
        except:
            try:
                f = open(file, "rb")
                f.seek(0, os.SEEK_END)
                bytesize = f.tell()
                size = (bytesize / 2) - 1  
                return size
            except IOError:
                print("Could not open file.")
                return 0

def read_data(filename, SampFreq, iteration):
    """ read in raw data from binary file inputted by user

    :param: binary file, sampling frequency, and iteration number of loop in main method
    :returns: ten second data of binary file based on iteration """     
    from scipy.io import loadmat
    import h5py  
    
    try:
        f = loadmat(filename)
        d = dict(f)

        ECGvals = d.get('ecg')
        PPvals = d.get('pp')
        tensec_data = np.array([])

        i = 10*SampFreq*(iteration-1)

        while(i < 10*SampFreq*iteration):
            tensec_data = np.append(tensec_data, np.round(PPvals[0][i], 1))
            tensec_data = np.append(tensec_data, np.round(ECGvals[0][i], 1))
            i+=1

        return tensec_data

    except:
        try:
            f = h5py.File(filename)
            d = dict(f)

            ECGvals = d.get('ecg')
            PPvals = d.get('pp')
            tensec_data = np.array([])

            i = 10*SampFreq*(iteration-1)

            while(i < 10*SampFreq*iteration):
                tensec_data = np.append(tensec_data, np.round(PPvals[i], 1))
                tensec_data = np.append(tensec_data, np.round(ECGvals[i], 1))
                i+=1

            return tensec_data

        except:
            try:
                f = open(filename, "rb")
                f.seek(2*2*(10*SampFreq*iteration))
                tensec_data = np.array([])
                i = 0

                while(i < (20*SampFreq)):
                    data = f.read(2)
                    tensec_data = np.append(tensec_data, np.round(int.from_bytes(data, byteorder = 'little'), 1))
                    f.seek(0, 1)
                    i+=1       
                return tensec_data
            except IOError:
                return 0


def find_sampfreq(filename):
    """ find sampling frequency from the first values of the binary file

    :param: binary file
    :returns: ECG and Pulse sampling frequency  """ 
    from scipy.io import loadmat
    import h5py     

    try:
        f = loadmat(filename)
        d = dict(f)
        SampFreq = d.get('fs')
        SampFreq = SampFreq[0][0]
        return SampFreq
    except:
        try:
            f = h5py.File(filename)
            d = dict(f)
            SampFreq = d.get('fs')
            SampFreq = SampFreq[0][0]

            return SampFreq
        except:
            try:
                f = open(filename, "rb")
                SampFreqBoth = f.read(2) 
                SampFreq = int.from_bytes(SampFreqBoth, byteorder = 'little')
                return SampFreq
            except IOError:
                return 0


def obtain_ECG(tensec_data):
    """ obtain ECG values of ten second data

    :param: multiplexed ECG and Pleth data
    :returns: ECG data  """
    ECGData= tensec_data[1::2]

    return ECGData

def obtain_Pleth(tensec_data):
    """ obtain Pulse Pleth values of ten second data

    :param: multiplexed ECG and Pleth data
    :returns: Pleth data  """
    PlethData = tensec_data[0::2]

    return PlethData

def heart_rate_insta(ECGorPlethData):
    """ estimate number of peaks in 10 second ECG or Pleth data
    
    :param: 10 second ECG or Pleth data
    :returns: 10 second ECG or Pleth heart rate
    """
    instantaneous_HR_indicies = np.array([]) # Array which holds temporary values of heart rates as data is read

    i=6
    while i < ECGorPlethData.size-6:
        Databefore = np.average(ECGorPlethData[(i-5):(i-1)])

        Dataafter = np.average(ECGorPlethData[(i+1):(i+5)])

        if ECGorPlethData[i] > Databefore and ECGorPlethData[i] > Dataafter:
            instantaneous_HR_indicies = np.append(instantaneous_HR_indicies, i)
        i+=1
    
    ten_sec_info = len(instantaneous_HR_indicies)
   
    return ten_sec_info


def estimate_instantaneous_HR(signal, ten_sec_info_ECG, ten_sec_info_Pleth):
    """ estimate 10 second instantaneous heart rate

    :param: 10 second average of ECG and Pulse HR data and signal of interest
    :returns: instantaneous averaged heart rate
    """
    if(signal == "ECG"):
        tensec_info_avg = ten_sec_info_ECG
    elif(signal == "PLETH"):
        tensec_info_avg = ten_sec_info_Pleth
    else:
        tensec_info_avg = (ten_sec_info_ECG + ten_sec_info_Pleth) / 2


    instantaneous_HR = tensec_info_avg * 6

    print("10 second instantaneous heart rate is %d bmp." % instantaneous_HR, flush = True)
    logging.info("10 sec inst. HR: %d bpm" % instantaneous_HR)

    return instantaneous_HR

def alert_brady_tachy(tenmin_log):
    """ bradycardia alert

    :param: ten minute heart rate back log
    :returns: ten minute heart rate back log
    """
    
    tenmin_log_vals = list(tenmin_log)

    return tenmin_log_vals

def alert_log(instantaneous_HR, tenmin_log, brady, tachy):
    """ ten minute log output in the case of bradycardia or tachycardia

    :param: 10 second heart rate, ten minute log, bradycardia threshold, tachycardia threshold
    :returns:
    """
    if(instantaneous_HR < brady):
        tenmin_log_brady = alert_brady_tachy(tenmin_log)
        print("Alert, bradycardia detected! Here is 10 minute backlog: ", flush = True)
        print(tenmin_log_brady, flush = True)
        logging.warning("Alert, bradycardia detected! Here is 10 minute backlog: ")
        logging.warning(tenmin_log_brady)


    if(instantaneous_HR > tachy):
        tenmin_log_tachy = alert_brady_tachy(tenmin_log)
        print("Alert, tachycardia detected! Here is 10 minute backlog: ", flush = True)
        print(tenmin_log_tachy, flush = True)
        logging.warning("Alert, tachycardia detected! Here is 10 minute backlog: ")
        logging.warning(tenmin_log_tachy)


def some_min_avg(onemin_avg_log, fivemin_avg_log, usermin_avg_log, usermin):
    """ some minute average heart rate output

    :param: one minute HR log, five minute HR log, user inputted minute HR log
    :returns: 
    """

    if(len(onemin_avg_log) == 6):
        onemin_avg = sum(onemin_avg_log) / len(onemin_avg_log)
        print("1 minute average heart rate is %d." % onemin_avg, flush = True)
        logging.info("1 min. avg. HR: %d bpm" % onemin_avg)

    if(len(fivemin_avg_log) == 30):
        fivemin_avg = sum(fivemin_avg_log) / len(fivemin_avg_log)
        print("5 minute average heart rate is %d." % fivemin_avg, flush = True)
        logging.info("5 min. avg. HR: %d bpm" % fivemin_avg)

    if(len(usermin_avg_log) == (usermin*6)):
        usermin_avg = sum(usermin_avg_log) / len(usermin_avg_log)
        print("%d minute average heart rate is %d." % (usermin, usermin_avg), flush = True)
        logging.info("%d min. avg. HR: %d bpm" % (usermin, usermin_avg))




    
