import numpy as np

def reject_outliers_std(data, m=2):
    # https://stackoverflow.com/a/11686764
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def reject_outliers_median(data, m=2):
    # https://stackoverflow.com/a/16562028
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]

def reject_outliers_iqr(data, iq_range=0.5):
    # https://stackoverflow.com/a/39424972
    pcnt = (1 - iq_range) / 2.0 * 100
    qlow, median, qhigh = np.percentile(data, [pcnt, 50, 100 - pcnt])
    iqr = qhigh - qlow
    return data[np.absolute(data - median) <= iqr]

