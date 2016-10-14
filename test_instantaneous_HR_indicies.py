from heart_rate_monitoring import heart_rate_ECG_insta, heart_rate_Pleth_insta

def test_instantaneous_HR_indicies():
    """ test heart_rate_ECG_insta() and heart_rate_Pleth_insta() method

    :param signal: input sine wave
    :returns: assertion of expected number of peaks in sine wave against the measured values from using test respective methods
    """
    import numpy as np
    Fs = 80
    sample = 80
    f = 5
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * f * x / Fs))

    heart_rate_ECG_length = heart_rate_ECG_insta(y)
    heart_rate_Pleth_length = heart_rate_Pleth_insta(y)

    assert heart_rate_ECG_length == 5
    assert heart_rate_Pleth_length == 5
