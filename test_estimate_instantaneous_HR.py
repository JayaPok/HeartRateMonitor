from heart_rate_monitoring import heart_rate_indicies_Plethysmograph, estimate_instantaneous_HR

def test_estimate_instantaneous_HR():

    import numpy as np
    Fs = 80
    sample = 20
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))


    instantaneous_HR_indicies_Pleth = heart_rate_indicies_Plethysmograph(y)
    instantaenous_HR = estimate_instantaneous_HR(instantaneous_HR_indicies_Pleth, Fs)


    assert instantaenous_HR == [300, 300, 300]

#     all_HR = []
#     k = 0
#     while k < len(instantaneous_HR_indicies_Pleth)-1:
#         instantaenous_HR = ((60 * Fs) / (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k])) # calculates instantaenous HR for each beat
#         all_HR.append(instantaenous_HR)
#         print(instantaenous_HR)
#         if instantaenous_HR < 30: # detects for Bradycardia where heart rate is below 30 bpm
#             print("Bradycardia alert! Here is 10 minute trace of heart rate:")
#             invertedHR = np.array(all_HR[::-1])
#             invertedHRseconds = 1 / (invertedHR / 60)
#             HR_sum = 0
#             for x in range(0, k):
#                 HR_sum = HR_sum + invertedHRseconds[x]
#                 ten_min_invert = invertedHR[0:x]
#                 ten_min_real = np.array(ten_min_invert[::-1])
#                 if np.sum(ten_min_real) > 600:
#                     print(ten_min_real)
#                     break
#         if instantaenous_HR > 240: # detects for Bradycardia where heart rate is above 240 bpm
#             print("Tachycardia alert! Here is 10 minute trace of heart rate:")
#             invertedHR = np.array(all_HR[::-1])
#             invertedHRseconds = 1 / (invertedHR / 60)
#             HR_sum = 0
#             for x in range(0, k):
#                 HR_sum = HR_sum + invertedHRseconds[x]
#                 ten_min_invert = invertedHR[0:x]
#                 ten_min_real = np.array(ten_min_invert[::-1])
#                 if np.sum(ten_min_real) > 600:
#                     print(ten_min_real)
#                     break
#         k+=1

#    #assert a == ""

# test_estimate_instantaneous_HR()