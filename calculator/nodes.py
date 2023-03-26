import decimal
from decimal import Decimal
from types_ import Node


decimal.getcontext().prec = 10


class BinOperationNode(Node):
    def __init__(
            self,
            operator: str,
            left: float | int | Decimal,
            right: float | int | Decimal) -> None:
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"BinOperationNode({self.operator}, {self.left}, {self.right})"

    def eval(self) -> Decimal:
        operator = self.operator
        left_value = Decimal(self.left)\
            if not isinstance(self.left, Node) else Decimal(self.left.eval())
        right_value = Decimal(self.right)\
            if not isinstance(self.right, Node) else Decimal(self.right.eval())
        match operator:
            case "+":
                value = left_value + right_value
            case "-":
                value = left_value - right_value
            case "*":
                value = left_value * right_value
            case "/":
                value = left_value / right_value
            case "^":
                value = left_value ** right_value
            case _:
                raise RuntimeError("Unknown operator: " + self.operator)
        return value
