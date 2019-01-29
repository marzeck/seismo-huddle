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

import matplotlib.pyplot as plt
from matplotlib import patches

###### change if necessary in here:

# theoretical poles and zeroes
THpoles = [complex(-0.888+0.888j), complex(-0.888-0.888j), complex(-0.29+0j)]
THzeros = [complex(0j), complex(0j), complex(0j)]

# higlight specific station (or None)
highl = None
#highl = 'AAC'

###### processing

# read data
with open('huddle-results.txt','r') as f:
	temp = f.read().splitlines()
f.closed

# remove header
del temp[0]

# translate to proper objects
results = []
for line in temp:
	results.append([
		line.split()[0],
		line.split()[1],
		[complex(item.strip('[](),')) for item in line.split()[2:5]],
		[complex(item.strip('[](),')) for item in line.split()[5:8]],
		float(line.split()[8]),
		float(line.split()[9])])

# combine all plots and zooms
unit_circle = patches.Circle(
	(0,0),
	radius=1,
	fill=False,
	color='black',
	ls='solid',
	alpha=0.1)

# raw plot
fig = plt.figure()
ax1 = plt.subplot(221)
for j in results:
	if j[0] == highl or j[1] == highl and highl is not None:
		[ax1.scatter(j[2][i].real, j[2][i].imag, color='red') for i in range(0,3)]
	else:
		[ax1.scatter(j[2][i].real, j[2][i].imag, color='blue') for i in range(0,3)]
ax1.scatter(THpoles[0].real, THpoles[0].imag, color='green', marker='D')
ax1.scatter(THpoles[1].real, THpoles[1].imag, color='green', marker='D')
ax1.scatter(THpoles[2].real, THpoles[2].imag, color='green', marker='D')
ax1.axis('tight')
ax1.set_aspect('equal', adjustable='box')
ax1.grid(True, color='0.9', linestyle='-', which='both', axis='both')
ax1.add_patch(unit_circle)
ax1.axvline(0, color='black', alpha=0.1)
ax1.axhline(0, color='black', alpha=0.1)
ax1.set_xlim([-1.1, 1.1])
ax1.set_ylim([-1.1, 1.1])
ax1.set_xlabel('real part')
ax1.set_ylabel('imaginary part')
ax1.set_title('whole plane')

# zoom for positive imaginary part
ax2 = plt.subplot(222)
for j in results:
	if j[0] == highl or j[1] == highl and highl is not None:
		ax2.scatter(j[2][0].real, j[2][0].imag, color='red')
	else:
		ax2.scatter(j[2][0].real, j[2][0].imag, color='blue')
ax2.scatter(THpoles[0].real, THpoles[0].imag, color='green',marker='D')
ax2.set_aspect('equal', adjustable='box')
ax2.set_xlim([-1,-0.7])
ax2.set_ylim([0.7,1.05])
ax2.set_xlabel('real part')
ax2.set_ylabel('imaginary part')
ax2.grid(True, color='0.9', linestyle='-', which='both', axis='both')
ax2.set_title('first pole')

# zoom for negative imaginary part
ax3 = plt.subplot(223)
for j in results:
	if j[0] == highl or j[1] == highl and highl is not None:
		ax3.scatter(j[2][1].real, j[2][1].imag, color='red')
	else:
		ax3.scatter(j[2][1].real, j[2][1].imag, color='blue')
ax3.scatter(THpoles[1].real, THpoles[1].imag, color='green',marker='D')
ax3.set_aspect('equal', adjustable='box')
ax3.set_xlim([-1,-0.7])
ax3.set_ylim([-1.05,-0.7])
ax3.set_xlabel('real part')
ax3.set_ylabel('imaginary part')
ax3.grid(True, color='0.9', linestyle='-', which='both', axis='both')
ax3.set_title('second pole')

# zoom for third pole (imaginary part = 0)
ax4 = plt.subplot(224)
for j in results:
	if j[0] == highl or j[1] == highl and highl is not None:
		ax4.scatter(j[2][2].real, j[2][2].imag, color='red')
	else:
		ax4.scatter(j[2][2].real, j[2][2].imag, color='blue')
ax4.scatter(THpoles[2].real, THpoles[2].imag, color='green',marker='D')
ax4.set_aspect('equal', adjustable='box')
ax4.set_xlim([-0.8,0])
ax4.set_ylim([-0.4,0.4])
ax4.set_xlabel('real part')
ax4.set_ylabel('imaginary part')
ax4.grid(True, color='0.9', linestyle='-', which='both', axis='both')
ax4.set_title('third pole')

plt.tight_layout()
plt.suptitle('best fitted poles - huddle test')
plt.savefig('resulting-poles.png', dpi=300, format='png')
#plt.show()




