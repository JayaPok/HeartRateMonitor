from heart_rate_monitoring import read_data, find_sampfreq

def test_filetypes():
    from scipy.io import loadmat
    import h5py  
    import numpy as np
    
    binary_sampfreq = find_sampfreq('test1.bin')
    matlab_sampfreq = find_sampfreq('matvals.mat')

    assert binary_sampfreq == 20000
    assert matlab_sampfreq == 16717
