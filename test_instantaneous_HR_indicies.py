from heart_rate_monitoring import heart_rate_insta


def test_instantaneous_HR_indicies():

    import numpy as np
    Fs = 80
    sample = 8000
    x = np.arange(sample)
    y = np.array(np.sin(2 * np.pi * x / Fs))

    heart_rate_length = heart_rate_insta(y)

    assert heart_rate_length == 100
