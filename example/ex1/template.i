[MeshGenerators]
  [./gmg]
    type = GeneratedMeshGenerator
    dim = 3
    nx = 20
    ny = 2
    nz = 20
    bias_x = 1.2
    xmin = 0.0
    xmax = 200.0
    ymin = 0.0
    ymax = 1.0
    bias_z = 1.2
    zmax = 0.0
    zmin = -200.0
  []

  ### For two wells on the bottom
  [./createNewSidesetOne]
    type = SideSetsFromBoundingBoxGenerator
    input = gmg
    boundary_id_old = 'back' #says to look on the bottom boundary
    boundary_id_new = 10     #new boundary is assigned to 10
    # bottom_left = '-0.1 0.69 0.99' #bounds of the new boundary
    # top_right = '0.31 1.1 1.1'     #bounds of the new boundary
    bottom_left = '0 -0.1 -1000.1' #bounds of the new boundary
    top_right = '1.071 51 100'     #bounds of the new boundary
    block_id = 0                #applied on block_id = 0 (i.e. the whole domain)
  []
  [./createNewSidesetTwo]
    type = SideSetsFromBoundingBoxGenerator
    input = createNewSidesetOne
    boundary_id_old = 'back'
    boundary_id_new = 11
    # bottom_left = '0.69 -0.1 0.99' #bounds of the new boundary
    # top_right = '0.8 1.1 1.01'     #bounds of the new boundary
    bottom_left = '40 -0.1 -1000' #bounds of the new boundary
    top_right = '50 51 100'     #bounds of the new boundary
    block_id = 0
  []
[]

[Mesh]
  type = MeshGeneratorMesh
  boundary_id = '10 11'
  boundary_name = 'injectionBC productionBC'
[]

[GlobalParams]
  PorousFlowDictator = dictator
  gravity = '0 0 0'
[]

[Variables]
  [./temp]
    initial_condition = 0
  [../]
  [./pp]
    scaling = 1e7
    initial_condition = 0.0
  [../]
[]

[BCs]
  [./injection]
    type = PorousFlowSink
    variable = pp
    boundary = injectionBC
    #flux_function = -0.0233426704015
    flux_function = flux_function_placeholder
    fluid_phase = 0
    use_mobility = use_mobility_placeholder
    save_in = fluxes_in
  [../]
  [./production]
    type = PorousFlowSink
    variable = pp
    boundary = productionBC
    flux_function = 0
    # flux_function =  0.0025
    fluid_phase = 0
    use_mobility = use_mobility_placeholder
    save_in = fluxes_out
  [../]
 [./injection_heat]
   type = PresetBC
   variable = temp
   boundary = injectionBC
   value = 0
 [../]

 # [./production_heat]
 #   type = PorousFlowSink
 #   variable = temp
 #   boundary = productionBC
 #   # flux_function = 0
 #   #flux_function =  1.e0
 #   flux_function =  0.25
 #   use_enthalpy = true
 #   fluid_phase = 0
 #   use_mobility = true
 # [../]
[]

# [Adaptivity]
#  marker = errorfrac
#  steps = 2
#  max_h_level = 2
#  [./Indicators]
#    [./error]
#      type = GradientJumpIndicator
#      variable = pp
#      # variable = temp
#      outputs = none
#    [../]
#  [../]
#  [./Markers]
#    [./errorfrac]
#      type = ErrorFractionMarker
#      refine = 0.5  #Refines the elements that contribut the top 50% of error.
#      coarsen = 0.1 #this would coarsen the elements that contribute only 10% of the error, but wont coarsen past original size
#      indicator = error
#      outputs = none
#    [../]
#  [../]
# []

[Kernels]
  [./mass0]
    type = PorousFlowMassTimeDerivative
    fluid_component = 0
    variable = pp
  [../]
  [./adv0]
    type = PorousFlowAdvectiveFlux
    fluid_component = 0
    variable = pp
  [../]
 [./energy_dot]
   type = PorousFlowEnergyTimeDerivative
   variable = temp
 [../]
 [./convection]
   type = PorousFlowHeatAdvection
   variable = temp
 [../]
 [./conduction]
   type = PorousFlowHeatConduction
   variable = temp
 [../]
[]

[UserObjects]
  [./dictator]
    type = PorousFlowDictator
    # porous_flow_vars = 'pp'
    porous_flow_vars = 'pp temp'
    number_fluid_phases = 1
    number_fluid_components = 1
  [../]
[]

[Modules]
  [./FluidProperties]
    [./simple_fluid]
      type = SimpleFluidProperties
      bulk_modulus = 1.0
      density0 = density_placeholder
      #density0 = 1.
      thermal_expansion = 0.0
      viscosity = viscosity_placeholder
      cv = 4.2e3
    [../]
  [../]
[]

[Materials]
  [./permeability]
    type = PorousFlowPermeabilityConst
    permeability = 'permeability_placeholder 0 0   0 permeability_placeholder 0   0 0 permeability_placeholder'
  [../]
  [./poro]
    type = PorousFlowPorosityConst
    porosity = 1e-1
  [../]
  [./relp]
    type = PorousFlowRelativePermeabilityConst
    phase = 0
  [../]
  [./rock_heat]
    type = PorousFlowMatrixInternalEnergy
    specific_heat_capacity = 800
    density = 2500
  [../]
 [./temperature]
   type = PorousFlowTemperature
   temperature = temp
 [../]
  [./ppss_qp]
    type = PorousFlow1PhaseFullySaturated
    porepressure = pp
  [../]
  [./massfrac]
    type = PorousFlowMassFraction
  [../]
  [./simple_fluid_qp]
    type = PorousFlowSingleComponentFluid
    fp = simple_fluid
    phase = 0
  [../]
 [./rock_thermal_conductivity]
   type = PorousFlowThermalConductivityIdeal
   dry_thermal_conductivity = '2.1 0 0  0 2.1 0  0 0 2.1'
   wet_thermal_conductivity = '1.8 0 0  0 1.8 0  0 0 1.8'
 [../]
[]

[Preconditioning]
  [./smp]
    type = SMP
    full = true
    petsc_options_iname = '-pc_type -pc_factor_mat_solver_package'
    petsc_options_value = 'lu mumps'
  [../]
[]


[AuxVariables]
  [./fluxes_out]
  [../]
  [./fluxes_in]
  [../]
  [./darcy_x]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./darcy_y]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./darcy_z]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./density_water]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./porosity]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./permeability_x]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./permeability_xy]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./permeability_y]
    family = MONOMIAL
    order = CONSTANT
  [../]
[]

[AuxKernels]
  [./darcy_x]
    type = PorousFlowDarcyVelocityComponent
    variable = darcy_x
    gravity = '0 0 0'
    component = x
    #block = 'EnhPerm'
  [../]
  [./darcy_y]
    type = PorousFlowDarcyVelocityComponent
    variable = darcy_y
    #gravity = '0 0 -10E-6'
    gravity = '0 0 0'
    component = y
  [../]
  [./darcy_z]
    type = PorousFlowDarcyVelocityComponent
    variable = darcy_z
    gravity = '0 0 0'
    component = z
  [../]
  [./density_water]
    type = PorousFlowPropertyAux
    variable = density_water
    property = density
    phase = 0
    execute_on = timestep_end
  [../]
  [./porosity]
    type = MaterialRealAux
    property = PorousFlow_porosity_qp
    variable = porosity
  [../]
  [./permeability_x]
    type = MaterialRealTensorValueAux
    property = PorousFlow_permeability_qp
    column = 0
    row = 0
    variable = permeability_x
  [../]
  [./permeability_xy]
    type = MaterialRealTensorValueAux
    property = PorousFlow_permeability_qp
    column = 0
    row = 1
    variable = permeability_xy
  [../]
  [./permeability_y]
    type = MaterialRealTensorValueAux
    property = PorousFlow_permeability_qp
    column = 0
    row = 0
    variable = permeability_y
  [../]
[]

[Debug]
  show_var_residual_norms = true
[]

[Postprocessors]
  [./outlet_flux_kg_s]
    type = NodalSum
    boundary = productionBC
    variable = fluxes_out
    execute_on = 'timestep_end'
  [../]
  [./inlet_flux_kg_s]
    type = NodalSum
    boundary = injectionBC
    variable = fluxes_in
    execute_on = 'timestep_end'
  [../]
[]

[Executioner]
  type = Transient
  solve_type = NEWTON
  start_time = 0.0
  end_time = 100
  # dt = 2.e5
  dtmax = 100
  dtmin = 1
 [./TimeStepper]
   type = IterationAdaptiveDT
   dt = 1.0
   optimal_iterations = 6
   # time_t  = '0  60'
   # time_dt = '1  1'
 [../]
# controls for linear iterations
  l_max_its = 15
  l_tol = 1e-10
# controls for nonlinear iterations
  nl_max_its = 20
  nl_rel_tol = 1e-5
  nl_abs_tol = 1e-10
[]

## Puts correct pressure out
[VectorPostprocessors]
  [./pressure]
    type = SideValueSampler
    variable = pp
    sort_by = x
    execute_on = timestep_end
    boundary = bottom
  [../]
[]

[Outputs]
  [./out]
    type = Exodus
    execute_on = 'initial timestep_end'
  [../]
  [./csv]
    type = CSV
    execute_on = final
  [../]
[]
