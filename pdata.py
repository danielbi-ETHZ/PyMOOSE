## PyMOOSEFramework

import numpy as np
import matplotlib.pyplot as plt
import mpmath
import os
try:
    from __future__ import print_function
except ModuleNotFoundError:
    pass

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
               temp_ic = None, temp_bc = None,
               template_file = 'template.i',
               flux_function_placeholder='flux_function_placeholder',
               permeability_val = None,permeability2 = None,
               porosity = None, porosity2 = None, viscosity_val = None,
               density_val = None, bulk_modulus_val = None,
               thermal_expansion_val = None, use_mobility = None,
               lambda_f = None, lambda_s = None,
               mesh_file = None, start_time = None, end_time = None):
    """
    mesh_file - path the mesh file (str)
    start_time is restart time in [Executioner] (float)
    end_time is the end_time in [Executioner] (float)
    lambda_f is the fluid thermal conductivity
    lambda_s is the solid thermal conductivity
    """
    if flux_function_val == None:
        flux_function_val = -0.233426704015
        print('# WARNING: no flux_function_val was provided to run_mosse')
    if temp_ic == None:
        temp_ic = 293.15
        print('# WARNING: no temp_ic was provided to run_moose')
    if temp_bc == None:
        temp_bc = 293.15
        print('# WARNING: no temp_bc was provided to run_mosse')
    if permeability_val == None:
        permeability_val = 1.0;
        print('# WARNING: no permeability_val was provided to run_moose')
    if permeability2 == None:
        permeability2 = 1.0;
        print('# WARNING: no permeability value was provided to second mateiral')
    if porosity == None:
        porosity = 1.0;
        print('# WARNING: no porosity was provided to run_moose')
    if porosity2 == None:
        porosity2 = 1.0;
        print('# WARNING: no porosity2 was provided to run_moose')
    if viscosity_val == None:
        viscosity_val = 1.0;
        print('# WARNING: no viscosity_val was provided to run_mosse')
    if density_val == None:
        density_val = 1.0
        print('# WARNING: no density_val was provided to run_mosse')
    if bulk_modulus_val == None:
        bulk_modulus_val = 1./4.4e-10 #Pa
        print('# WARNING: no bulk_modulus_val was provided to run_mosse')
    if thermal_expansion_val == None:
        thermal_expansion_val = 0.0
        print('# WARNING: no thermal_expansion_val was provided to run_mosse')
    if lambda_f == None:
        lambda_f = 0.6; #W/m - K
        print('# WARNING: no lambda_f was provided to run_mosse')
    if lambda_s == None:
        lambda_s = 2.8; # W/m-K
        print('# WARNING: no lambda_s was provided to run_mosse')
    if use_mobility == None:
        use_mobility = False
        print('# WARNING: no use_mobility was provided to run_mosse')
    if mesh_file == None:
        mesh_file = 'mesh.e'
        print('# WARNING: no mesh_file was provided to run_mosse')

    if start_time == None:
        start_time = 0.0
    else:
        if mesh_file == None:
            print('# Error: provid mesh file for restart')
            lakjfsdlkajdflkj
    if end_time == None:
        end_time = 365.25*24.*60.*60. # seconds
        print('# WARNING: no end_time provided')
    temp_ic_placeholder  = 'temp_ic_placeholder'
    temp_bc_placeholder  = 'temp_bc_placeholder'
    permeability_placeholder = 'permeability_placeholder'
    permeability2_placeholder = 'permeability2_placeholder'
    porosity_placeholder = 'porosity_placeholder'
    porosity2_placeholder = 'porosity2_placeholder'
    viscosity_placeholder = 'viscosity_placeholder'
    density_placeholder = 'density_placeholder'
    bulk_modulus_placeholder = 'bulk_modulus_placeholder'
    thermal_expansion_placeholder = 'thermal_expansion_placeholder'
    lambda_f_placeholder = 'lambda_f_placeholder'
    lambda_s_placeholder = 'lambda_s_placeholder'
    use_mobility_placeholder = 'use_mobility_placeholder'
    mesh_file_placeholder = 'mesh_file_placeholder'
    start_time_placeholder = 'start_time_placeholder'
    end_time_placeholder = 'end_time_placeholder'

    ## Look for flux_function_placeholder (str) in the input file and replace with flux_function_val (float)
    fin = open(template_file,'rt')
    fout = open(input_file,'wt')

    for line in fin:
        if temp_ic_placeholder in line:
            fout.write(line.replace(temp_ic_placeholder,str(temp_ic)))
        elif temp_bc_placeholder in line:
            fout.write(line.replace(temp_bc_placeholder,str(temp_bc)))
        elif permeability_placeholder in line:
            fout.write(line.replace(permeability_placeholder,str(permeability_val)))
        elif permeability2_placeholder  in line:
            fout.write(line.replace(permeability2_placeholder,str(permeability2)))
        elif porosity_placeholder in line:
            fout.write(line.replace(porosity_placeholder,str(porosity)))
        elif porosity2_placeholder in line:
            fout.write(line.replace(porosity2_placeholder,str(porosity2)))
        elif flux_function_placeholder in line:
            fout.write(line.replace(flux_function_placeholder,str(flux_function_val)))
        elif viscosity_placeholder in line:
            fout.write(line.replace(viscosity_placeholder,str(viscosity_val)))
        elif use_mobility_placeholder in line:
            fout.write(line.replace(use_mobility_placeholder,str(use_mobility)))
        elif bulk_modulus_placeholder in line:
            fout.write(line.replace(bulk_modulus_placeholder,str(bulk_modulus_val)))

        elif lambda_s_placeholder in line:
            fout.write(line.replace(lambda_s_placeholder,str(lambda_s)))
        elif lambda_f_placeholder in line:
            fout.write(line.replace(lambda_f_placeholder,str(lambda_f)))

        elif thermal_expansion_placeholder in line:
            fout.write(line.replace(thermal_expansion_placeholder,str(thermal_expansion_val)))
        elif start_time_placeholder in line:
            fout.write(line.replace(start_time_placeholder,str(start_time)))
        elif end_time_placeholder in line:
            fout.write(line.replace(end_time_placeholder,str(end_time)))
        elif mesh_file_placeholder in line:
            fout.write(line.replace(mesh_file_placeholder,mesh_file))
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



def flux_function_from_Qv(use_mobility = None, Qv = None, viscosity = None,
                          permeability = None, boundary_area = None,
                          density = None):
    if use_mobility == None:
        use_mobility = True
    if Qv == None:
        Qv = 1.0 #volumetric flow rate (m3/s) that is desired at boundary
    if viscosity == None:
        viscosity = 1.e-3
    if permeability == None:
        permeability = 1.e-12
    if boundary_area == None:
        boundary_area = 1.0 #are of the boundary coundition
    if density == None:
        density = 1000. # fluid density
    if use_mobility:
        flux_function = Qv*viscosity/boundary_area/permeability;
    else:
        flux_function = Qv*density/boundary_area;
    return flux_function

def calc_density0(rho_at_P0_T0 = None, P0=None, bulk_modulus = None,
                  thermal_expansion = None,T0 = None):
    """
    This function calculates density0 for SimpleFluidProperties
    based on a desired density at reference pressure and temp: rho_at_P0_T0
        where P0 is the reference pressure
        where T0 is the reference temperature
        where bulk_modulus and thermal_expansion are from SimpleFluidProperties
    """
    import numpy as np
    if rho_at_P0_T0 == None:
        rho_at_P0_T0 = 1000.; # kg/m3
    if P0 == None:
        P0 = 0.0 # Pa
    if T0 == None:
        T0 = 0.0
    if bulk_modulus == None:
        bulk_modulus = 1./4.4e-10 #Pa^-1
    if thermal_expansion == None:
        thermal_expansion = 0.0
    density0 = rho_at_P0_T0/np.exp(P0/bulk_modulus - thermal_expansion*T0)
    return density0
