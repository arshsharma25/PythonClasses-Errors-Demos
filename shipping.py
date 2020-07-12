import iso6346

class ShippingContainer:
    next_serial: int = 1337


    @classmethod
    def _generate_serial(cls):
        result = cls.next_serial
        cls.next_serial += 1
        return result


    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(owner_code=owner_code, serial=str(serial).zfill(6))


    @classmethod
    # As the Child Class _init__ method has additional arguments so in order for these functions to support we use
    # kwargs
    def create_empty(cls, owner_code, **kwargs):
        return cls(owner_code, contents=[], **kwargs)


    @classmethod
    def create_with_items(cls, owner_code, items, **kwargs):
        return cls(owner_code, contents=list(items), **kwargs)


    def __init__(self, owner_code, contents, **kwargs):
        self.owner_code = owner_code
        self.contents = contents
        self.bic = self._make_bic_code(owner_code=owner_code, serial=ShippingContainer._generate_serial())




class RefrigeratedShippingContainer(ShippingContainer):


    MAX_CELSIUS = 4.0


    # in order to make celsius keyword-only argument, we insert a singular * in the argument list before it
    def __init__(self, owner_code, contents, *, celsius, **kwargs):
        super.__init__(owner_code, contents, **kwargs)
        if celsius > RefrigeratedShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature too hot!")
        self.celsius = celsius




    @staticmethod
    def _make_bic_code(owner_code: object, serial: object) -> object:
        return iso6346.create(owner_code=owner_code, serial=str(serial).zfill(6), category="R")
