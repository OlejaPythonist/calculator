import abc
from typing import Protocol, NamedTuple, Tuple, TypeAlias, Any
from enum import Enum, auto
from decimal import Decimal


class Node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def eval(self) -> Decimal:
        raise NotImplementedError


Calculated: TypeAlias = Any


class AstElement(Protocol):
    def eval(self) -> Calculated:
        ...


ResultValue: TypeAlias = (
    str | int | float | Decimal | AstElement | None |
    Tuple["ResultValue", "ResultValue"]
)


class Tag(Enum):
    RESERVED = auto()
    INT = auto()


class Token(NamedTuple):
    value: str | int | float | Decimal
    tag: Tag
