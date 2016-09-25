from heart_rate_monitoring import heart_rate_indicies_ECG, heart_rate_indicies_Plethysmograph

def test_instantaneous_HR_indicies():

    import numpy as np
    Fs = 80
    sample = 80
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))

    instantaneous_HR_indicies_ECG = heart_rate_indicies_ECG(y)
    instantaneous_HR_indicies_Pleth = heart_rate_indicies_Plethysmograph(y)

    assert instantaneous_HR_indicies_ECG == [4, 20, 36, 52, 68]
    assert instantaneous_HR_indicies_Pleth == [4, 20, 36, 52, 68]