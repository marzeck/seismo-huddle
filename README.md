# seismo-huddle
These files are used to perform a huddle test with seismometers. It's a relative calibration of the poles, zeroes and the Gain of the sensors. 

### Requirements
* [ObsPy](http://obspy.org)
* [dinver (from Geopsy package)] (http://www.geopsy.org/download.php)

### workflow

1.)
```
$ python huddle-test-T2.py
```
Calculates all relative transferfunctions of all seismometer combination of the huddle test. The estimated transfer function (based on Havskov Instrumentation in Earthquake Seismology', p. 293-294) will be stored in a .txt-file in a separate subfolder (here /transfer-functions). Adjust input and output names in file.

2.)
```
$ bash huddle-dinver-run.sh
```
(uses script "huddle-test-dinver.py)

A forward modeling of all given transferfunctions will be done wiht dinver. First, the python script "huddle-test-dinver.py" will be adjusted automatically. Second, the modelling will be done by executing dinver. All free parameters, which will be optimized are provided in the .dinver-file and can be changed in there (with the use of dinver). The communication between the python algorithm and the forward modelling of dinver is done via the files "parameters" and "misfit". They are automatically created and should not be changed during the calculations. The results (poles, zeroes, Gain, misfit) of each calculation step are stored in log files in the subfolder /misfits-log.

3.)
```
$ python sort-misfits.py
```
The log files of the forward modelling are sorted in ascending order by their misfits.

4.)
```
$ bash huddle-results.sh
```
The uppermost lines (the results of smallest misfit) of all given ordered log-files are stored separately in the file "huddle-results.txt"

5.)
```
$ python huddle-analysis.py
```
A small python script to plot all poles (imaginary over real part) derived by forward modelling and with smalles misfit.
