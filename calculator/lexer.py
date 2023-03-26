import re
from types_ import Token, Tag
from errors import IllegalCharacter


NUMBER = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))


def arithmetic_lex(chars: str) -> list[Token]:
    tokens: list[Token] = []
    position = 0
    max_position = len(chars)
    while position < max_position:
        if chars[position] in (" ", "\t", "\n"):
            position += 1

        elif chars[position] in ("+", "-", "*", "/", "^", "(", ")"):
            tokens.append(Token(chars[position], Tag.RESERVED))
            position += 1

        elif (num := NUMBER.match(chars, position)):
            integer, float_, exp = num.groups(default=None)
            if integer and\
                    (float_ or exp):
                result = float(f"{integer}{(float_ or '')}{exp or ''}")
            elif integer:
                result = int(integer)
            else:
                result = None

            if result:
                tokens.append(Token(result, Tag.INT))
                position = num.end()

        else:
            raise IllegalCharacter(
                f"position: {position}, "
                f"char: {chars[position]}"
            )
    return tokens
