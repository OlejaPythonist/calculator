import abc
from typing import Callable, Any
from types_ import Token, Tag, ResultValue


class Result:
    def __init__(self, value: ResultValue, position: int) -> None:
        self.value = value
        self.position = position

    def __repr__(self) -> str:
        return f"Result(value={self.value}, position={self.position})"


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        raise NotImplementedError

    def __add__(self, other: "Parser") -> "Concat":
        return Concat(self, other)

    def __mul__(self, other: "Parser") -> "Exp":
        return Exp(self, other)

    def __or__(self, other: "Parser") -> "Alternative":
        return Alternative(self, other)

    def __xor__(self, function: Callable[[Any], Any]) -> "Process":
        return Process(self, function)


class Reserved(Parser):
    def __init__(self, value: str) -> None:
        self.value = value

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        if position < len(tokens) and tokens[position][0] == self.value:
            return Result(tokens[position][0], position + 1)
        return None


class Number(Parser):
    def __init__(self) -> None:
        pass

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        if position < len(tokens) and\
                tokens[position][1] == Tag.INT:
            return Result(tokens[position][0], position + 1)
        return None


class Concat(Parser):
    def __init__(
            self,
            left: Parser,
            right: Parser) -> None:
        self.left = left
        self.right = right

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        left_result = self.left(tokens, position)
        if left_result:
            right_result = self.right(tokens, left_result.position)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.position)
        return None


class Exp(Parser):
    def __init__(
            self,
            parser: Parser,
            separator: Parser) -> None:
        self.parser = parser
        self.separator = separator

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        if not (result := self.parser(tokens, position)):
            return result

        SeparatorFunction = Callable[[ResultValue, ResultValue], ResultValue]
        Parsed = tuple[SeparatorFunction, ResultValue]
        def process_next(
                parsed: Parsed) -> ResultValue:
            sepfunc, right = parsed
            if result is None:
                return result
            return sepfunc(result.value, right)

        next_parser = (self.separator + self.parser) ^ process_next
        next_result: Result | None = result
        while next_result:
            next_result = next_parser(tokens, result.position)
            if next_result:
                result = next_result
        return result


class Alternative(Parser):
    def __init__(
            self,
            left: Parser,
            right: Parser) -> None:
        self.left = left
        self.right = right

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        left_result = self.left(tokens, position)
        if left_result:
            return Result(left_result.value, left_result.position)
        right_result = self.right(tokens, position)
        if right_result:
            return Result(right_result.value, right_result.position)
        return None


class Process(Parser):
    def __init__(
            self,
            parser: Parser,
            function: Callable[[Any], Any]) -> None:
        self.parser = parser
        self.function = function

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        result = self.parser(tokens, position)
        if result:
            result.value = self.function(result.value)
            return result
        return None


class Lazy(Parser):
    def __init__(self, parser_func: Callable[[], Parser]) -> None:
        self.parser: Parser | None = None
        self.parser_func = parser_func

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, position)


class Phrase(Parser):
    def __init__(
            self,
            parser: Parser) -> None:
        self.parser = parser

    def __call__(
            self,
            tokens: list[Token],
            position: int) -> Result | None:
        result = self.parser(tokens, position)
        if result and result.position == len(tokens):
            return result
        return None
