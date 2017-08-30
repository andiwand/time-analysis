import numpy as np
import itertools

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

def read_table(path, t=float):
    with open(path, "r") as f:
        data = [list(map(t, line.split(" "))) for line in f.readlines()[:-1]]
    return data

def write_table(data, path, fm="%.9f"):
    with open(path, "w") as f:
        for d in data:
            f.write(" ".join([fm % e for e in d]))
            f.write("\n")

def map_table(data, m):
    return [list(map(m, d)) for d in data]

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

