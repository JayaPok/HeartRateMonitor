This project, "Heart Rate Monitor", takes in binary files of multiplexed ECG and Pulse Plethysmography data and returns information including instantaneous heart rate, 1 minute and 5 minute average heart rate estimate, alarm detection of bradycardia and tachycardia, and a 10 minute trace log in the case of alarm.



How to Use:
1. Type main_HRmonitoring.py --file "name of binary/matlab/HDF5 file" to run code with binary file

2. Can additionaly type --brady (number) --tachy (number) --signal ('ECG', 'PLETH', or 'BOTH') 
--usermin (number) for additional user inputs to change threshold of bradycardia, tachycardia, type of signal, 
and custom minute average heart rate value

Contributers:

Jaya Pokuri

Project License: 
See LICENSE.txt file

Packages Utilized:
1. 
numpy - utilize MATLAB commands and features in the python environment

2. collections - implement argpars into methods and python environment

3. os - allows for reading length of binary file

4. logging - allows for logging information with timestamps to another file

5. scipy.io - allows for reading matlab (.mat) files

6. h5py - allows for reading HDF5 files

7. sys - allows for exiting out of lab
