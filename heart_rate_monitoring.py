from __future__ import division, print_function
import numpy as np

def read_data(filename):
    """ read in raw data from binary file inputted by user

    :param filename: filename = ""
    :returns: ECG Sampling Frequency, Pulse Plethysmograph Sampling Frequency, ECG sampling values array, Pulse Plethysmograph sampling values array """ 
    import numpy as np

    data = np.fromfile(filename, dtype = 'uint16')


    ECGAllData = np.array(data[0::2])
    PlethAllData = np.array(data[1::2])
    
    ECGSampFreqHz = ECGAllData[0]
    PlethSampFreqHz = PlethAllData[0]
    
    ECGData = np.array(data[2::2])
    PlethData = np.array(data[3::2])

    return ECGSampFreqHz, PlethSampFreqHz, ECGData, PlethData   



def heart_rate_indicies_ECG(ECGData):
    """ estimate indicies of ECG peaks
    
    :param signal: ECG sampling values array from read_data()
    :returns: indicies of peaks in ECG sampling values array
    """

    instantaneous_HR_indicies_ECG = detect_peaks(ECGData, show=False)

    return instantaneous_HR_indicies_ECG

    # instantaneous_HR_indicies_ECG = [] # Array which holds temporary values of heart rates as data is read
    # i=1
    # while i < ECGData.size-1:
    #     if ECGData[i] > ECGData[i-1] and ECGData[i] > ECGData[i+1]:
    #         instantaneous_HR_indicies_ECG.append(i)
    #     i+=1
    
    # return instantaneous_HR_indicies_ECG


def heart_rate_indicies_Plethysmograph(PlethData):
    """ estimate indicies of Plethysmograph peaks
    
    :param signal: Plethysmograph sampling values array from read_data()
    :returns: indicies of peaks in Plethysmograph sampling values array
    """

    instantaneous_HR_indicies_Pleth = detect_peaks(PlethData, show=False)

    return instantaneous_HR_indicies_Pleth

    # instantaneous_HR_indicies_Pleth = [] # Array which holds temporary values of heart rates as data is read
    # i=1
    # while i < PlethData.size-1:
    #     if PlethData[i] > PlethData[i-1] and PlethData[i] > PlethData[i+1]:
    #         instantaneous_HR_indicies_Pleth.append(i)
    #     i+=1
    
    # return instantaneous_HR_indicies_Pleth


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.
    
    __author__ = "Marcos Duarte, https://github.com/demotu/BMC"

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`
    
    The function can handle NaN's 
    """


    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help.
    
    __author__ = "Marcos Duarte, https://github.com/demotu/BMC"
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                    label='%d %s' % (ind.size, label))
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02*x.size, x.size*1.02-1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
        ax.set_xlabel('Data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        mode = 'Valley detection' if valley else 'Peak detection'
        ax.set_title("%s (mph=%s, mpd=%d, threshold=%s, edge='%s')"
                     % (mode, str(mph), mpd, str(threshold), edge))
        # plt.grid()
        plt.show()


def estimate_instantaneous_HR(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate instantaneous heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: instantaneous HR, alert, and 10 minute log of instantaneous heart rate
    """
    import numpy as np

    all_HR_Pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        instantaenous_HR_Pleth = ((60 * PlethSampFreqHz) / (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k])) # calculates instantaenous HR for each beat
        all_HR_Pleth.append(instantaenous_HR_Pleth)
        if instantaenous_HR_Pleth < 30: # detects for Bradycardia where heart rate is below 30 bpm
            invertedHR_Pleth = np.array(all_HR_Pleth[::-1])
            invertedHRseconds_Pleth = 1 / (invertedHR_Pleth / 60)
            HR_sum = 0
            for x in range(0, k):
                HR_sum_Pleth = HR_sum_Pleth + invertedHRseconds_Pleth[x]
                ten_min_invert_Pleth = invertedHR_Pleth[0:x]
                ten_min_real_Pleth = np.array(ten_min_invert_Pleth[::-1])
                if np.sum(ten_min_real_Pleth) > 600:
                    print("Bradycardia alert! Here is 10 minute trace of heart rate:")
                    return ten_min_real_Pleth
                    break
        elif instantaenous_HR_Pleth > 240: # detects for Bradycardia where heart rate is above 240 bpm
            invertedHR_Pleth = np.array(all_HR_Pleth[::-1])
            invertedHRseconds_Pleth = 1 / (invertedHR_Pleth / 60)
            HR_sum_Pleth = 0
            for x in range(0, k):
                HR_sum_Pleth = HR_sum_Pleth + invertedHRseconds_Pleth[x]
                ten_min_invert_Pleth = invertedHR_Pleth[0:x]
                ten_min_real_Pleth = np.array(ten_min_invert_Pleth[::-1])
                if np.sum(ten_min_real_Pleth) > 600:
                    print("Tachycardia alert! Here is 10 minute trace of heart rate:")
                    return ten_min_real_Pleth
                    break
        else:
            return all_HR_Pleth
        k+=1        

    
def estimate_heart_rate_oneminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate one minute average heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: one minute average heart rate
    """
    one_minute_HR_Pleth = []
    total_one_minute_HR_pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        time_between_beats_Pleth = (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k]) / PlethSampFreqHz
        one_minute_HR_Pleth.append(time_between_beats_Pleth)
        one_minute_HR_sum_Pleth = sum(one_minute_HR_Pleth)
        if one_minute_HR_sum_Pleth > 60:
            one_minute_total_HR_Pleth =  len(one_minute_HR_Pleth)
            total_one_minute_HR_pleth.append(one_minute_total_HR_Pleth)
            one_minute_HR_Pleth = []
            return total_one_minute_HR_pleth
        k+=1
    

def estimate_heart_rate_fiveminute_index(instantaneous_HR_indicies_Pleth, PlethSampFreqHz):
    """ estimate five minute average heart rate

    :param signal: input peak index values from heart_rate_indicies() and plethysmograph sampling frequency from read_data()
    :returns: five minute average heart rate
    """

    five_minute_HR_Pleth = []
    total_five_minute_HR_pleth = []
    k = 0
    while k < len(instantaneous_HR_indicies_Pleth)-1:
        time_between_beats_Pleth = (instantaneous_HR_indicies_Pleth[k+1] - instantaneous_HR_indicies_Pleth[k]) / PlethSampFreqHz
        five_minute_HR_Pleth.append(time_between_beats_Pleth)
        five_minute_HR_sum_Pleth = sum(five_minute_HR_Pleth)
        if five_minute_HR_sum_Pleth > 300:
            five_minute_total_HR_Pleth =  len(five_minute_HR_Pleth) / 5
            total_five_minute_HR_pleth.append(five_minute_total_HR_Pleth)
            five_minute_HR_Pleth = []
            return total_five_minute_HR_pleth
        k+=1

  