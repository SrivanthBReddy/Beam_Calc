import beamobjects

beam_type = input("Preset or Custom? ")

if beam_type.lower() == "preset":
    material = input("Wood, Concrete, or Steel?").lower()
    beaminfo = beamobjects.beam(material)
    beamlength = float(input("What is the length of your beam in meters? "))
elif beam_type.lower() == "custom":
    name = input("Enter your material name: ")
    youngs_modulus = float(input("Enter Young's Modulus in Pascals: "))
    yield_strength = float(input("Enter Yield Strength in Pascals: "))
    density = float(input("Enter Density in kg/m^3: "))
    beaminfo = beamobjects.beam(material=name, youngs_modulus=youngs_modulus, yield_strength=yield_strength, density=density)
    beamlength = float(input("What is the length of your beam in meters? "))
else:
    raise ValueError("Invalid beam type. Please enter 'Preset' or 'Custom'.")

supports = int(input("How many supports? "))
if supports > 0:
    supports_list = [None]*supports
    for i in range(supports):
        support_type = input(f"Enter the type of support (Pin, Roller, or Fixed) {i+1}: ")
        distance = float(input(f"Enter the distance of support {i+1} from the left support: "))
        support = beamobjects.SupportObj(support_type, distance)
        supports_list[i] = support
else:
    raise ValueError("Invalid number of supports. Must be greater than 0.")

numinputs = input("What type of loads? (point, distributed, both, or none): ").lower()

#Optional Input for point loads
if numinputs == "none":
    finalbeam = beamobjects.BeamFinalPlain(beam=beaminfo, length=beamlength, supports=supports_list)   
if numinputs == "point" or numinputs == "both":
    loads = int(input("How many point loads? "))
    if loads > 0:
        point_loads_list = [None]*loads
        for i in range(loads):
            force = float(input(f"Enter the force of load {i+1} in Newtons: "))
            distance = float(input(f"Enter the distance of load {i+1} from the left support in meters: "))
            point_load_direction = input(f"Enter the direction of load {i+1} (up or down): ")
            point_load = beamobjects.PointLoad(force, distance, point_load_direction)  
            point_loads_list[i] = point_load
        if numinputs == "point":
            finalbeam = beamobjects.BeamFinalPoint(beam=beaminfo, length=beamlength, supports=supports_list, point_loads=point_loads_list)
    else :
        raise ValueError("Invalid number of point loads. Must be greater than 0.")
else:
    raise ValueError("Invalid load type. Must be 'point' or 'both'.")
        
#Optional input for distributed loads
if numinputs == "distributed" or numinputs == "both":
    distributed_loads = int(input("How many distributed loads? "))
    if distributed_loads > 0:
        distributed_loads_list = [None]*distributed_loads
        for i in range(distributed_loads):
            load_type = input(f"Enter the type of distributed load {i+1} (rectangular, triangular bottom to top, triangular top to bottom): ")
            load_value = float(input(f"Enter the load value of distributed load {i+1} in N/m(if triangular state the largest value of load): "))
            x_initial = float(input(f"Enter the initial distance of distributed load {i+1} from the left support in meters: "))
            x_final = float(input(f"Enter the final distance of distributed load {i+1} from the left support in meters: "))
            distributed_load_direction = input(f"Enter the direction of distributed load {i+1} (up or down): ")
            distributed_load = beamobjects.DistributedLoad(load_type, load_value, x_initial, x_final, distributed_load_direction)
            distributed_loads_list[i] = distributed_load
        if numinputs == "distributed":
            finalbeam = beamobjects.BeamFinalDistributed(beam=beaminfo, length=beamlength, supports=supports_list, distributed_loads=distributed_loads_list)
    else:
        raise ValueError("Invalid number of distributed loads. Must be greater than 0.")
else:
    raise ValueError("Invalid load type. Must be 'distributed' or 'both'.")
if numinputs == "both":
    finalbeam = beamobjects.BeamFinalBoth(beam=beaminfo, length=beamlength, supports=supports_list, point_loads=point_loads_list, distributed_loads=distributed_loads_list)
    