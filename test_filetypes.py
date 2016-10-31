from heart_rate_monitoring import read_data, find_sampfreq

def test_filetypes():
    from scipy.io import loadmat
    import h5py  
    import numpy as np
    
    binary_sampfreq = find_sampfreq('test1.bin')
    matlab_sampfreq = find_sampfreq('ecg_pp_vals.mat')
    h5py_sampfreq = find_sampfreq('ecg_pp_vals_h5py.mat')

    matlab_data_tensec = read_data('ecg_pp_vals.mat', matlab_sampfreq, 1)
    h5py_data_tensec = read_data('ecg_pp_vals_h5py.mat', h5py_sampfreq, 1)
    binary_data_tensec = read_data('test1.bin', 10, 1)

    assert binary_sampfreq == 20000
    assert matlab_sampfreq == 5000
    assert h5py_sampfreq == 5000

    assert matlab_data_tensec[0:10] == [45.5, 45.5, 45.3, 45.3, 45.1, 45.1, 44.9, 44.9, 44.8, 44.8]
    assert h5py_data_tensec[0:10] == [45.5, 45.5, 45.3, 45.3, 45.1, 45.1, 44.9, 44.9, 44.8, 44.8]
    assert binary_data_tensec[0:10] == [21608, 34362, 21624, 34378, 21398, 34394, 21495, 34410, 21737, 34426]
