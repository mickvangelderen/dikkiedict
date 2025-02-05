`dikkiedict` is a dependency-free python library makes it easy to implement conversion from dict-like types for your own types.

This can be used, for example, to create configuration class instances from data parsed from a JSON, YAML, or TOML file.
It does not matter how you obtain the dict-like value and so this library is independent of any particular deserialization library.

```python
import json
from abc import ABC
from dataclasses import dataclass

from dikkiedict import from_dict, from_dict_abc, from_dict_dataclass

@from_dict_abc
class Base(ABC):  # noqa: B024
    pass

@from_dict_dataclass
@dataclass
class DerivedA(Base):
    a: int

@from_dict_dataclass
@dataclass
class DerivedB(Base):
    b: int

json_source = """\
{
    "type": "DerivedA",
    "a": 1
}
"""

dict_like = json.loads(json_source)

assert from_dict(Base, dict_like) == DerivedA(a=1)
```

The library is currently very unstable as there are open questions to answer:

- what should things be called
- should there be a single decorator or different decorators for `ABC`s, `dataclass`es

The library is also incomplete because it is lacking:

- support for `Union` types
- support for `Iterable` types
