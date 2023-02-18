from decimal import Decimal
from lexer import arithmetic_lex
from arithmetic_parser import parser
from types_ import Node


def solve(chars: str) -> Decimal | None:
    tokens = arithmetic_lex(chars)
    result = parser()(tokens, 0)
    if not result:
        return None
    else:
        value = result.value

    if value and isinstance(value, Node):
        return value.eval()
    elif isinstance(value, (int, float, Decimal)):
        return Decimal(value)
    else:
        return None


if __name__ == "__main__":
    while 1:
        print(solve(input()))
