## This example shows how to write and run an input file using PyMOOSE.
## The result is then compared to an analytical solution.

## Import relevant things
import numpy as np
import matplotlib.pyplot as plt
import mpmath
import os
import pdata as dat
import analytical_solutions as a_s

## Initialize plot
plt.figure(); plt.hold('on')

## Set options for the functions
run = True
use_mobility = True
flux_function = 0.02334267

filename_base = 'input1' #specifies the input file name
filename = filename_base+'_csv_pressure_0008.csv' #points to the output data, which can be compared to analytical solution
if run:
    if os.path.exists(filename):
        os.remove(filename)
dat.run_moose2(input_file=filename_base,run_sim= run,
               flux_function_val = flux_function)
a_s.theis_solution(k=1.,filename=filename,use_mobility = use_mobility,
                   flux_function = flux_function)

plt.legend([
            'k=1 analytical','k=1 numerical',
            ])
plt.xlabel('distance from well(m)')
plt.ylabel('dP (Pa)')
plt.savefig('Permeability_PFSink.png')
plt.show()
