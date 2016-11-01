from heart_rate_monitoring import heart_rate_insta


def test_instantaneous_HR_indicies():
    """ test heart_rate_insta()

    :param signal: input sine wave
    :returns: assertion of expected number of peaks in
     sine wave against the measured values from using test respective methods
    """
    import numpy as np
    Fs = 80
    sample = 8000
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * x / Fs))

    heart_rate_ECG_length = heart_rate_insta(y)
    heart_rate_Pleth_length = heart_rate_insta(y)

    assert heart_rate_ECG_length == 12
    assert heart_rate_Pleth_length == 12
