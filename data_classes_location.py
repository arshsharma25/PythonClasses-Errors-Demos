from utility import typename

def auto_repr(cls):

    # Members of the class will be extracted using in-built function -- vars
    # It returns a mapping from member names to members objects
    members = vars(cls)
    for name, member in members.items():
        print(name, member)

    if "__repr__ " in members:
        raise TypeError(f"{cls.__name__} already defines __repr__")

    if "__init__" in members:
        raise TypeError(f"{cls.__name__} does not override __init__")

    # We need to verify every argument of __init__ beyond self, there exists a
    # property with the same name
    # to get hold of the argument list by passing reference of __init__ to signature method
    sig = inspect.signature(cls.__init__)
    # as self is the first argument we do not need it
    parameter_names = list(sig.parameters)[1:]
    print("__init__ parameter names: ", parameter_names)

    # Given a parameter name here called name, this expression attempts to get object corresponding to that name from the members mapping. If there is no entry matching name, the call to get returns None. We then check the type of results of this lookup against property. The built-in property decorator is also the property object that the property operator produces

    # this generator expression evaluates to a series of boolean values, but we need all values to be True
    if not all(
        # this expression evaluates true if the object associated with name is a property  rather than say, a regular method
        isinstance(members.get(name, None, property))
        # checking for each parameter name
        for name in parameter_names
    )
        raise TypeError(
            f"Cannot apply auto_repr to {cls.__name__} because not all "
            "__init__ parameters have matching properties"
        )

    def synthesized_repr(self):
        return "{typename}({args})".format(
            # to report runtime dynamic type of self
            typename=typename(self),
            args=",".join(
                # using repr here so resulting string looks like source code
                "{name}={value!r}".format(
                    # to retrive property value from self instance
                    name=name,
                    value=getattr(self, name)
                ) for name in parameter_names
            )
        )

    # We need to plug the synthesized_repr function into the class being decorated as __repr__
    setattr(cls, "__repr__", synthesized_repr)

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

    # special methods to support equality comparison
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.name == other.name) and (self.position == other.position)

    def __hash__(self):
        return hash((self.name, self.position))



hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
