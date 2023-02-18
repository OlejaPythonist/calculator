from functools import reduce
from typing import Callable, Literal, TypeAlias
from decimal import Decimal

from types_ import AstElement
from parser_combinator import (
    Parser,
    Reserved,
    Number,
    Lazy,
    Phrase,
)
from nodes import BinOperationNode


PLUS, MINUS = Reserved("+"), Reserved("-")
TIMES, DIVIDE = Reserved("*"), Reserved("/")
LPAREN, RPAREN = Reserved("("), Reserved(")")


ParenthisExpression: TypeAlias = (
    tuple[tuple[Literal["("], AstElement], Literal[")"]]
)


def parenthis_parse(
        expr: ParenthisExpression) -> AstElement:
    ((_, response), _) = expr
    return response


def factor() -> Parser:
    return (
        Number() |
        (LPAREN + Lazy(expression) + RPAREN) ^ parenthis_parse
    )


BinNumbers: TypeAlias = float | int | Decimal


def bin_operation(
        operator: str) -> Callable[[BinNumbers, BinNumbers], BinOperationNode]:
    return (lambda left, right: BinOperationNode(operator, left, right))


def any_operator_in_list(operators: list[str]) -> Parser:
    operators_parsers: list[Parser] = (
        [Reserved(operator) for operator in operators]
    )
    parser = reduce(
        (lambda left, right: left | right),
        operators_parsers
    )
    return parser


def get_precedence() -> list[list[str]]:
    return [
        ["^", ],
        ["*", "/"],
        ["+", "-"],
    ]


Combine: TypeAlias = (
    Callable[[str], Callable[[BinNumbers, BinNumbers], BinOperationNode]]
)


def operator_parser(precedence_level: list[str], combine: Combine) -> Parser:
    return any_operator_in_list(precedence_level) ^ combine


def precedence(
        value_parser: Parser,
        precedence_levels: list[list[str]],
        combine: Combine) -> Parser:
    parser = value_parser * operator_parser(precedence_levels[0], combine)

    for precedence_level in precedence_levels[1:]:
        parser = parser * operator_parser(precedence_level, combine)

    return parser


def expression() -> Parser:
    return precedence(
            factor(),
            get_precedence(),
            bin_operation
    )


def parser() -> Phrase:
    return Phrase(expression())
