import sys
from collections.abc import Callable, Iterator, Mapping
from typing import Any, ClassVar, Generic, TypeVar, final, overload
from typing_extensions import ParamSpec

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = ("Context", "ContextVar", "Token", "copy_context")

_T = TypeVar("_T")
_D = TypeVar("_D")
_P = ParamSpec("_P")

@final
class ContextVar(Generic[_T]):
    @overload
    def __init__(self, name: str) -> None: ...
    @overload
    def __init__(self, name: str, *, default: _T) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def name(self) -> str: ...
    @overload
    def get(self) -> _T: ...
    @overload
    def get(self, __default: _T) -> _T: ...
    @overload
    def get(self, __default: _D) -> _D | _T: ...
    def set(self, __value: _T) -> Token[_T]: ...
    def reset(self, __token: Token[_T]) -> None: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

@final
class Token(Generic[_T]):
    @property
    def var(self) -> ContextVar[_T]: ...
    @property
    def old_value(
        self,
    ) -> Any: ...  # returns either _T or MISSING, but that's hard to express
    MISSING: ClassVar[object]
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

def copy_context() -> Context: ...

# It doesn't make sense to make this generic, because for most Contexts each ContextVar will have
# a different value.
@final
class Context(Mapping[ContextVar[Any], Any]):
    def __init__(self) -> None: ...
    @overload
    def get(self, __key: ContextVar[_T], __default: None = None) -> _T | None: ...
    @overload
    def get(self, __key: ContextVar[_T], __default: _T) -> _T: ...
    @overload
    def get(self, __key: ContextVar[_T], __default: _D) -> _T | _D: ...
    def run(
        self, callable: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> _T: ...
    def copy(self) -> Context: ...
    def __getitem__(self, __key: ContextVar[_T]) -> _T: ...
    def __iter__(self) -> Iterator[ContextVar[Any]]: ...
    def __len__(self) -> int: ...
    def __eq__(self, __value: object) -> bool: ...
