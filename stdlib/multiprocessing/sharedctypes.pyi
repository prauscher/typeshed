import ctypes
from collections.abc import Callable, Sequence
from ctypes import _CData, _SimpleCData, c_char
from multiprocessing.context import BaseContext
from multiprocessing.synchronize import _LockLike
from types import TracebackType
from typing import Any, Generic, Literal, Protocol, TypeVar, overload

__all__ = ["RawValue", "RawArray", "Value", "Array", "copy", "synchronized"]

_T = TypeVar("_T")
_SingleT = TypeVar("_SingleT")
_MultiGetT = TypeVar("_MultiGetT")
_MultiSetT = TypeVar("_MultiSetT")
_CT = TypeVar("_CT", bound=_CData)

@overload
def RawValue(typecode_or_type: type[_CT], *args: Any) -> _CT: ...
@overload
def RawValue(typecode_or_type: str, *args: Any) -> Any: ...
@overload
def RawArray(typecode_or_type: type[_CT], size_or_initializer: int | Sequence[Any]) -> ctypes.Array[_CT]: ...
@overload
def RawArray(typecode_or_type: str, size_or_initializer: int | Sequence[Any]) -> Any: ...
@overload
def Value(typecode_or_type: type[_CT], *args: Any, lock: Literal[False], ctx: BaseContext | None = None) -> _CT: ...
@overload
def Value(
    typecode_or_type: type[_CT], *args: Any, lock: Literal[True] | _LockLike = True, ctx: BaseContext | None = None
) -> SynchronizedBase[_CT]: ...
@overload
def Value(
    typecode_or_type: str, *args: Any, lock: Literal[True] | _LockLike = True, ctx: BaseContext | None = None
) -> SynchronizedBase[Any]: ...
@overload
def Value(
    typecode_or_type: str | type[_CData], *args: Any, lock: bool | _LockLike = True, ctx: BaseContext | None = None
) -> Any: ...
@overload
def Array(
    typecode_or_type: type[_CT], size_or_initializer: int | Sequence[Any], *, lock: Literal[False], ctx: BaseContext | None = None
) -> _CT: ...
@overload
def Array(
    typecode_or_type: type[c_char],
    size_or_initializer: int | Sequence[Any],
    *,
    lock: Literal[True] | _LockLike = True,
    ctx: BaseContext | None = None,
) -> SynchronizedString: ...
@overload
def Array(
    typecode_or_type: type[_CT],
    size_or_initializer: int | Sequence[Any],
    *,
    lock: Literal[True] | _LockLike = True,
    ctx: BaseContext | None = None,
) -> SynchronizedArray[_CT]: ...
@overload
def Array(
    typecode_or_type: str,
    size_or_initializer: int | Sequence[Any],
    *,
    lock: Literal[True] | _LockLike = True,
    ctx: BaseContext | None = None,
) -> SynchronizedArray[Any]: ...
@overload
def Array(
    typecode_or_type: str | type[_CData],
    size_or_initializer: int | Sequence[Any],
    *,
    lock: bool | _LockLike = True,
    ctx: BaseContext | None = None,
) -> Any: ...
def copy(obj: _CT) -> _CT: ...
@overload
def synchronized(obj: _SimpleCData[_T], lock: _LockLike | None = None, ctx: Any | None = None) -> Synchronized[_T]: ...
@overload
def synchronized(obj: ctypes.Array[c_char], lock: _LockLike | None = None, ctx: Any | None = None) -> SynchronizedString: ...
@overload
def synchronized(obj: ctypes.Array[_CT], lock: _LockLike | None = None, ctx: Any | None = None) -> SynchronizedArray[_CT]: ...
@overload
def synchronized(obj: _CT, lock: _LockLike | None = None, ctx: Any | None = None) -> SynchronizedBase[_CT]: ...

class _AcquireFunc(Protocol):
    def __call__(self, block: bool = ..., timeout: float | None = ..., /) -> bool: ...

class SynchronizedBase(Generic[_CT]):
    acquire: _AcquireFunc
    release: Callable[[], None]
    def __init__(self, obj: Any, lock: _LockLike | None = None, ctx: Any | None = None) -> None: ...
    def __reduce__(self) -> tuple[Callable[[Any, _LockLike], SynchronizedBase[Any]], tuple[Any, _LockLike]]: ...
    def get_obj(self) -> _CT: ...
    def get_lock(self) -> _LockLike: ...
    def __enter__(self) -> bool: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None, /
    ) -> None: ...

class Synchronized(SynchronizedBase[_SimpleCData[_T]], Generic[_T]):
    value: _T

class SynchronizedArray(SynchronizedBase[ctypes.Array[_CT]], Generic[_CT]):
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: slice) -> Any: ...
    @overload
    def __getitem__(self, i: int) -> Any: ...
    @overload
    def __setitem__(self, i: slice, value: Any) -> None: ...
    @overload
    def __setitem__(self, i: int, value: Any) -> None: ...
    def __getslice__(self, start: int, stop: int) -> Any: ...
    def __setslice__(self, start: int, stop: int, values: Any) -> None: ...

class SynchronizedString(SynchronizedArray[c_char]):
    value: bytes
    raw: bytes
