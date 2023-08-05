from dummy.add import add
from dummy.mul import mul
from dummy.sub import sub


def calc(n1, op, n2):
    """
    The function ``calc`` performs a computation combining numbers n1, n2
    with the operation 'op'.

    :param: n1: The first number (left hand side of operation)
    :param: op: The operation to perform
    :param: n2: The second number (right hand side of operation)
    """
    if op == '+':
        return add(n1, n2)
    elif op == '-':
        return sub(n1, n2)
    elif op in ['*', 'x', '.']:
        return mul(n1, n2)
    else:
        raise Exception('dummy does not support this operation: ' + str(op))
