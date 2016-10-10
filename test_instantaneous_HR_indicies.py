from heart_rate_monitoring import heart_rate_indicies_ECG, heart_rate_indicies_Plethysmograph

def test_instantaneous_HR_indicies():
    """ test instantaneous_HR_indicies() method

    :param signal: input sine wave
    :returns: assertion of expected 0 indicies of peaks in sine wave against the measured values from using test instantaneous_HR_indicies() method
    """
    import numpy as np
    Fs = 80
    sample = 80
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))

    instantaneous_HR_indicies_ECG = heart_rate_indicies_ECG(y)
    instantaneous_HR_indicies_Pleth = heart_rate_indicies_Plethysmograph(y)

    assert instantaneous_HR_indicies_ECG[0] == 4
    assert instantaneous_HR_indicies_ECG[1] == 20
    assert instantaneous_HR_indicies_ECG[2] == 36
    assert instantaneous_HR_indicies_ECG[3] == 52
    assert instantaneous_HR_indicies_ECG[4] == 68
