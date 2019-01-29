#!/usr/bin/env python

######################################################
# 
# name: sort-misfits.py
# author: Martin Zeckra
# mail: zeckra@uni-potsdam.de
#
# purpose: 
# This script is used to sort all the misfitslogs 
# in ascending order by the misfit values.
# 
######################################################

import os
import glob

# find misfit files
ls = glob.glob('misfits-log/*.txt')

# check if output directory exists
if not os.path.exists('misfits-log/ordered'):
			os.mkdir('misfits-log/ordered')

for i in range(len(ls)):
	print(ls[i])

	# read misfit file as list of lines
	with open(ls[i],'r') as f:
		temp = f.read().split('\n')
	f.closed
	del temp[-1] #remove last element

	# separate list into array
	misfits = []
	for line in temp:
		misfits.append(line.split('\t'))

	# sort array by last column (misfit-values)
	misfits_sort = sorted(misfits, key=lambda mis: float(mis[3]))

	# write results into file
	with open('misfits-log/ordered/misfits-ordered-{0}-{1}.txt'.format(ls[i][23:26], ls[i][27:30]),'w') as f:
		for line in misfits_sort:
			if line[3] == ' nan ':
				continue
			f.write('{0}\t{1}\t{2}\t{3}'.format(line[0],line[1],line[2],line[3],))
			f.write('\n')
	f.closed

