# Attack Analysis Tests
Attack analysis tests is a file that makes use of python unit tests to assert that the attack methods analysed within capture_analysis work as expected. Packets are provided to this file using .pcap files, as this file's main goal is to test the analysis of the packets works as expected, not to test the capturing of packets.

## Dependencies
```
import unittest
import matplotlib
matplotlib.use('Agg')
from pythonGUI.capture_analysis import attack_detection, GUI_actions
```
Attack analysis tests imports the following libraries and code:
 - unittest - The python framework for implementing unit tests
 - matplotlib - An object-oriented plotting library used to visualise the tests
   - .use('Agg') - Select the interactive backend implementation of matplotlib for GUI integration
 - from pythonGUI.capture_analysis import attack_detection, GUI_actions - Import dependencies from other parts of the program to execute the attack analyses