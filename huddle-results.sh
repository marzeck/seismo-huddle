#/bin/bash

####################################################
# 
# name: huddle-results.sh
# author: Martin Zeckra
# mail: zeckra@uni-potsdam.de
# 
# purpose:
# This bash-script is used to extract the poles, 
# zeros and Gain of the huddle inversion with the
# lowest misfit and write it to one file.
# 
####################################################

echo '# S1, S2, poles (1, 2, 3), zeroes (1, 2, 3), Gain, best misfit' > huddle-results.txt

for file in misfits-log/ordered/*; do
	fname=$(basename "$file")
	S1=${fname:16:3}
	S2=${fname:20:3}
	line=$(head -n 1 misfits-log/ordered/$fname)
	echo $S1 $S2 $line >> huddle-results.txt

done 
