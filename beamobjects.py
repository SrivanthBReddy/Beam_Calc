from dataclasses import dataclass
from enum import Enum
from dataclasses import field

#Wood
class Wood(Enum):
    YOUNGMODULE = (1.3*(10**10)) 
    YEILDSTRENGTH = (3*(10**7))
    DENSITY = ()

#Concrete
class Concrete(Enum):
    YOUNGMODULE = ()
    YEILDSTRENGTH = ()
    DENSITY = ()

#Steel
class Steel(Enum):
    YOUNGMODULE = () 
    YEILDSTRENGTH = ()
    DENSITY = () 

#End Supports
class Support(Enum):
    FIXED = "Fixed"
    ROLLER = "Roller"
    PIN = "Pin"
    
#custom
class beam:
    def __init__(self, material : str = None,youngs_modulus: float = None, yield_strength: float = None, density: float = None):
        if material is not None and youngs_modulus is not None and yield_strength is not None and density is not None:
            self.material = material
            self.youngs_modulus = youngs_modulus
            self.yield_strength = yield_strength
            self.density = density
        elif material is None and youngs_modulus is not None and yield_strength is not None and density is not None:
            self.material = "Material"
            self.youngs_modulus = youngs_modulus
            self.yield_strength = yield_strength
            self.density = density
        elif str.lower(material) == "wood":
            self.youngs_modulus = Wood.YOUNGMODULE.value
            self.yield_strength = Wood.YEILDSTRENGTH.value
            self.density = Wood.DENSITY.value
        elif str.lower(material) == "concrete":
            self.youngs_modulus = Concrete.YOUNGMODULE.value
            self.yield_strength = Concrete.YEILDSTRENGTH.value
            self.density = Concrete.DENSITY.value
        elif str.lower(material) == "steel":
            self.youngs_modulus = Steel.YOUNGMODULE.value
            self.yield_strength = Steel.YEILDSTRENGTH.value
            self.density = Steel.DENSITY.value
        else : 
            raise ValueError("Invalid material or missing properties for custom beam. Must be in the order of Mateerial Name, Youngs Moduls, Yeild Strenght, and Density")
        
@dataclass
class SupportObj:
    type: str
    distance: float

@dataclass
class PointLoad:
    force: float
    distance: float
    direction: str

@dataclass
class DistributedLoad:
    load_type: str
    load_value: float
    x_initial: float
    x_final: float
    direction: str

@dataclass
class BeamFinal:
    beam: beam
    length: float
    supports: list[SupportObj]
    point_loads: list[PointLoad] = field(default_factory=list)
    distributed_loads: list[DistributedLoad] = field(default_factory=list)
    Moment_of_Intertia: float = float




#Preset or Custom

#if Preset
#Wood Concrete or Steel
#What is the length of your beam in meters?
#how many supports?
#state the support type, where in meters from the left support in the form, and the orientation of the support(top or bottom) (Support Type, Distance from left support, orientation), ...
#(optional)State the load applied to the beam and where in Newtons and meters in the form (Force, Distance from left support), ...
#(optional)State the distritubted load applied type(rectangular, triangluar bottom to top, triangular top to bottom) and the load in Newtons per meter and the start and end distance from the left support in meters in the form (Load Type, Load in N/m, x initial from left support, x final from left support), ...


#if custom
#Enter your material name, Youngs Modulus, Yeild Strength, and Density in that order.
#What is the length of your beam in meters?
#how many supports?
#state the support type and where in meters from the left support in the form (Support Type, Distance from left support), ...
#(optional)State the load applied to the beam and where in Newtons and meters in the form (Force, Distance from left support), ...
#(optional)State the distritubted load applied type(rectangular, triangluar bottom to top, triangular top to bottom) and the load in Newtons per meter and the start and end distance from the left support in meters in the form (Load Type, Load in N/m, x initial from left support, x final from left support), ...

#output should be a graph of the force, moment, deflection, stress, and strain of the beam of the beam with the maximum values of each displayed on the graph.









