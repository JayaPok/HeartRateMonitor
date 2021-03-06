import numpy as np
import collections
import logging


def parse_cli():
    """ argparse capabilites that enables user to input values to change output

    :param: user inputed values for one or more of filename, bradycardia
     threshold, tachycardia threshold, signal type,
     and desired minute HR average
    :return args: user inputted arguments
    """

    import argparse as ap

    par = ap.ArgumentParser(description="run program for inputted binary file",
                            formatter_class=ap.ArgumentDefaultsHelpFormatter)
    par.add_argument("--file", dest="file", help="input binary file", type=str)
    par.add_argument("--brady", dest="brady",
                     help="input bradycardia starting heart rate",
                     type=int, default=30)
    par.add_argument("--tachy", dest="tachy",
                     help="input tachycardia starting heart rate",
                     type=int, default=240)
    par.add_argument("--signal", dest="signal",
                     help="input ECG for ECG signal HR estimation, "
                          "PLETH for Plethysmograph HR estimation, "
                          "or BOTH for an average of both signals "
                          "HR estimation", type=str, default="BOTH")
    par.add_argument("--usermin", dest="usermin",
                     help="input desired multi-minute heart rate average",
                     type=int, default=2)

    args = par.parse_args()

    return args


def main_arg():
    """ run all functions of heart_rate_monitoring file

    :param: arg arguments from argparse
    :return file: return user inputted file
    :return brady: return user inputted bradycardia value
    :return tachy: return user inputted tachycardia value
    :return signal: return user inputted signal
    :return usermin: return user inputted number of minutes HR
    """

    args = parse_cli()

    file = args.file
    brady = args.brady
    tachy = args.tachy
    signal = args.signal
    usermin = args.usermin

    return file, brady, tachy, signal, usermin


def file_size(file):
    """ determine size of matlab, hd5f, or binary file

    :param file: user inputted file
    :return size: size of file
    """

    import os
    from scipy.io import loadmat
    import h5py 
    try:
        f = loadmat(file)
        d = dict(f)
        ecgvals = d.get('ecg').T.astype(np.float)
        size = len(ecgvals[0]) * 2
        return size
    except:
        try: 
            f = h5py.File(file)
            d = dict(f)
            ecgvals = d.get('ecg')[0].T.astype(np.float)
            size = len(ecgvals) * 2
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


def read_data(filename, sampfreq, iteration, signal):
    """ read in raw data from matlab, hdf5, or binary file inputted by user

    :param filename: user inputted file
    :param sampfreq: sample frequency of file
    :param iteration: position in file data that is being read
    :param signal: signal type specified by user
    :return tensec_data: ten seconds worth of heart rate data
    """

    from scipy.io import loadmat
    import h5py

    try:
        f = loadmat(filename)
        d = dict(f)

        if signal == "ECG":
            ecgvals = d.get('ecg').T.astype(np.float)
            ppvals = d.get('ecg').T.astype(np.float)
        elif signal == "PLETH":
            ecgvals = d.get('pp').T.astype(np.float)
            ppvals = d.get('pp').T.astype(np.float)
        else:
            ecgvals = d.get('ecg').T.astype(np.float)
            ppvals = d.get('pp').T.astype(np.float)

        tensec_data = np.array([])

        i = int(10 * sampfreq * (iteration - 1))

        while i < 10*sampfreq*iteration:
            tensec_data = np.append(tensec_data, np.round(ppvals[0][i], 1))
            tensec_data = np.append(tensec_data, np.round(ecgvals[0][i], 1))
            i += 1

        return tensec_data

    except:
        try:
            f = h5py.File(filename)
            d = dict(f)

            if signal == "ECG":
                ecgvals = d.get('ecg')[0].T.astype(np.float)
                ppvals = d.get('ecg')[0].T.astype(np.float)
            elif signal == "PLETH":
                ecgvals = d.get('pp')[0].T.astype(np.float)
                ppvals = d.get('pp')[0].T.astype(np.float)
            else:
                ecgvals = d.get('ecg')[0].T.astype(np.float)
                ppvals = d.get('pp')[0].T.astype(np.float)
                
                tensec_data = np.array([])

            i = int(10*sampfreq*(iteration-1))

            while i < 10*sampfreq*iteration:
                tensec_data = np.append(tensec_data, np.round(ppvals[i], 1))
                tensec_data = np.append(tensec_data, np.round(ecgvals[i], 1))
                i += 1

            return tensec_data

        except:
            try:
                f = open(filename, "rb")
                f.seek(2*2*(10*sampfreq*iteration))
                tensec_data = np.array([])
                i = 0

                while i < (20*sampfreq):
                    data = f.read(2)
                    tensec_data = np.append(tensec_data, np.round(
                        int.from_bytes(data, byteorder='little'), 1))
                    f.seek(0, 1)
                    i += 1
                return tensec_data
            except IOError:
                return 0


def find_sampfreq(filename):
    """ find sampling frequency from matlab, hdf5, or binary file

    :param filename: user inputted file
    :return sampfreq: sample frequency found from file
    """

    from scipy.io import loadmat
    import h5py

    try:
        f = loadmat(filename)
        d = dict(f)
        sampfreq = (d.get('fs')).astype(np.float)
        sampfreq = sampfreq[0][0]
        return sampfreq
    except:
        try:
            f = h5py.File(filename)
            d = dict(f)
            sampfreq = (d.get('fs')[0]).astype(np.float)
            sampfreq = sampfreq[0]

            return sampfreq
        except:
            try:
                f = open(filename, "rb")
                sampfreqboth = f.read(2)
                sampfreq = int.from_bytes(sampfreqboth, byteorder='little')
                return sampfreq
            except IOError:
                return 0


def obtain_ECG(tensec_data):
    """ obtain ECG values of ten second data

    :param tensec_data: 10 seconds worth of heart rate data points
    :return ECGData: ECG unmultiplexed data
    """

    ECGData = tensec_data[1::2]

    return ECGData


def obtain_Pleth(tensec_data):
    """ obtain Pulse Pleth values of ten second data

    :param tensec_data: 10 seconds worth of heart rate data points
    :return PlethData: Pulse Pleth unmultiplexed data
    """

    PlethData = tensec_data[0::2]

    return PlethData


def heart_rate_insta(ECGorPlethData):
    """ estimate number of peaks in 10 second ECG or Pleth data

    :param ECGorPlethData: 10 seconds worth of heart rate data points
    :return ten_sec_info: number of peaks in 10 seconds of data
    """

    instantaneous_HR_indicies = np.array([])  # Array which holds
    # temporary values of heart rates as data is read

    i = 6
    while i < ECGorPlethData.size-6:
        Databefore = np.average(ECGorPlethData[(i-5):(i-1)])

        Dataafter = np.average(ECGorPlethData[(i+1):(i+5)])

        if ECGorPlethData[i] > Databefore and ECGorPlethData[i] > Dataafter:
            instantaneous_HR_indicies = np.append(instantaneous_HR_indicies, i)
        i += 1

    ten_sec_info = len(instantaneous_HR_indicies) / 3

    return ten_sec_info


def estimate_instantaneous_HR(signal, ten_sec_info_ECG, ten_sec_info_Pleth):
    """ estimate 10 second instantaneous heart rate

    :param signal: signal of "ECG", "PLETH", or "BOTH
    :param ten_sec_info_ECG: ten second heart rate ECG data
    :param ten_sec_info_Pleth: ten second heart rate Pulse Pleth data
    :return instantaneous_HR: instantaneous heart rate of 10 second data
    """

    if signal == "ECG":
        tensec_info_avg = ten_sec_info_ECG
    elif signal == "PLETH":
        tensec_info_avg = ten_sec_info_Pleth
    else:
        tensec_info_avg = (ten_sec_info_ECG + ten_sec_info_Pleth) / 2

    instantaneous_HR = tensec_info_avg * 6

    print("10 second instantaneous heart rate is %d bmp." % instantaneous_HR,
          flush=True)
    logging.info("10 sec inst. HR: %d bpm" % instantaneous_HR)

    return instantaneous_HR


def alert_brady_tachy(tenmin_log):
    """ bradycardia/tachycardia alert

    :param tenmin_log: log containing up to last 60 values of past 10 seconds
     of HR data
    :return tenmin_log_vals: ten minute log in the form of a list
    """

    tenmin_log_vals = list(tenmin_log)

    return tenmin_log_vals


def alert_log(instantaneous_HR, tenmin_log, brady, tachy):
    """ ten minute log output in the case of bradycardia or tachycardia

    :param instantaneous_HR: heart rate obtained from previous 10 seconds of HR data
    :param tenmin_log: log containing up to last 60 values of past 10 seconds of
     HR data
    :param brady: heart rate value representing bradycardia
    :param tachy: heart rate value representing tachycardia
    :return: prints log in case of alarm
    """

    if instantaneous_HR < brady:
        tenmin_log_brady = alert_brady_tachy(tenmin_log)
        print("Alert, bradycardia detected! Here is 10 minute backlog: ",
              flush=True)
        print(tenmin_log_brady, flush=True)
        logging.warning("Alert, bradycardia detected! Here is 10 minute"
                        " backlog: ")
        logging.warning(tenmin_log_brady)

    if instantaneous_HR > tachy:
        tenmin_log_tachy = alert_brady_tachy(tenmin_log)
        print("Alert, tachycardia detected! Here is 10 minute backlog: ",
              flush=True)
        print(tenmin_log_tachy, flush=True)
        logging.warning("Alert, tachycardia detected! Here is 10 minute"
                        " backlog: ")
        logging.warning(tenmin_log_tachy)


def some_min_avg(onemin_avg_log, fivemin_avg_log, usermin_avg_log, usermin):
    """some minute average heart rate output

    :param onemin_avg_log: log of 6 values of 10 second instantaneous
     heart rate over the past minute
    :param fivemin_avg_log: log of 30 values of 10 second
    instantaneous heart rate over the past 5 minutes
    :param usermin_avg_log: log of usermin*6 values of 10 second
    instantaneous heart rate over the past user inputted minutes
    :param usermin: user inputted minute to be averaged
    :return onemin_avg: one minute average of heart rate
    :return fivemin_avg: five minute average of heart rate
    :return usermin_avg: user inputted minute average of heart rate
    """

    if len(onemin_avg_log) == 6:
        onemin_avg = sum(onemin_avg_log) / len(onemin_avg_log)
        print("1 minute average heart rate is %d." % onemin_avg, flush=True)
        logging.info("1 min. avg. HR: %d bpm" % onemin_avg)
    else:
        onemin_avg = None

    if len(fivemin_avg_log) == 30:
        fivemin_avg = sum(fivemin_avg_log) / len(fivemin_avg_log)
        print("5 minute average heart rate is %d." % fivemin_avg, flush=True)
        logging.info("5 min. avg. HR: %d bpm" % fivemin_avg)
    else:
        fivemin_avg = None

    if len(usermin_avg_log) == (usermin*6):
        usermin_avg = sum(usermin_avg_log) / len(usermin_avg_log)
        print("%d minute average heart rate is %d." % (usermin, usermin_avg),
              flush=True)
        logging.info("%d min. avg. HR: %d bpm" % (usermin, usermin_avg))
    else:
        usermin_avg = None

    return onemin_avg, fivemin_avg, usermin_avg
