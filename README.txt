This project, "Heart Rate Monitor", takes in binary files of multiplexed ECG and Pulse Plethysmography data and returns information including instantaneous heart rate, 1 minute and 5 minute average heart rate estimate, alarm detection of bradycardia and tachycardia, and a 10 minute trace log in the case of alarm.



How to Use:
 (code not fully functional)
1. Save binary test file in same respository as main_HRmonitoring.py and heart_rate_monitoring.py

2. Write name of binary file in the quotations of read_data("") in the main_HRmonitoring.py file


3. Run main_HRmonitoring.py file in python with 'python main_HRmonitoring.py' command

Contributers:

Jaya Pokuri

Project License: 
See LICENSE.txt file

Packages Utilized:
1. 
numpy - utilize MATLAB commands and features in the python environment
2. time - handles date and time and allows for implementing time delays
3. threading - allows for running multiple operations in the same process space


Notes:
Had trouble reading in binary file so read_data() might not be fully operational. Also, didn't implement code in some ways lacks robustness and will not work adequately on all inputed files.