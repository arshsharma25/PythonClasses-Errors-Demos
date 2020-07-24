from utility import typename

def auto_repr(cls):
    print(f"Decorating {cls.__name__} with auto_repr")
    # Members of the class will be extracted using in-built function -- vars
    # It returns a mapping from member names to members objects
    members = vars(cls)
    for name, member in members.items():
        print(name, member)
    return cls


@auto_repr
class Location:

    def __init__(self, name, position):
        self._name = _name
        self._position = position


    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    def __str__(self):
        return self.name

hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
