from heart_rate_monitoring import read_data

def test_read_data():
    """ read in raw data from binary file

    :param: read_data() "
    :returns: true/false whether return values in read_data function is equal to the expected values"""    
    import numpy as np
    
    ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData  = read_data("test.bin")

    assert ECGSampFreqHz == 770
    assert PlethSampFreqHz == 1284
    assert ECGData == [1798]
    assert PlethData == [2312]

