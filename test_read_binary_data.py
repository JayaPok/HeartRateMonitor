from heart_rate_monitoring import find_sampfreq

def test_read_data():
    """ test read_data file

    :param signal: filename = "test.bin"
    :returns: ECG Sampling Frequency, Pulse Plethysmograph Sampling Frequency, ECG sampling values array, Pulse Plethysmograph sampling values array """ 

    import numpy as np

    SampFreq = find_sampfreq("test.bin")
    
    assert SampFreq == 770

