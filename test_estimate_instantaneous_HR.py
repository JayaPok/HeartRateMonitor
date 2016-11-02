from heart_rate_monitoring import heart_rate_insta, estimate_instantaneous_HR


def test_estimate_instantaneous_HR():
    """ test estimate_instantaneous_HR() method

    :param signal: input sine wave, and 0 indicies of peaks in sine wave
    :returns: assertion of the last instantaneous heart rate value of estimate_instantaneous_HR() method against the measured value
    """

    import numpy as np
    Fs = 80
    sample = 8000
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * x / Fs))


    heart_rate_length = heart_rate_insta(y)
    instantaneous_HR = estimate_instantaneous_HR("ECG", heart_rate_length, heart_rate_length)

    assert instantaneous_HR == 600
