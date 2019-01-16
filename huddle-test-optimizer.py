#!/usr/bin/env python

######################################################
### huddle test dinver transfer script
# 
# name: huddle-test-dinver.py
# author: Martin Zeckra
# mail: zeckra@uni-potsdam.de
#
# purpose: 
# This script is used to estimate the misfit between
# the calculated relative transfer function of two
# seismometers and their hypothetical transfer function
# calculated from the poles & zeroes given by the 
# manufacturer. Input and Output will be further analysed
# by dinver (Geopsy) and this script does the forward 
# calculations. Output will be saved in misfits.txt
# (delete file before each run in dinver.
# Here it is used for the Lennartz 3D/5s.
# 
######################################################

import os
import math
from obspy.signal.invsim import paz_to_freq_resp

# read out calculated transfer function
with open('transfer-functions/T2-relative_A2M-to-A2K.txt','r') as f:
	temp = f.read().split('\n')
	f.closed
del temp[-1] #remove last element
# convert list of strings into list of complex numbers
T2calc = []
T2calc = map(complex,temp)


temp = []
with open('parameters','r') as f:
	temp = f.read().split('\n')
	f.closed
del temp[-1]

# define gain
LEscale = float(temp[3])

#define poles
LEpoles = [complex(float(temp[0]),float(temp[1])), complex(float(temp[0]),-float(temp[1])), complex(float(temp[2]),0)]

## define additional PAZ values for transfer function
LEzeros = [0j, 0j, 0j]
sampfreq = 100.
nfft = 4096

## simulate second transferfunction

T2sim = paz_to_freq_resp(LEpoles, LEzeros, LEscale, 1.0/sampfreq, nfft, freq=True)

# only analyze below 5 HZ
thr = len(filter(lambda x: x<5,T2sim[1])) - 1

# misfit determination by complex L2-Norm 
misfit = math.sqrt(sum(((T2sim[0][0:thr] - T2calc[0:thr])*(T2sim[0][0:thr] - T2calc[0:thr]).conjugate()).real))

#print(misfit)
with open('misfit','w') as f:
	f.write('{}'.format(misfit))

if not os.path.exists('misfits-log'):
	os.mkdir('misfits-log')

with open('misfits-log/misfitslog-A2M-A2K.txt','a') as f:
	f.write('{0} \t {1} \t {2} \t {3} \n'.format(LEpoles, LEzeros, LEscale, misfit))

r = [math.sqrt((T2sim[0][i] - T2calc[i]).real**2+(T2sim[0][i] - T2calc[i]).imag**2) for i in range(0,thr)]





