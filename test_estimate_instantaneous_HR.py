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

    assert instantaenous_HR == 300
