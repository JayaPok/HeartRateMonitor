from heart_rate_monitoring import read_data, find_sampfreq, obtain_ECG, obtain_Pleth, heart_rate_ECG_insta, heart_rate_Pleth_insta, \
estimate_instantaneous_HR, alert_brady, alert_tachy, some_min_avg
import collections
import os
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


def main():
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


if __name__ == "__main__":
    """ run all functions of heart_rate_monitoring file
    
    :param: binary multiplexed data file
    :returns: prints instantaneous heart rate, one minute heart rate, five minute heart rate, and heart rate log in the case of alert """ 
    
    file, brady, tachy, signal, usermin = main()

    logging.basicConfig(level=logging.INFO, filename="log.txt", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    SampFreq = find_sampfreq(file)

    tenmin_log = collections.deque([], maxlen = 60)
    onemin_avg_log = collections.deque([], maxlen = 6)
    fivemin_avg_log = collections.deque([], maxlen = 30)
    usermin_avg_log = collections.deque([], maxlen = (usermin*6))

    try:
        f = open(file, "rb")
        f.seek(0, os.SEEK_END)
        size = f.tell()
    except:
        try: 
            f = loadmat(file)
            d = dict(f)
            ECGvals = d.get('ecg')
            size = len(ECGvals[0])*2
        except:
            try:
                f = h5py.File(filename)
                d = dict(f)
                ECGvals = d.get('ecg')
                size = len(ECGvals[0])*2
            except IOError:
                print("Could not open file.")

    iteration = 1
    continuerun = True
    
    try:
        while continuerun:
            if ((20*iteration) > size):
                continuerun = False

            tensec_data = read_data(file, SampFreq, iteration)
            ECGData = obtain_ECG(tensec_data)
            PlethData = obtain_Pleth(tensec_data)
        
            ten_sec_info_ECG = heart_rate_ECG_insta(ECGData)
            ten_sec_info_Pleth = heart_rate_Pleth_insta(PlethData)

            if(signal == "ECG"):
                tensec_info_avg = ten_sec_info_ECG
            elif(signal == "PLETH"):
                tensec_info_avg = ten_sec_info_Pleth
            else:
                tensec_info_avg = (ten_sec_info_ECG + ten_sec_info_Pleth) / 2

            instantaneous_HR = estimate_instantaneous_HR(tensec_info_avg)
            tenmin_log.append(instantaneous_HR)
            onemin_avg_log.append(instantaneous_HR)
            fivemin_avg_log.append(instantaneous_HR)
            usermin_avg_log.append(instantaneous_HR)
        
            print("10 second instantaneous heart rate is %d bmp." % instantaneous_HR)
            logging.info("10 sec inst. HR: %d bpm" % instantaneous_HR)
        
            if(instantaneous_HR < brady):
                tenmin_log_brady = alert_brady(tenmin_log)
                print("Alert, bradycardia detected! Here is 10 minute backlog: ")
                print(tenmin_log_brady)
                logging.warning("Alert, bradycardia detected! Here is 10 minute backlog: ")
                logging.warning(tenmin_log_brady)


            if(instantaneous_HR > tachy):
                tenmin_log_tachy = alert_tachy(tenmin_log)
                print("Alert, tachycardia detected! Here is 10 minute backlog: ")
                print(tenmin_log_tachy)
                logging.warning("Alert, tachycardia detected! Here is 10 minute backlog: ")
                logging.warning(tenmin_log_brady)

            if(len(onemin_avg_log) == 6):
                onemin_avg = some_min_avg(onemin_avg_log)
                print("1 minute average heart rate is %d." % onemin_avg)
                logging.info("1 min. avg. HR: %d bpm" % onemin_avg)
                onemin_avg_log.clear()

            if(len(fivemin_avg_log) == 30):
                fivemin_avg = some_min_avg(fivemin_avg_log)
                print("5 minute average heart rate is %d." % fivemin_avg)
                logging.info("5 min. avg. HR: %d bpm" % fivemin_avg)
                fivemin_avg_log.clear()

            if(len(usermin_avg_log) == (usermin*6)):
                usermin_avg = some_min_avg(usermin_avg_log)
                print("%d minute average heart rate is %d." % (usermin, usermin_avg))
                logging.info("%d min. avg. HR: %d bpm" % (usermin, usermin_avg))
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

