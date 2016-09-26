from heart_rate_monitoring import heart_rate_indicies_Plethysmograph, estimate_heart_rate_fiveminute_index

def test_estimate_heart_rate_fiveminute_index():
    """ test estimate_heart_rate_fiveminute_index() method

    :param signal: input sine wave, and 0 indicies of peaks in sine wave
    :returns: assertion of the last instantaneous five minute heart rate value of estimate_heart_rate_fiveminute_index() method against the measured value
    """
    
    import numpy as np
    Fs = 80
    sample = 100000
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))

    instantaneous_HR_indicies_Pleth = heart_rate_indicies_Plethysmograph(y)
    one_minute_total_HR_Pleth = estimate_heart_rate_fiveminute_index(instantaneous_HR_indicies_Pleth, Fs)

    assert one_minute_total_HR_Pleth == 300.2