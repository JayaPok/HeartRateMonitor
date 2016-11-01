from heart_rate_monitoring import read_data, find_sampfreq, obtain_ECG, obtain_Pleth, \
estimate_instantaneous_HR, some_min_avg, file_size, heart_rate_insta, alert_brady_tachy, alert_log, parse_cli, main_arg
import collections
import os
import logging
from scipy.io import loadmat
import h5py 
import sys


if __name__ == "__main__":
    """ run all functions of heart_rate_monitoring file
    
    :param: binary multiplexed data file
    :returns: prints instantaneous heart rate, one minute heart rate, five minute heart rate, and heart rate log in the case of alert """ 
    
    file, brady, tachy, signal, usermin = main_arg()

    logging.basicConfig(level=logging.INFO, filename="log.txt", filemode = 'w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    SampFreq = find_sampfreq(file)

    tenmin_log = collections.deque([], maxlen = 60)
    onemin_avg_log = collections.deque([], maxlen = 6)
    fivemin_avg_log = collections.deque([], maxlen = 30)
    usermin_avg_log = collections.deque([], maxlen = (usermin*6))

    size = file_size(file)

    iteration = 1
    contrun = 1
    
    try:
        while contrun == 1:
            if (20*iteration*SampFreq > size+1):
                logging.debug("File is finished!")
                sys.exit()

            tensec_data = read_data(file, SampFreq, iteration)
            ECGData = obtain_ECG(tensec_data)
            PlethData = obtain_Pleth(tensec_data)
        
            ten_sec_info_ECG = heart_rate_insta(ECGData)
            ten_sec_info_Pleth = heart_rate_insta(PlethData)

            instantaneous_HR = estimate_instantaneous_HR(signal, ten_sec_info_ECG, ten_sec_info_Pleth)
            
            tenmin_log.append(instantaneous_HR)
            alert_log(instantaneous_HR, tenmin_log, brady, tachy)
            onemin_avg_log.append(instantaneous_HR)
            fivemin_avg_log.append(instantaneous_HR)
            usermin_avg_log.append(instantaneous_HR)

            some_min_avg(onemin_avg_log, fivemin_avg_log, usermin_avg_log, usermin)

            if(len(onemin_avg_log) == 6):
                onemin_avg_log.clear()

            if(len(fivemin_avg_log) == 30):
                fivemin_avg_log.clear()

            if(len(usermin_avg_log) == (usermin*6)):
                usermin_avg_log.clear()
        
            iteration += 1
    except EOFError:
        print("End of file.")
        logging.error("End of file.")
    except KeyboardInterrupt:
        print("You canceled the operation.")
        logging.error("You canceled the operation.")
    except:
        print("An error has occured.")
        logging.error("An error has occured.")

