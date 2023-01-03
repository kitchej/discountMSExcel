from datetime import datetime
from decimal import Decimal, InvalidOperation
import math


def _sum(values_list):
    if len(values_list) <= 1:
        return 'ERROR'
    try:
        values_list = [Decimal(i) for i in values_list]
    except InvalidOperation:
        return 'ERROR'
    return sum(values_list)


def difference(values_list):
    if len(values_list) <= 1:
        return 'ERROR'
    try:
        out = Decimal(values_list[0])
    except InvalidOperation:
        return 'ERROR'
    for value in values_list[1:len(values_list)]:
        try:
            value = Decimal(value)
        except InvalidOperation:
            return 'ERROR'
        out -= value
    return out


def product(values_list):
    if len(values_list) <= 1:
        return 'ERROR'
    out = 1
    for value in values_list:
        try:
            value = Decimal(value)
        except InvalidOperation:
            return 'ERROR'
        out *= value
    return out


def quotient(values_list):
    if len(values_list) <= 1:
        return 'ERROR'
    try:
        lhs = Decimal(values_list[0])
        rhs = Decimal(values_list[1])
    except InvalidOperation:
        return 'ERROR'

    out = lhs / rhs
    for value in values_list[2:len(values_list)]:
        try:
            value = Decimal(value)
        except InvalidOperation:
            return 'ERROR'
        out /= value
    return out


def floor(value: str):
    try:
        value = Decimal(value)
    except InvalidOperation:
        return 'ERROR'
    return math.floor(value)


def ceiling(value: str):
    try:
        value = Decimal(value)
    except InvalidOperation:
        return 'ERROR'
    return math.ceil(value)


def trunc(value: str):
    try:
        value = Decimal(value)
    except InvalidOperation:
        return 'ERROR'
    return math.trunc(value)


def _round(value: str, precision: str):
    if isinstance(precision, float) or '.' in precision:
        return 'ERROR'
    try:
        precision = int(precision)
    except ValueError:
        return 'ERROR'
    try:
        value = Decimal(value)
    except InvalidOperation:
        return 'ERROR'
    return round(value, precision)


def average(values_list):
    if len(values_list) == 0:
        return 'ERROR'
    else:
        try:
            values_list = [Decimal(i) for i in values_list]
        except InvalidOperation:
            return 'ERROR'
        return Decimal(sum(values_list)) / Decimal(len(values_list))


def now(_format):
    out = datetime.now().strftime(_format)
    if out == '':
        return 'ERROR'
    else:
        return out



if __name__ == '__main__':
    print(quotient(['10', '20', '30', '40']))