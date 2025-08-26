from collections.abc import Hashable
from dataclasses import dataclass, fields, is_dataclass
from types import GenericAlias, UnionType
from typing import TypeAlias, TypeVar, Union, get_args, get_origin, overload

from frozendict import frozendict
from typing_extensions import TypeForm


@dataclass(frozen=True, slots=True, kw_only=True)
class Untagged:
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class InternallyTagged:
    variant_key: str | None = None
    variant_values: frozendict[Hashable, str] | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class AdjacentlyTagged:
    variant_key: str | None = None
    variant_values: frozendict[Hashable, str] | None = None
    content_key: str | None = None


type Tagging = Untagged | InternallyTagged | AdjacentlyTagged


def variant_key(tagging: Tagging):
    match tagging:
        case Untagged():
            return None
        case InternallyTagged(variant_key=value):
            return value
        case AdjacentlyTagged(variant_key=value):
            return value


class TaggedUnion:
    tagging: Tagging
    union: Hashable


type TypeLike = Hashable
type UnionLike = Hashable

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def list_from_dict(typ: TypeForm[T], value: list[object]) -> list[T]:
    return [from_dict(typ, item) for item in value]


def dict_from_dict(key_typ: TypeForm[K], val_typ: TypeForm[V], value: dict[object, object]) -> dict[K, V]:
    return {from_dict(key_typ, k): from_dict(val_typ, v) for k, v in value.items()}


def from_dict(typ: TypeForm[T], value: object) -> T:
    origin = get_origin(typ)

    if origin is list:
        (item_typ,) = get_args(typ)
        if not isinstance(value, list):
            raise TypeError(f"Expected list for {typ}, got {type(value)}")
        return list_from_dict(item_typ, value)  # pyright: ignore[reportUnknownArgumentType, reportReturnType]

    if origin is dict:
        key_typ, val_typ = get_args(typ)
        if not isinstance(value, dict):
            raise TypeError(f"Expected dict for {typ}, got {type(value)}")
        return dict_from_dict(key_typ, val_typ, value)  # pyright: ignore[reportUnknownArgumentType, reportReturnType]

    # if origin is Union or isinstance(typ, UnionType):
    #     for option in get_args(typ):
    #         try:
    #             return from_dict(option, value)
    #         except Exception:
    #             continue
    #     raise TypeError(f"{value!r} not compatible with {typ}")

    # # Dataclasses
    # if isinstance(typ, type) and is_dataclass(typ):
    #     if not isinstance(value, dict):
    #         raise TypeError(f"Expected dict for {typ}, got {type(value)}")
    #     kwargs = {}
    #     for f in fields(typ):
    #         if f.name in value:
    #             kwargs[f.name] = from_dict(f.type, value[f.name])
    #     return typ(**kwargs)

    if typ is int:
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {typ}, got {type(value)}")
        return int(value)  # pyright: ignore[reportReturnType]

    if typ is str:
        if not isinstance(value, str):
            raise TypeError(f"Expected str for {typ}, got {type(value)}")
        return str(value)  # pyright: ignore[reportReturnType]

    raise NotImplementedError(f"Don't know how to handle {typ!r}")


def test_from_dict():
    out: list[int] = from_dict(list[int], 1)
    assert out == [1]
    out2: str | int = from_dict(Union[int, str], 1)
    assert from_dict(str, "s") == 2


# from abc import ABC
# from dataclasses import dataclass

# import pytest

# from . import from_dict

# from . import from_dict, from_dict_abc, from_dict_dataclass


# def test_from_dict():
#     @from_dict_abc
#     class Base(ABC):  # noqa: B024
#         pass

#     @from_dict_dataclass
#     @dataclass
#     class DerivedA(Base):
#         a: int

#     @from_dict_dataclass
#     @dataclass
#     class DerivedB(Base):
#         b: int

#     assert from_dict(
#         Base,
#         {
#             "type": "DerivedA",
#             "a": 1,
#         },
#     ) == DerivedA(1)

#     assert from_dict(
#         Base,
#         {
#             "type": "DerivedB",
#             "b": 2,
#         },
#     ) == DerivedB(2)


# def test_from_dict_with_tag_key():
#     @from_dict_abc(tag_key="tag")
#     class Base(ABC):  # noqa: B024
#         pass

#     @from_dict_dataclass
#     @dataclass
#     class DerivedA(Base):
#         a: int

#     @from_dict_dataclass
#     @dataclass
#     class DerivedB(Base):
#         b: int

#     assert from_dict(
#         Base,
#         {
#             "tag": "DerivedA",
#             "a": 1,
#         },
#     ) == DerivedA(1)

#     assert from_dict(
#         Base,
#         {
#             "tag": "DerivedB",
#             "b": 2,
#         },
#     ) == DerivedB(2)


# def test_from_dict_with_tag_name():
#     @from_dict_abc
#     class Base(ABC):  # noqa: B024
#         pass

#     @from_dict_dataclass(tag_name="a")
#     @dataclass
#     class DerivedA(Base):
#         a: int

#     @from_dict_dataclass(tag_name="b")
#     @dataclass
#     class DerivedB(Base):
#         b: int

#     assert from_dict(
#         Base,
#         {
#             "type": "a",
#             "a": 1,
#         },
#     ) == DerivedA(1)

#     assert from_dict(
#         Base,
#         {
#             "type": "b",
#             "b": 2,
#         },
#     ) == DerivedB(2)


# def test_type_error():
#     @from_dict_dataclass
#     @dataclass
#     class A:
#         a: int

#     assert from_dict(
#         A,
#         {
#             "a": 1,
#         },
#     ) == A(1)

#     with pytest.raises(TypeError):
#         _ = (
#             from_dict(
#                 A,
#                 {
#                     "a": "1",
#                 },
#             ),
#         )


# def test_primitives():
#     @from_dict_dataclass
#     @dataclass
#     class A:
#         a: int
#         c: bool
#         d: str
#         d:

#     assert from_dict(
#         A,
#         {
#             "a": 1,
#         },
#     ) == A(1)


# def test_all():
#     @dataclass
#     class A:
#         a: int | None

#     assert from_dict(A, {}) == A(None)
