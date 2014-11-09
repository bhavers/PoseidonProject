# PoseidonProject - Tutorial 1

##Introduction
PoseidonClient: contains the client for the Raspberry Pi
NodeRed: the flow to be pasted in Nodered

##Usage
Important files:
- PoseidonClient/config.py: your configuration settings, add to .gitignore
- PoseidonClient/PoseidonClient.py: the main script to execute
- PoseidonClient/poseidon.sh: script for starting/stopping PoseidonClient.py

See the files for instructions.

##License 
The code is licensed under the Apache v2 open source license, see License.txt. 
Poseidon is a project of the Dutch Courage foundation, http://dutchcourage.org/

## External dependencies
- Setup GrovePi by cloning the git repository: https://github.com/DexterInd/GrovePi 
- Execute install.sh (as root) from GrovePi git foldder /Script/
- Copy grovepi.py and grove_barometer_lib.py from GrovePi fit folder Script/Python to PoseidonClient