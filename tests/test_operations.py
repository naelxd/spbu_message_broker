import pytest

from common.operations import OperationError, apply_operation


@pytest.mark.parametrize(
    "operation,values,expected",
    [
        ("add", [1, 2], 3),
        ("subtract", [5, 3], 2),
        ("multiply", [2, 4], 8),
        ("divide", [8, 2], 4),
    ],
)
def test_apply_operation_success(operation, values, expected):
    assert apply_operation(operation, values) == expected


def test_apply_operation_unsupported():
    with pytest.raises(OperationError):
        apply_operation("power", [2, 3])


def test_apply_operation_divide_by_zero():
    with pytest.raises(OperationError):
        apply_operation("divide", [1, 0])
