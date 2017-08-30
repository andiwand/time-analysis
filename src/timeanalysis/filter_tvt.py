#!/usr/bin/env python3

import os
import argparse
from collections import deque
import decimal
import numpy as np
import pandas as pd
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import shared

parser = argparse.ArgumentParser()
parser.add_argument("file_in", help="path to input file")
parser.add_argument("file_out", help="path to output file")
parser.add_argument("-x", "--subtract-x", help="transform y=y-x", action="store_true")
parser.add_argument("-o", "--offset-x", help="x offset", type=decimal.Decimal, default=0)
parser.add_argument("--crop", help="crop input data", type=int)
parser.add_argument("--moving-avg", help="use moving average", action="store_true")
parser.add_argument("--remove-x", help="remove x data", action="store_true")
parser.add_argument("--moving-window", help="windows size for moving avg/std", type=int, default=100)
parser.add_argument("--fft", help="fourier transform", action="store_true")
parser.add_argument("--ifft", help="inverse fourier transform", action="store_true")
parser.add_argument("--fit", help="polynomial fit", action="store_true")
parser.add_argument("--fit-deg", help="degree of the fitting polynomial", type=int, default=2)
parser.add_argument("--fit-ref", help="path to reference file")
parser.add_argument("--fit-ref-offset", help="reference offset", type=float)
parser.add_argument("--fit-ref-std", help="reference standard deviation", type=float)
parser.add_argument("--fit-window", help="windows size for polynomial fit", type=int, default=10)
parser.add_argument("--fit-cut", help="polynomial fit cut-off condition", type=float, default=1.5)
args = parser.parse_args()

data = shared.read_table(args.file_in, t=decimal.Decimal)

if args.crop:
    data = data[:args.crop]

if args.subtract_x:
    for d in data:
        d[1] = d[1] - d[0]

if args.offset_x:
    for d in data:
        d[0] = d[0] - args.offset_x
    #while data[0][0] < 0:
    #    data = data[1:]

data = np.array(shared.map_table(data, float))

if args.moving_avg:
    #df = pd.DataFrame(data)
    #rdf = df.rolling(args.window_size)
    #data = rdf.mean().values
    s = pd.Series(data[:,1])
    rs = s.rolling(args.moving_window, center=True)
    avg_data = rs.mean().values
    #data = np.column_stack([data[:,0], avg_data])
    data[:,1] = avg_data
    data = data[args.moving_window//2:]

if args.fft:
    dt = np.mean(data[1:,0] - data[:-1,0])
    n = len(data)
    data = np.fft.rfft(data[:,-1])
    data = np.column_stack([np.fft.rfftfreq(n, d=dt), data.real, data.imag])

if args.ifft:
    df = data[1,0] - data[0,0]
    data = np.fft.irfft(data[:,-2] + 1j * data[:,-1])
    dt = 1 / (len(data) * df)
    start = args.offset_x
    end = args.offset_x + len(data) * dt
    data = np.column_stack([np.linspace(start, end, num=len(data)), data])

if args.fit:
    if args.fit_ref:
        ref_data = np.array(shared.read_table(args.fit_ref))
        args.fit_ref_offset = np.mean(ref_data[:,1])
        args.fit_ref_std = np.std(ref_data[:,1])
    polys = []
    start = 0
    end = args.fit_window
    while True:
        sub = data[start:end]
        r = np.polyfit(sub[:,0], sub[:,1], args.fit_deg, full=True)
        std = (r[1][0] / (len(sub) - 1)) ** 0.5
        if std > args.fit_ref_std * args.fit_cut:
            polys.append((sub[0,0], sub[-1,0], r[0]))
            start = end - 1
        if end == len(data):
            polys.append((sub[0,0], sub[-1,0], r[0]))
            break
        end = min(end + args.fit_window, len(data))
    print(len(polys))
    polyi = iter(polys)
    poly = next(polyi)
    for i, x in enumerate(data[:,0]):
        if x > poly[1]: poly = next(polyi)
        data[i,1] = np.polyval(poly[2], x)

if args.remove_x:
    data = data[:,1:]

shared.write_table(data, args.file_out)

