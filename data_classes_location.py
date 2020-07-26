from dataclasses import dataclass

from position import Position, EarthPosition

# arguments passed in dataclass decorator so it is a decorator factory
@dataclass(
    init=True, # enables __init__
    repr=True, # enables __repr__
    eq=True,  # enables __eq__
    order=False, # enables __lt__, __gt__ etc i.e. less than or greater than
    unsafe_hash=False, # configure __hash__ If not configured we cannot use hash based collections like set or dict in the underlying class
    frozen=False, # it means immutable, if we make it True then we can use collections based on hash like set or dict in the underlying class
)
class Location:
    name: str
    position: Position

    # if some value is empty we will not be able to checking
    # this can be achieved by using __post__init__ method
    # when this method is called all instance attributes will have been initialized therefore it doesn't take any argument beyond self
    # it is good place to perform validation on data class instance construction
    def __post__init__(self):
        if self.name == "":
            raise ValueError("Location name cannot be empty!")




hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
stockholm = Location("Stockholm", EarthPosition(59.33, 18.06))
cape_town = Location("Cape Town", EarthPosition(-33.93, 18.42))
rotterdam = Location("Rotterdam", EarthPosition(51.96, 4.47))
maracaibo = Location("Maracaibo", EarthPosition(10.65, -71.65))
