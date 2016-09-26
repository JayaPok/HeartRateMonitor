from heart_rate_monitoring import read_data, heart_rate_indicies_ECG, heart_rate_indicies_Plethysmograph, \
estimate_instantaneous_HR, estimate_heart_rate_oneminute_index, estimate_heart_rate_fiveminute_index

if __name__ == "__main__":
    
    ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData = read_data("test.bin")
    print(ECGSampFreqHz)


