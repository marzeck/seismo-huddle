#!/usr/bin/env python

######################################################
### huddle test relative transfer function calculation
#
# name: huddle-test-T2.py
# author: Martin Zeckra
# mail: zeckra@uni-potsdam.de
#
# purpose:
# This script is used to calculate the relative
# transfer function of two seismometers in a huddle-test.
# Input are continuous seismic data of two close seismometers
# measuring hours of the same noise. Best results are
# achieved with a big earthquake during sensing period.
# The resulting relative transfer function is then written
# into a .txt-file. Here it is used for the Lennartz 3D/5s.
#
# after Lee, 1967, Statistical Theory of Communication:
# 'the input-output cross-power density spectrum of a
# linear system is the product of the system function
# [(transfer function)] and the input power density spectrum'
#
# the calculations base on Havskov 'Instrumentation in
# Earthquake Seismology', p. 293-294
#
######################################################

import os
from obspy import read
from obspy import UTCDateTime
from operator import truediv
from matplotlib.mlab import psd,csd
from obspy.signal.invsim import paz_to_freq_resp

datadir = './data_brazil/'

# define window around event in brazil (2019-01-05 19:25:35)
start = UTCDateTime('2019-01-05T19:00:00')
end = UTCDateTime('2019-01-05T20:59:59.99')

# load data
st = read(datadir + '*HHZ_2019-01-05*', starttime=start, endtime=end)

# create list of stations
stationList = list(set([tr.stats.station for tr in st.traces]))

# define PAZ values for transfer function
# example with Lennartz 3D/5s instruments
LEpoles = [(-0.888+0.888j), (-0.888-0.888j), (-0.29+0j)]
LEzeros = [0j, 0j, 0j]
LEscale = 400.0
sampfreq = 100.
nfft = 4096	
# maybe 4096 (adjust also in psd and csd) to get more long period spectrum

# calculate transfer function
T1 = paz_to_freq_resp(LEpoles, LEzeros, LEscale, 1.0/sampfreq, nfft, freq=True)

# iterate over each station combination

for stat1 in stationList:
	for stat2 in stationList:
		if stat1 == stat2:
			continue

		# select traces
		st1 = st.select(station=stat1)
		st2 = st.select(station=stat2)

		# calculate power spectral density and cross-spectrum
		P11 = psd(st1, Fs=sampfreq, NFFT=nfft)
		P21 = csd(st2,st1, Fs=sampfreq, NFFT=nfft)

		# derive quotient for transfer function estimation
		quot = map(truediv,P21[0],P11[0])

		# calculate second transferfunction
		T2calc = map(lambda x,y,z: (x*y)/z, T1[0], P21[0], P11[0])

		# output
		if not os.path.exists('transfer-functions'):
			os.mkdir('transfer-functions')

		with open('transfer-functions/T2-relative_{0}-to-{1}.txt'.format(stat1, stat2),'w') as f:
			for item in T2calc:
				f.write('{0}'.format(item))
				f.write('\n')




