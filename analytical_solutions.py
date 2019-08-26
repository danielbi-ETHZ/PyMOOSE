def theis_solution(permeability_val=None,density_val=None,viscosity_val=None,
                   filename=None,use_mobility=None,
                   flux_function = None):
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
    dx = 1.071; dy = 1.0; #meters
    if flux_function == None:
        flux_function = -0.233426704015
    b = 1.0; # thickness (m)
    Kw = 1.0 # compressibility of water (Pa^-1)
    phi = 0.1 # porosity
    t_end = 100.0; #seconds
    if use_mobility == None:
        use_mobility = False
    ## Calculations
    well_area = dx*dy; # well area (m2)
    print 'well_area ', well_area

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
    prefactor = 4.0*Q*viscosity_val/(4.0*np.pi*b*permeability_val) # Pa, multiplier of exponential integral, 4.0 factor is because of 1/4 grid symmetry
    r_anal = np.linspace(1,200,101); #radius in meters
    dP_anal = np.zeros(len(r_anal))
    t_final = 1.e2; # seconds
    u = (r_anal**2.0)*phi*viscosity_val/(4.0*permeability_val*t_final*Kw)
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
                if float(row[2]) > -199.77360637445-.1 and float(row[2]) <  -199.77360637445+.1:
                    x[line_count-1] = float(row[0])
                    pp[line_count-1] = float(row[-1])
                    line_count += 1
                # x = np.append([x],[row[0]]);
                # pp = np.append([pp],[row[-1]]);


    plt.plot(x,pp,'.')
