def theis_solution(permeability_val=None,density_val=None,viscosity_val=None,
                   filename=None,use_mobility=None,
                   flux_function = None, b = None, well_area = None, Kw = None,
                   phi = None, t_end = None, z_plot_loc = None, fixed_axis = None,
                   pp_loc = None,P0 = None, symmetry = True):
    import numpy as np
    import matplotlib.pyplot as plt
    import mpmath
    import os
    if filename == None:
        filename = 'simple_theis_k1_csv_pressure_0009.csv'
    if permeability_val == None:
        permeability_val = 1.0 # m2
    if density_val == None:
        density_val = 1.0; #kg/m3
    if viscosity_val == None:
        viscosity_val = 1.0; #Pa-s
    if flux_function == None:
        flux_function = -0.233426704015
    if b == None:
        b = 1.0; # aquifer thickness (m)
    if Kw == None:
        Kw = 1.0 # compressibility of water (Pa^-1)
    if phi == None:
        phi = 0.1 # porosity
    if t_end == None:
        t_end = 100.0; #seconds
    if use_mobility == None:
        use_mobility = False
    if z_plot_loc == None:
        z_plot_loc = -199.77360637445
    if fixed_axis == None:
        fixed_axis = 2 # integer telling which axis should be fixed (x = 0, y = 1, z = 2)
    if pp_loc == None:
        pp_loc = -1 #integer to tell where the pore pressure is found in csv file
    if P0 == None:
        P0 = 0.
    if well_area == None:
        dx = 1.07131; dy = 1.0; #meters
        well_area = dx*dy; # well area (m2)
        print 'well_area ', well_area

    ## Calculations

    if use_mobility:
        Qm = -flux_function*density_val*permeability_val/viscosity_val*well_area
    else:
        Qm = -flux_function*well_area
    print 'Mass flow rate in (i.e. fluxes_in expected)', Qm

    ignore_density = False #Always False if use_mobility = False. Maybe also if use_mobility = True??
    if ignore_density:
        Q = Qm
    else:
        Q = Qm/density_val
    print 'volumetric flow rate (checked against Theis)', Q

    ## Calculate the analytical solution my way
    import pudb; pudb.set_trace()
    if symmetry:
        prefactor = 4.0*Q*viscosity_val/(4.0*np.pi*b*permeability_val) # Pa, multiplier of exponential integral, 4.0 factor is because of 1/4 grid symmetry
    else:
        prefactor = Q*viscosity_val/(4.0*np.pi*b*permeability_val) # Pa, multiplier of exponential integral, 4.0 factor is because of 1/4 grid symmetry
    r_anal = np.linspace(1,200,101); #radius in meters
    dP_anal = np.zeros(len(r_anal))
    u = (r_anal**2.0)*phi*viscosity_val/(4.0*permeability_val*t_end*Kw)
    for i in xrange(0,len(u)):
        dP_anal[i] = prefactor*mpmath.e1(u[i])


    plt.plot(r_anal,dP_anal)

    x = np.zeros(40)
    pp = np.zeros(40);
    import csv
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                junkvar = 1
                line_count += 1
            else:
                if float(row[fixed_axis]) > z_plot_loc-.1 and float(row[fixed_axis]) <  z_plot_loc+.1 and float(row[0])>0:
                    x[line_count-1] = float(row[0])
                    pp[line_count-1] = float(row[pp_loc])-P0
                    line_count += 1
                # x = np.append([x],[row[0]]);
                # pp = np.append([pp],[row[-1]]);


    plt.plot(x,pp,'.')
    # plt.savefig('theis_solution.png')

def porosity_weighted_average(val=None,phi=None):
    """
    This function takes the fluid and solid value and calculates an average
    in the way presented in the MOOSE documentation and Saar (2011) review.
    Useful for calculating the average thermal conductivity and other thermal
    parameters.

    val [val_f,val_s] should be lenght two with the value of the fluid and solid
    phi is the porosity
    """
    import numpy as np

    if val is None:
        print('ERROR, need provide val to provide fluid and solid values')
        alkjfsdlk #error
    elif len(val) != 2:
        print('ERROR, need the value to provide fluid and solid values')
        lkjalksdfj #error

    if phi is None:
        phi = 0.1
        print('WARNING: val_f not defined')

    weighted_average = float(phi)*float(val[0]) + (1.0-float(phi))*float(val[1])
    return weighted_average


def Postprocessors_plot_over_time(filename = None):
    """
    This plots the values over time from a [Posptroccessor] with
    type = PointValue and outputs = csv.
    """
    import csv
    import numpy as np
    import matplotlib.pyplot as plt
    import mpmath
    import os

    t = np.zeros(0)
    uz_0 = np.zeros(0);
    uz_1 = np.zeros(0);
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                junkvar = 1
                line_count += 1
            else:
                t = np.append(t,float(row[0]))
                uz_0 = np.append(uz_0,float(row[1]))
                uz_1 = np.append(uz_1,float(row[2]))
                # if float(row[fixed_axis]) > z_plot_loc-.1 and float(row[fixed_axis]) <  z_plot_loc+.1 and float(row[0])>0:
                #     x[line_count-1] = float(row[0])
                #     pp[line_count-1] = float(row[pp_loc])-P0
                #     line_count += 1
                # x = np.append([x],[row[0]]);
                # pp = np.append([pp],[row[-1]]);

    return [t, uz_0, uz_1]
