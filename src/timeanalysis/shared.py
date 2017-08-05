import numpy as np

def outliers_std(data, m=2):
    # https://stackoverflow.com/a/11686764
    return abs(data - np.mean(data)) < m * np.std(data)

def reject_outliers_std(data, m=2):
    return data[outliers_std(data, m)]

def outliers_median(data, m=2):
    # https://stackoverflow.com/a/16562028
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return s < m

def reject_outliers_median(data, m=2):
    return data[outliers_median(data, m)]

def outliers_iqr(data, iq_range=0.5):
    # https://stackoverflow.com/a/39424972
    pcnt = (1 - iq_range) / 2.0 * 100
    qlow, median, qhigh = np.percentile(data, [pcnt, 50, 100 - pcnt])
    iqr = qhigh - qlow
    return np.absolute(data - median) < iqr

def reject_outliers_iqr(data, iq_range=0.5):
    return data[reject_outliers_iqr(data, iq_range)]

