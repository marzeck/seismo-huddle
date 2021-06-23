#/bin/bash

####################################################
# 
# name: huddle-dinver-run.sh
# author: Martin Zeckra
# mail: zeckra@uni-potsdam.de
# 
# purpose:
# This bash-script is used to automatically run
# all relative seismometer transfer function 
# calculations with dinver. First, huddle-test-T2.py
# has to be run through to estimate the relative
# transfer functions. This script adjust the huddle-
# test-dinver.py file to correctly calculate the 
# forward transfer functions of all seismometer
# combinations. The parameter for dinver are stored
# in the .dinver-file.

####################################################

echo '####################################################################'
echo '\n run inversion on dinver for all provided seismometer combinations'
echo '####################################################################'

# get current working directory (new in Geopsy 3.4+)
cwd=$(pwd)

for file in transfer-functions/*; do
	fname=$(basename "$file")

	S1=${fname:12:3}
	S2=${fname:19:3}

	echo "run huddle test for station ${S1} and ${S2}"

	sed -i "28s/.*/with open('$cwd\/transfer-functions\/T2-relative_$S1-to-$S2.txt','r') as f:/" huddle-test-optimizer.py
	sed -i "70s/.*/if not os.path.exists('$cwd\/misfits-log'):/" huddle-test-optimizer.py
	sed -i "73s/.*/with open('$cwd\/misfits-log\/misfitslog-$S1-$S2.txt','a') as f:/" huddle-test-optimizer.py
	dinver -i DinverExt -optimization -target huddle-test.dinver -param huddle-test.dinver -f

	mkdir -p run-reports
	mv run.report run-reports/run.report-${S1}-${S2}

rm parameters
rm misfit

done


