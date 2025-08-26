# import dataclasses
# from collections.abc import Callable, MutableMapping
# from dataclasses import Field, is_dataclass
# from enum import Enum, StrEnum
# from types import NoneType, UnionType
# from typing import Any, TypeVar, Union, get_args, get_origin
# from weakref import WeakKeyDictionary

# from ._util import class_decorator, expect_dict, expect_str, expect_type, ft, fv

# _class_to_tag_name: MutableMapping[type, str] = WeakKeyDictionary()


# def register_tag_name(cls: type, tag_name: str):
#     if cls in _class_to_tag_name:
#         raise ValueError(f"tag name already registered for {ft(cls)}")
#     _class_to_tag_name[cls] = tag_name


# def tag_name(cls: type) -> str | None:
#     return _class_to_tag_name.get(cls, cls.__name__)


# _class_to_from_dict: MutableMapping[type, Callable[[Any], Any]] = WeakKeyDictionary()


# T = TypeVar("T")


# def register_from_dict(cls: type[T], deserialize: Callable[[Any], T]):
#     if cls in _class_to_from_dict:
#         raise ValueError(f"deserialize already registered for {ft(cls)}")
#     _class_to_from_dict[cls] = deserialize


# def from_dict(cls: type[T], obj) -> T:
#     if cls not in _class_to_from_dict:
#         raise TypeError(f"no deserialize implementation registered for type {ft(cls)}")
#     return _class_to_from_dict[cls](obj)


# def _from_dict_primitive(cls: type[T]) -> Callable[[Any], T]:
#     def _from_dict_primitive_inner(obj) -> T:
# if not isinstance(obj, cls):
#     raise TypeError(f"expected a value of type {ft(cls)} but got type {ft(type(obj))} from value {fv(obj)}")
#         return obj

#     return _from_dict_primitive_inner


# register_from_dict(int, _from_dict_primitive(int))
# register_from_dict(float, _from_dict_primitive(float))
# register_from_dict(str, _from_dict_primitive(str))
# register_from_dict(bool, _from_dict_primitive(bool))


# def _from_dict_abc(cls: type[T], tag_key: str) -> Callable[[Any], T]:
#     def _from_dict_abc_inner(obj) -> T:
#         obj = expect_dict(obj)
#         if tag_key not in obj:
#             raise KeyError(f"type tag {fv(tag_key)} is not present in f{fv(obj)}")
#         type_ = expect_str(obj[tag_key])
#         type_to_cls = {tag_name(sub_cls): sub_cls for sub_cls in cls.__subclasses__()}
#         if type_ not in type_to_cls:
#             raise ValueError(
#                 f"the type tag {fv(tag_key)} must be one of {fv(tuple(type_to_cls.keys()))} but got f{fv(type_)}"
#             )
#         sub_cls = type_to_cls[type_]
#         return from_dict(sub_cls, obj)

#     return _from_dict_abc_inner


# @class_decorator
# def from_dict_abc(*, tag_name: str | None = None, tag_key: str = "type"):
#     def from_dict_abc_inner(cls: type):
#         if tag_name is not None:
#             register_tag_name(cls, tag_name)
#         register_from_dict(cls, _from_dict_abc(cls, tag_key))
#         return cls

#     return from_dict_abc_inner


# def _from_dict_dataclass(cls: type[T]) -> Callable[[Any], T]:
#     def _from_dict_dataclass_inner(obj) -> T:
#         obj = expect_dict(obj)
#         fields = dataclasses.fields(cls)  # type: ignore
#         return cls(**{field.name: from_dict(expect_type(field.type), obj[field.name]) for field in fields})

#     return _from_dict_dataclass_inner


# @class_decorator
# def from_dict_dataclass(*, tag_name: str | None = None) -> Callable[[type], type]:
#     def from_dict_dataclass_inner(cls: type):
#         if tag_name is not None:
#             register_tag_name(cls, tag_name)
#         register_from_dict(cls, _from_dict_dataclass(cls))
#         return cls

#     return from_dict_dataclass_inner

# int
# float
# bool
# str
# None
# Literal[...]
# Union[...]
# TypedDict
# NamedTuple
# Enum
# StrEnum
# Protocol
# ABC
# list
# dict
# tuple
# generics
# dataclass
# NewType https://docs.python.org/3/library/typing.html#newtype


# First version must support:

# int
# float
# bool
# str
# str | None (Union)
# int | None (Union)
# StrEnum
# list      # value like
# dataclass # dict like

# T = TypeVar("T")

# Type[T] -> T has a strange behaviour https://github.com/python/mypy/issues/9003#issuecomment-734648129
# TypeVar incompatible with constrained union https://github.com/python/mypy/issues/9424
# TypeForm[T]: Spelling for regular types (int, str) & special forms (Union[int, str], Literal['foo'], etc) https://github.com/python/mypy/issues/9773


# def is_union(type_) -> bool:
#     return isinstance(type_, UnionType)


# def dataclass_field_from_dict(field: Field, obj: dict):
#     if is_union(field.type) is Union:
#         types = get_args(field.type)
#         if NoneType in types:
#             if field.name in obj:


#         raise ValueError("UNION", can_be_none, get_args(field.type))
#     else:
#         pass


# def from_dict(cls: type[T], obj) -> T:
#     if is_dataclass(cls):
#         obj = expect_dict(obj)
#         fields = dataclasses.fields(cls)
#         return cls(**{field.name: dataclass_field_from_dict(field, obj) for field in fields})

#     # TODO: dict

#     raise ValueError(f"Unsupported type {ft(cls)}")
