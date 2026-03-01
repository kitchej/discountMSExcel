from datetime import datetime
import decimal
import math


def get_sum(args):
    if len(args) == 0:
        return 'ERROR'
    try:
        args = [decimal.Decimal(i) for i in args]
    except decimal.InvalidOperation:
        return 'ERROR'
    return sum(args)


def get_difference(args):
    if len(args) == 0:
        return 'ERROR'
    try:
        out = decimal.Decimal(args[0])
    except decimal.InvalidOperation:
        return 'ERROR'
    for value in args[1:len(args)]:
        try:
            value = decimal.Decimal(value)
        except decimal.InvalidOperation:
            return 'ERROR'
        out -= value
    return out


def get_product(args):
    if len(args) == 0:
        return 'ERROR'
    out = 1
    for value in args:
        try:
            value = decimal.Decimal(value)
        except decimal.InvalidOperation:
            return 'ERROR'
        out *= value
    return out


def get_quotient(args):
    if len(args) == 0:
        return 'ERROR'
    try:
        lhs = decimal.Decimal(args[0])
        rhs = decimal.Decimal(args[1])
    except decimal.InvalidOperation:
        return 'ERROR'

    out = lhs / rhs
    for value in args[2:len(args)]:
        try:
            value = decimal.Decimal(value)
        except decimal.InvalidOperation:
            return 'ERROR'
        out /= value
    return out


def get_floor(args):
    if len(args) != 1:
        return 'ERROR'
    try:
        value = decimal.Decimal(args[0])
    except decimal.InvalidOperation:
        return 'ERROR'
    decimal.getcontext().rounding = decimal.ROUND_FLOOR
    return round(value, 0)


def get_ceiling(args):
    if len(args) != 1:
        return 'ERROR'
    try:
        value = decimal.Decimal(args[0])
    except decimal.InvalidOperation:
        return 'ERROR'
    decimal.getcontext().rounding = decimal.ROUND_CEILING
    return round(value, 0)


def get_trunc(args):
    if len(args) != 1:
        return 'ERROR'
    try:
        value = int(args[0])
    except decimal.InvalidOperation:
        return 'ERROR'
    return value


def get_round(args):
    if len(args) != 2:
        return 'ERROR'
    try:
        value = decimal.Decimal(args[0])
    except decimal.InvalidOperation:
        return 'ERROR'
    try:
        precision = int(args[1])
    except ValueError:
        return 'ERROR'
    decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
    return round(value, precision)


def get_average(args):
    if len(args) == 0:
        return 'ERROR'
    else:
        try:
            args = [decimal.Decimal(i) for i in args]
        except decimal.InvalidOperation:
            return 'ERROR'
        return decimal.Decimal(sum(args)) / decimal.Decimal(len(args))


def get_current_date(args):
    if len(args) != 1:
        return 'ERROR'
    out = datetime.now().strftime(args[0])
    if out == '' or "%" in out:
        return 'ERROR'
    else:
        return out



if __name__ == '__main__':
    print(get_quotient(['10', '20', '30', '40']))