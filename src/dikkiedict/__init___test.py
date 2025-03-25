from abc import ABC
from dataclasses import dataclass

import pytest

from . import from_dict

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


def test_all():
    @dataclass
    class A:
        a: int | None

    assert from_dict(A, {}) == A(None)
