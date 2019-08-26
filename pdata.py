## PyMOOSEFramework

import numpy as np
import matplotlib.pyplot as plt
import mpmath
import os

def run_moose(input_file = 'simple_theis.i', np = None, executable_loc = None,run_sim = True):
    if np == None:
        np = 4
    if executable_loc == None:
        try:
            porous_flow_dir = os.environ['POROUS_FLOW_DIR']
            executable_loc=porous_flow_dir+'/porous_flow-opt'
        except:
            print 'Must specifiy POROUS_FLOW_DIR'
    command = 'mpirun -np '+str(np)+' '+executable_loc+' -i '+str(object=input_file)
    if run_sim:
        os.system(command)




def run_moose2(input_file = 'input.i', np = None, executable_loc = None,
               run_sim = True,flux_function_val=None,
               template_file = 'template.i',
               flux_function_placeholder='flux_function_placeholder'):
    if flux_function_val == None:
        flux_function_val = -0.233426704015
    ## Look for flux_function_placeholder (str) in the input file and replace with flux_function_val (float)
    fin = open(template_file,'rt')
    fout = open(input_file,'wt')
    for line in fin:
        fout.write(line.replace(flux_function_placeholder,str(flux_function_val)))
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
                print 'Must specifiy POROUS_FLOW_DIR or MOOSE_DIR in ~/.bashrc profile'
    command = 'mpirun -np '+str(np)+' '+executable_loc+' -i '+str(object=input_file)
    if run_sim:
        os.system(command)
