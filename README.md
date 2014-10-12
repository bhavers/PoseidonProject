# PoseidonProject

##Introduction
Poseidon aims to reduce the overuse of fresh water in the world.
The objective of the first iteration of Poseidon is to:
- Develop a water monitoring solution for educational purposes.
- Deliver education material for building the solution
- Build and support a community of cross discipline enthusiasts (scientists, hydrologists, agriculture experts, application developers, hardware experts, etc)
 
The project uses a Raspberry Pi with soil moisture and barometer sensors. The data is submitted to
Bluemix, a cloud platform (Platform as a Service), for process by application.
The code in this repository provides the Python script that will be running on the Pi.

##Usage
Important files:
- Tutorial1/config.py: your configuration settings, add to .gitignore
- Tutorial1/PoseidonClient.py: the main script to execute
- Tutorial1/poseidon.sh: script for starting/stopping PoseidonClient.py

See the files for instructions.

##License 
The code is licensed under the Apache v2 open source license, see License.txt. 
Poseidon is a project of the Dutch Courage foundation, http://dutchcourage.org/

## External dependencies
The code is dependent on the following external libraries:
- tbd...