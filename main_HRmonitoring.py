from heart_rate_monitoring import read_data, find_sampfreq, obtain_ECG, obtain_Pleth, heart_rate_ECG_insta, heart_rate_Pleth_insta, \
estimate_instantaneous_HR, alert_brady, alert_tachy, one_min_avg, five_min_avg
import collections

def parse_cli():
    import argparse as ap

    par = ap.ArgumentParser(description = "run program for inputted binary file", formatter_class = ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("--file", dest = "file", help="input binary file")


    args = par.parse_args()

    return args


def main():
    args = parse_cli()

    file = args.file

    return file


if __name__ == "__main__":
    """ run all functions of heart_rate_monitoring file
    
    :param: binary multiplexed data file
    :returns: prints instantaneous heart rate, one minute heart rate, five minute heart rate, and heart rate log in the case of alert """ 
    
    file = main()

    SampFreq = find_sampfreq(file)

    tenmin_log = collections.deque([], maxlen = 60)
    onemin_avg_log = collections.deque([], maxlen = 6)
    fivemin_avg_log = collections.deque([], maxlen = 30)
    iteration = 1

    while(iteration < 1000):
        tensec_data = read_data(file, SampFreq, iteration)
        ECGData = obtain_ECG(tensec_data)
        PlethData = obtain_Pleth(tensec_data)
        
        ten_sec_info_ECG = heart_rate_ECG_insta(ECGData)
        ten_sec_info_Pleth = heart_rate_Pleth_insta(PlethData)

        tensec_info_avg = (ten_sec_info_ECG + ten_sec_info_Pleth) / 2

        instantaneous_HR = estimate_instantaneous_HR(tensec_info_avg)
        tenmin_log.append(instantaneous_HR)
        onemin_avg_log.append(instantaneous_HR)
        fivemin_avg_log.append(instantaneous_HR)
        
        print("Ten second instantaneous heart rate is %d." % instantaneous_HR)
        
        if(instantaneous_HR < brady):
            tenmin_log_brady = alert_brady(tenmin_log)
            print("Alert, bradycardia detected! Here is 10 minute backlog: ")
            print(tenmin_log_brady)

        if(instantaneous_HR > tachy):
            tenmin_log_tachy = alert_tachy(tenmin_log)
            print("Alert, tachycardia detected! Here is 10 minute backlog: ")
            print(tenmin_log_tachy)

        if(len(onemin_avg_log) == 6):
            onemin_avg = one_min_avg(onemin_avg_log)
            print(onemin_avg)
            onemin_avg_log.clear()

        if(len(fivemin_avg_log) == 30):
            fivemin_avg = five_min_avg(fivemin_avg_log)
            print(fivemin_avg)
            fivemin_avg_log.clear()
        
        iteration += 1

