## PyMOOSEFramework

import numpy as np
import matplotlib.pyplot as plt
import mpmath
import os

# def run_moose(input_file = 'simple_theis.i', np = None, executable_loc = None,run_sim = True):
#     if np == None:
#         np = 4
#     if executable_loc == None:
#         try:
#             porous_flow_dir = os.environ['POROUS_FLOW_DIR']
#             executable_loc=porous_flow_dir+'/porous_flow-opt'
#         except:
#             print('Must specifiy POROUS_FLOW_DIR')
#     command = 'mpirun -np '+str(np)+' '+executable_loc+' -i '+str(object=input_file)
#     if run_sim:
#         os.system(command)

def run_moose(input_file = 'input.i', np = None, executable_loc = None,
               run_sim = True,flux_function_val=None,
               template_file = 'template.i',
               flux_function_placeholder='flux_function_placeholder',
               permeability_val = None,viscosity_val = None,
               density_val = None):
    if flux_function_val == None:
        flux_function_val = -0.233426704015
    if permeability_val == None:
        permeability_val = 1.0
    if viscosity_val == None:
        viscosity_val = 1.0
    if density_val == None:
        density_val = 1.0
    permeability_placeholder = 'permeability_placeholder'
    viscosity_placeholder = 'viscosity_placeholder'
    density_placeholder = 'density_placeholder'

    ## Look for flux_function_placeholder (str) in the input file and replace with flux_function_val (float)
    fin = open(template_file,'rt')
    fout = open(input_file,'wt')

    for line in fin:
        if permeability_placeholder in line:
            fout.write(line.replace(permeability_placeholder,str(permeability_val)))
        elif flux_function_placeholder in line:
            fout.write(line.replace(flux_function_placeholder,str(flux_function_val)))
        elif viscosity_placeholder in line:
            fout.write(line.replace(viscosity_placeholder,str(viscosity_val)))
        else:
            fout.write(line.replace(density_placeholder,str(density_val)))
    fin.close()
    fout.close()

    if np == None:
        np = 4
    if executable_loc == None:
        try:
            porous_flow_dir = os.environ['POROUS_FLOW_DIR']
            executable_loc=porous_flow_dir+'porous_flow-opt'
        except:
            try:
                moose_dir = os.environ['MOOSE_DIR']
                executable_loc=porous_flow_dir+'/modules/porous_flow/porous_flow-opt'
            except:
                print('Must specifiy POROUS_FLOW_DIR or MOOSE_DIR in ~/.bashrc profile')
    command = 'mpirun -np '+str(np)+' '+executable_loc+' -i '+str(object=input_file)
    if run_sim:
        os.system(command)
