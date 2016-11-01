from heart_rate_monitoring import file_size


def test_filesize():

    matlab_size = file_size('test_filetypes.mat')
    h5py_size = file_size('test_filetypes_h5py.mat')
    binary_size = file_size('test1.bin')

    assert matlab_size == 22
    assert h5py_size == 22
    assert binary_size == 200000
