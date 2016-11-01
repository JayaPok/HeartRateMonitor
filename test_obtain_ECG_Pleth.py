from heart_rate_monitoring import read_data, find_sampfreq, obtain_ECG, obtain_Pleth


def test_obtain_ECG_Pleth():
    from scipy.io import loadmat
    import numpy as np

    matlab_sampfreq = find_sampfreq('test_filetypes.mat')
    matlab_data_tensec = read_data('test_filetypes.mat', matlab_sampfreq, 1)
    
    ECGData = obtain_ECG(matlab_data_tensec)
    PlethData = obtain_Pleth(matlab_data_tensec)

    assert np.all(ECGData == [0, 1, 2, 3, 4, 5, 6, 7 ,8, 9])
    assert np.all(PlethData == [0, 1, 2, 3, 4, 5, 6, 7 ,8, 9])
