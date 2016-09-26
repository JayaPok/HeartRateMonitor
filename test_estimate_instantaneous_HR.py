from heart_rate_monitoring import heart_rate_indicies_Plethysmograph, estimate_instantaneous_HR

def test_estimate_instantaneous_HR():
    """ test estimate_instantaneous_HR() method

    :param signal: input sine wave, and 0 indicies of peaks in sine wave
    :returns: assertion of the last instantaneous heart rate value of estimate_instantaneous_HR() method against the measured value
    """

    import numpy as np
    Fs = 80
    sample = 80
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))


    instantaneous_HR_indicies_Pleth = [4, 20, 36, 52, 68]
    instantaenous_HR = estimate_instantaneous_HR(instantaneous_HR_indicies_Pleth, Fs)


    all_HR_Pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        instantaenous_HR_Pleth = ((60 * Fs) / (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k])) # calculates instantaenous HR for each beat
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
                    print(ten_min_real_Pleth)
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
                    print(ten_min_real_Pleth)
                    break
        else:
            print(instantaenous_HR_Pleth)
        k+=1     
test_estimate_instantaneous_HR()
   # assert instantaenous_HR == 300
