import iso6346


class ShippingContainer:

    HEIGHT_FT = 8.5
    WIDTH_FT = 8.0

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
    def create_empty(cls, owner_code, length_ft, **kwargs):
        return cls(owner_code, length_ft, contents=[], **kwargs)

    @classmethod
    def create_with_items(cls, owner_code, length_ft, items, **kwargs):
        return cls(owner_code, length_ft, contents=list(items), **kwargs)

    def __init__(self, owner_code, length_ft, contents, **kwargs):
        self.owner_code = owner_code
        self.length_ft = length_ft
        self.contents = contents
        self.bic = self._make_bic_code(owner_code=owner_code, serial=ShippingContainer._generate_serial())

    @property
    def volume_ft3(self):
        return ShippingContainer.HEIGHT_FT * ShippingContainer.WIDTH_FT * self.length_ft


class RefrigeratedShippingContainer(ShippingContainer):

    MAX_CELSIUS = 4.0
    FRIDGE_VOLUME_FT3 = 100

    # in order to make celsius keyword-only argument, we insert a singular * in the argument list before it
    def __init__(self, owner_code, length_ft, contents, *, celsius, **kwargs):
        """

        :type celsius: object
        """
        super.__init__(owner_code, length_ft, contents, **kwargs)
        """Self encapsulation where even uses of attributes internal to the class go through the property getter and 
        setter rather than directly accessing underlying attribute. It is a technique for helping establish and 
        maintain class invariants such as temperature constraint """
        self.celsius = celsius

    @staticmethod
    def _c_to_f(celsius):
        return celsius * 9/5 + 32

    @staticmethod
    def _f_to_c(fahrenheit):
        return (fahrenheit - 32) * 5 / 9

    # In pythons we do not use getter and setter methods but use the below two methods to set and get our attributes
    """ Enables to make celsius read only and not for public use """
    # getter method in python
    @property
    def celsius(self):
        return self._celsius

    """ Using the setter decorator in property taking celsius as decorator """
    # setter method in python
    @celsius.setter
    def celsius(self, value):
        if value > RefrigeratedShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature too hot!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return RefrigeratedShippingContainer._c_to_f(self.celsius)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = RefrigeratedShippingContainer._f_to_c(value)

    @property
    def volume_ft3(self):
        return (
            super().volume_ft3
            - RefrigeratedShippingContainer.FRIDGE_VOLUME_FT3
        )

    @staticmethod
    def _make_bic_code(owner_code: object, serial: object) -> object:
        return iso6346.create(owner_code=owner_code, serial=str(serial).zfill(6), category="R")


class HeatedRefrigeratedShippingContainer(RefrigeratedShippingContainer):

    MIN_CELSIUS = -20

    @RefrigeratedShippingContainer.celsius.setter
    def celsius(self, value):
        if value <= HeatedRefrigeratedShippingContainer.MIN_CELSIUS:
            raise ValueError("Temperature too cold!")
        RefrigeratedShippingContainer.celsius.fset(self, value)

