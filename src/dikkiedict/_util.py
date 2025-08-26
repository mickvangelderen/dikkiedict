from collections.abc import Callable
from typing import ParamSpec, TypeVar, overload


def ft(cls: object):
    """Format a type for in error strings."""
    if hasattr(cls, "__module__") and cls.__module__ not in ["__main__", "builtins"]:
        return f"`{cls.__module__}.{cls.__qualname__}`"
    else:
        return f"`{cls.__qualname__}`"


def fv(value: object):
    """Format a value for in error strings."""
    return f"`{repr(value)}`"


T = TypeVar("T")


def expect_instance(value: object, type_: type[T]) -> T:
    if isinstance(value, type_):
        return value
    else:
        raise TypeError(f"expected a value of type {ft(type_)} but got type {ft(type(value))} from value {fv(value)}")


def expect_str(value: object) -> str:
    return expect_instance(value, str)


def expect_dict(value: object) -> dict:  # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
    return expect_instance(value, dict)  # pyright: ignore[reportUnknownVariableType]


def expect_type(value: object) -> type:
    return expect_instance(value, type)


P = ParamSpec("P")


def class_decorator(decorator_generator: Callable[P, Callable[[type], type]]):
    """Returns a new decorator that can be called with and without parenthesis."""
    # NOTE(mickvangelderen): These overloads are only for type checking. I am
    # not sure my usage of them is correct. The order in which the overloads are
    # specified matters for some reason.

    @overload
    def wrapper(cls: type, /, *args: P.args, **kwargs: P.kwargs) -> type: ...

    @overload
    def wrapper(cls: None = None, /, *args: P.args, **kwargs: P.kwargs) -> Callable[[type], type]: ...

    def wrapper(cls: type | None = None, /, *args: P.args, **kwargs: P.kwargs) -> Callable[[type], type] | type:
        decorator = decorator_generator(*args, **kwargs)
        return decorator if cls is None else decorator(cls)

    return wrapper
