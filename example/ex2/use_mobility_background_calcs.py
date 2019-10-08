## Import relevant things
import numpy as np
import matplotlib.pyplot as plt
import mpmath
import os

# from pdata import *
import pdata as dat
import analytical_solutions as a_s


plt.figure(); plt.hold('on')

run = True
use_mobility = True
flux_function = 0.02334267

permeability = 1.0; viscosity = 1.0; density = 1.0;
filename_base = 'input1'
filename = filename_base+'_csv_pressure_0008.csv'
if run:
    if os.path.exists(filename):
        os.remove(filename)
dat.run_moose(input_file=filename_base,run_sim= run,
               flux_function_val = flux_function,permeability_val=permeability,
               viscosity_val=viscosity,density_val=density)
a_s.theis_solution(filename=filename,use_mobility = use_mobility,
                   flux_function = flux_function,permeability_val=permeability,
                   viscosity_val=viscosity,density_val=density)

permeability = 2.0; viscosity = 1.0; density = 1.0;
filename_base = 'input2'
filename = filename_base+'_csv_pressure_0008.csv'
if run:
    if os.path.exists(filename):
        os.remove(filename)
dat.run_moose(input_file=filename_base,run_sim= run,
               flux_function_val = flux_function,permeability_val=permeability,
               viscosity_val=viscosity,density_val=density)
a_s.theis_solution(filename=filename,use_mobility = use_mobility,
                   flux_function = flux_function,permeability_val=permeability,
                   viscosity_val=viscosity,density_val=density)


permeability = 1.0; viscosity = 3.0; density = 1.0;
filename_base = 'input3'
filename = filename_base+'_csv_pressure_0008.csv'
if run:
    if os.path.exists(filename):
        os.remove(filename)
dat.run_moose(input_file=filename_base,run_sim= run,
               flux_function_val = flux_function,permeability_val=permeability,
               viscosity_val=viscosity,density_val=density)
a_s.theis_solution(filename=filename,use_mobility = use_mobility,
                   flux_function = flux_function,permeability_val=permeability,
                   viscosity_val=viscosity,density_val=density)


permeability = 1.1; viscosity = 1.0; density = 4.0;
filename_base = 'input4'
filename = filename_base+'_csv_pressure_0008.csv'
if run:
    if os.path.exists(filename):
        os.remove(filename)
dat.run_moose(input_file=filename_base,run_sim= run,
               flux_function_val = flux_function,permeability_val=permeability,
               viscosity_val=viscosity,density_val=density)
a_s.theis_solution(filename=filename,use_mobility = use_mobility,
                   flux_function = flux_function,permeability_val=permeability,
                   viscosity_val=viscosity,density_val=density)


plt.legend([
            'k=1,mu=1,rho=1 analytical','k=1,mu=1,rho=1 numerical',
            'k=2,mu=1,rho=1 analytical','k=1,mu=1,rho=1 numerical',
            'k=1,mu=3,rho=1 analytical','k=1,mu=1,rho=1 numerical',
            'k=1.1,mu=1,rho=4 analytical','k=1,mu=1,rho=1 numerical',
            ])
plt.xlabel('distance from well(m)')
plt.ylabel('dP (Pa)')
plt.savefig('Permeability_PFSink.png')
plt.show()
