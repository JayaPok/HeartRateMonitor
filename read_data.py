def read_data(filename = "test.bin"):
    """ read in raw data from binary file

    :param filename: default = ""
    :returns: """ 
    import numpy as np
    Freqs = np.fromfile(filename, dtype = 'uint16')

    ECGData = np.array(Freqs[::2])
    PlethData = np.array(Freqs[1::2])
    
    ECGSampFreqHz = ECGData[0]
    PlethSampFreqHz = PlethData[0]

    return Freqs


with open('test.bin', 'rb') as filename:
    import numpy as np
    Freqs = np.fromfile(filename, dtype = 'uint16')
    print(Freqs)

    ECGData = np.array(Freqs[::2])
    PlethData = np.array(Freqs[1::2])
    print(ECGData)
    print(PlethData)
    
    ECGSampFreqHz = ECGData[0]
    PlethSampFreqHz = PlethData[0]
    print(ECGSampFreqHz)
    print(PlethSampFreqHz)
