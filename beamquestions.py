import beamobjects
from beamobjects import beam 

beam_type = input("Preset or Custom? ")

if beam_type.lower() == "preset":
    material = input("Wood, Concrete, or Steel? ").lower()
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
        support_type = input(f"Enter the type of support (Pin, Roller, or Fixed) {i+1}: ").upper()
        distance = float(input(f"Enter the distance of support {i+1} from the left support: "))
        support = beamobjects.SupportObj(support_type, distance)
        supports_list[i] = support
else:
    raise ValueError("Invalid number of supports. Must be greater than 0.")

moment_of_intertia = input("Enter the Moment of Intertia of the beam in m^4: ")
if moment_of_intertia == "":
    print("The default value for moment of intertia is 83e-3 m^4.")
    moment_of_intertia = 83e-3 #m^4 default value is b = 1m and h = 1m for a rectangular beam
elif float(moment_of_intertia) <= 0:
    raise ValueError("Invalid Moment of Inertia. Must be greater than 0.")
else:
    moment_of_intertia = float(moment_of_intertia)
cross_area = float(input("Enter the cross-sectional area of the beam in m^2: "))
extreme_fiber = float(input("Enter the distance to the extreme fiber of the beam in m^2: "))

point_loads_list = []  # Initialize the point_loads_list to an empty list
WeightofBeam = input("Is the weight of the beam negligible? Yes or No: ").lower()
if WeightofBeam == "no":
    if material in ["wood", "concrete", "steel"]:
        weight = beaminfo.density * 9.81 * beamlength * cross_area
        weight_distance = beamlength / 2
        weight_load = beamobjects.PointLoad(weight, weight_distance, "down")
        point_loads_list.append(weight_load)
    else:
        weight = float(input("Enter the weight of the beam in Newtons: "))
        weight_distance = float(input("Enter the distance of the weight from the left support in meters: "))
        weight_load = beamobjects.PointLoad(weight, weight_distance, "down")
        point_loads_list.append(weight_load)
else:
    pass  # If the weight of the beam is negligible, do nothing


numinputs = input("What type of loads? (point, distributed, both, or none): ").lower()
#Optional Input for point loads 
if numinputs == "point" or numinputs == "both":
    loads = int(input("How many point loads? "))
    if loads > 0:
        if WeightofBeam == "yes":
            point_loads_list = [None]*loads
        elif WeightofBeam == "no":
            point_loads_list = [None]*(loads + 1)  # Add one for the weight of the beam
            point_loads_list[loads] = weight_load #account for the weight of the beam in the loop below
        for i in range(loads):
            force = float(input(f"Enter the force of load {i+1} in Newtons: "))
            distance = float(input(f"Enter the distance of load {i+1} from the left support in meters: "))
            point_load_direction = input(f"Enter the direction of load {i+1} (up or down): ")
            point_load = beamobjects.PointLoad(force, distance, point_load_direction)  
            point_loads_list[i] = point_load
    elif loads == 0:
        if WeightofBeam == "no":
            pass # If the weight of the beam is already accounted for, do nothing
        else:
            raise ValueError("Invalid number of point loads. Must be greater than or equal to 0.")
    else:
        raise ValueError("Invalid number of point loads. Must be greater than or equal to 0.")
elif numinputs == "distributed" or numinputs == "none":
    pass #This will be handled in the next section   
else:
    raise ValueError("Invalid load type. Must be 'point', 'distributed', 'none', or 'both'.")
        
#Optional input for distributed loads
distributed_loads_list = [] # Initialize the distributed_loads_list to an empty list
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
    else:
        raise ValueError("Invalid number of distributed loads. Must be greater than 0.")
elif numinputs == 'none':
    pass

finalbeam = beamobjects.BeamFinal(beam=beaminfo, length=beamlength, Moment_of_Intertia = moment_of_intertia, cross_area = cross_area, extreme_fiber = extreme_fiber, supports=supports_list, point_loads=point_loads_list, distributed_loads=distributed_loads_list)