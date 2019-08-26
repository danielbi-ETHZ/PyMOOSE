# PyMOOSE
Serves as a python interface to write and run input files for MOOSE PorousFlow simulations.

### Getting Started
Ensure that you have installed MOOSE correctly and compiled the porous flow module executable.
Then set one of the following in your ~/.bashrc file so that PyMOOSE can find the excutable:
export MOOSE\_DIR=~/projects/moose
export POROUS\_FLOW\_DIR=~/projects/moose/modules/porous\_flow/

### Importing Python packages:
import pdata as dat
import analytical_solutions as a_s

### Example file
An example of how to run is shown in /example/example.py
