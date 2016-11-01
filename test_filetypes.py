from heart_rate_monitoring import read_data, find_sampfreq

def test_filetypes():
    from scipy.io import loadmat
    import h5py  
    import numpy as np
    
    binary_sampfreq = find_sampfreq('test1.bin')
    matlab_sampfreq = find_sampfreq('test_filetypes.mat')
    h5py_sampfreq = find_sampfreq('test_filetypes_h5py.mat')

    matlab_data_tensec = read_data('test_filetypes.mat', matlab_sampfreq, 1)
    h5py_data_tensec = read_data('test_filetypes_h5py.mat', h5py_sampfreq, 1)
    binary_data_tensec = read_data('test1.bin', 10, 1)

    assert binary_sampfreq == 20000
    assert matlab_sampfreq == 1
    assert h5py_sampfreq == 1

    assert np.all(matlab_data_tensec == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9])
    assert np.all(h5py_data_tensec == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9])
    assert np.all(binary_data_tensec[0:10] == [21608, 34362, 21624, 34378, 21398, 34394, 21495, 34410, 21737, 34426])
