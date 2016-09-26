from heart_rate_monitoring import read_data, heart_rate_indicies_ECG, heart_rate_indicies_Plethysmograph, \
estimate_instantaneous_HR, estimate_heart_rate_oneminute_index, estimate_heart_rate_fiveminute_index

if __name__ == "__main__":
    """ run all functions of heart_rate_monitoring file as well as input a time increment and run values simultaneously

    :param: none
    :returns: prints instantaneous heart rate, one minute heart rate, and five minute heart rate """ 

    ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData = read_data()
    instantaneous_HR_indicies_ECG = heart_rate_indicies_ECG(ECGData)
    instantaneous_HR_indicies_Pleth = instantaneous_HR_indicies_Pleth(PlethData)
    instantaenous_HR_Pleth = estimate_instantaneous_HR(instantaneous_HR_indicies_Pleth, PlethSampFreqHz)
    one_minute_total_HR_Pleth = estimate_heart_rate_oneminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz)
    five_minute_total_HR_Pleth = estimate_heart_rate_fiveminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz)

    import time
    from threading import Thread

    def run_instantaneous_HR():
    """ run instantaneous heart rate array at a time increment

    :param: none
    :returns: prints instantaneous heart rate at the exact time delay of the heart beat """ 
        i = 0
        while i < len(instantaenous_HR_Pleth):
            print("Instantaneous heart rate: ", instantaenous_HR_Pleth[i])
            sec_per_beat = 60 / instantaenous_HR_Pleth[i]
            time.sleep(sec_per_beat)
            i+=1
 
    def run_one_minute_instantaneous():
    """ run one minute heart rate average and displays every minute

    :param: none
    :returns: prints one minute heart rate average """ 
        j = 0
        while j < len(one_minute_total_HR_Pleth):
            print("One minute average heart rate: ", one_minute_total_HR_Pleth)
            time.sleep(60)
            j+=1

    def run_five_minute_instantaneous():
    """ run five minute heart rate average and displays every minute

    :param: none
    :returns: prints five minute heart rate average """ 
        k = 0
        while k < len(five_minute_total_HR_Pleth):
            print("Five minute average heart rate: ", five_minute_total_HR_Pleth)
            time.sleep(300)
            k+=1

    run1 = Thread(target = run_instantaneous_HR)
    run2 = Thread(target = run_one_minute_instantaneous)
    run3 = Thread(target = run_five_minute_instantaneous)	 

    run1.start()
    run2.start()
    run3.start()