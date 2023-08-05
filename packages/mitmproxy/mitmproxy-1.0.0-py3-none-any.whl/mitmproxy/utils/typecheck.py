import typing


def check_type(attr_name: str, value: typing.Any, typeinfo: type) -> None:
    """
    This function checks if the provided value is an instance of typeinfo
    and raises a TypeError otherwise.

    The following types from the typing package have specialized support:

    - Union
    - Tuple
    - IO
    """
    # If we realize that we need to extend this list substantially, it may make sense
    # to use typeguard for this, but right now it's not worth the hassle for 16 lines of code.

    e = TypeError("Expected {} for {}, but got {}.".format(
        typeinfo,
        attr_name,
        type(value)
    ))

    if typeinfo.__qualname__ == "Union":
        for T in typeinfo.__union_params__:
            try:
                check_type(attr_name, value, T)
            except TypeError:
                pass
            else:
                return
        raise e
    elif typeinfo.__qualname__ == "Tuple":
        if not isinstance(value, (tuple, list)):
            raise e
        if len(typeinfo.__tuple_params__) != len(value):
            raise e
        for i, (x, T) in enumerate(zip(value, typeinfo.__tuple_params__)):
            check_type("{}[{}]".format(attr_name, i), x, T)
        return
    elif typeinfo.__qualname__ == "Sequence":
        T = typeinfo.__args__[0]
        if not isinstance(value, (tuple, list)):
            raise e
        for v in value:
            check_type(attr_name, v, T)
    elif typeinfo.__qualname__ == "IO":
        if hasattr(value, "read"):
            return
    elif not isinstance(value, typeinfo):
        raise e


def get_arg_type_from_constructor_annotation(cls: type, attr: str) -> typing.Optional[type]:
    """
    Returns the first type annotation for attr in the class hierarchy.
    """
    for c in cls.mro():
        if attr in getattr(c.__init__, "__annotations__", ()):
            return c.__init__.__annotations__[attr]
