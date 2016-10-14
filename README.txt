This project, "Heart Rate Monitor", takes in binary files of multiplexed ECG and Pulse Plethysmography data and returns information including instantaneous heart rate, 1 minute and 5 minute average heart rate estimate, alarm detection of bradycardia and tachycardia, and a 10 minute trace log in the case of alarm.



How to Use:
 (code not fully functional)
1. Type main_HRmonitoring.py --file "name of binary file" to run code with binary file
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


Notes:
Peak detection still not refined and fully functional.