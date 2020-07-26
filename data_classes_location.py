from dataclasses import dataclass

from position import Position, EarthPosition

# arguments passed in dataclass decorator so it is a decorator factory
@dataclass(
    init=True, # enables __init__
    repr=True, # enables __repr__
    eq=True,  # enables __eq__
    order=False, # enables __lt__, __gt__ etc i.e. less than or greater than
    unsafe_hash=False,
    frozen=False,
)
class Location:
    name: str
    position: Position




hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
stockholm = Location("Stockholm", EarthPosition(59.33, 18.06))
cape_town = Location("Cape Town", EarthPosition(-33.93, 18.42))
rotterdam = Location("Rotterdam", EarthPosition(51.96, 4.47))
maracaibo = Location("Maracaibo", EarthPosition(10.65, -71.65))
