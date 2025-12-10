from typing import Sequence


class OperationError(Exception):
    pass


def apply_operation(operation: str, values: Sequence[float]) -> float:
    if len(values) != 2:
        raise OperationError("Exactly two operands are required")

    a, b = values

    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise OperationError("Division by zero")
        return a / b

    raise OperationError(f"Unsupported operation: {operation}")

