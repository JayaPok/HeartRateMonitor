from heart_rate_monitoring import read_data

def test_read_data():
    """ test read_data file

    :param signal: filename = "test.bin"
    :returns: ECG Sampling Frequency, Pulse Plethysmograph Sampling Frequency, ECG sampling values array, Pulse Plethysmograph sampling values array """ 

    import numpy as np
    
    ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData  = read_data("test.bin")

    assert ECGSampFreqHz == 770
    assert PlethSampFreqHz == 1284
    assert ECGData == [1798]
    assert PlethData == [2312]

