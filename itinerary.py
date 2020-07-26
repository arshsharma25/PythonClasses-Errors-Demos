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


# function decorator factory
def postcondition(predicate):

    def function_decorator(f):

        @functools.warp(f)
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            if not predicate(self):
                raise RuntimeError(
                    f"Post-condition {predicate.__name__} not "
                    f"maintained for {self!r}"
                )
            return result

        return wrapper

    return function_decorator

# class factory decorator
def invariant(predicate):
    function_decorator = postcondition(predicate)

    def class_decorator(cls):
        # copy of members of the class being decorated
        # we take a copy because we shouldn't modify the mapping while we're iterating over it
        members = list(vars(cls).items())
        for name, member in members:
            # we did not use ismethod as a member function does not become method until it bounds to an instance
            # if a member is a function we decorate it with the function_decorator
            if inspect.isfunction(member):
                decorated_member = function_decorator(member)
                # we reset the member in the class being decorated to the decorated function
                setattr(cls, name, decorated_member)

    return class_decorator


def at_least_two_locations(itinerary):
    return len(itinerary._locations) >= 2

def no_duplicates(itinerary):
    already_seen = set()
    for location in itinerary._locations:
        if location in already_seen:
            return False
        already_seen.add(location)
    return True

@auto_repr
@invariant(no_duplicates)
@invariant(at_least_two_locations)
# It manages a list of locations on a journey
class Itinerary:

    # named constructor
    @classmethod
    def from_locations(cls, *locations):
        return cls(locations)


    def __init__(self, locations):
        self._locations = locations

    def __str__(self):
        return "\n".join(location.name for location in self._locations)

    @property
    def locations(self):
        return tuple(self._locations)

    @property
    def origin(self):
        return self._locations[0]

    @property
    def destination(self):
        return self._locations[-1]


    def add(self, location):
        self._locations.append(location)


    def remove(self, name):
        removal_indexes = [
            index for index, location in enumerate(self._locations)
            if location.name == name
        ]
        for index in reversed(removal_indexes):
            del self._locations[index]


    def truncate_at(self, name):
        stop = None
        for index, location in enumerate(self._locations):
            if location.name == name:
                stop = index + 1

        self._locations = self._locations[:stop]
