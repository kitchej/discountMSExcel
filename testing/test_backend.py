import backend.equations as equ
from decimal import Decimal


def test_sum():
    assert equ.get_sum(['10', 'twenty', '30', '40']) == 'ERROR'
    assert equ.get_sum(['10', '2']) == Decimal('12')
    assert equ.get_sum(['10', '20', '30', '40']) == ((Decimal('10') + Decimal('20')) + Decimal('30')) + Decimal('40')
    assert equ.get_sum(['10.45', '20.698', '30.547', '40.1']) == \
           ((Decimal('10.45') + Decimal('20.698')) + Decimal('30.547')) + Decimal('40.1')


def test_diff():
    assert equ.get_difference(['10', 'twenty', '30', '40']) == 'ERROR'
    assert equ.get_difference(['ten', '20', '30', '40']) == 'ERROR'
    assert equ.get_difference(['10', '2']) == Decimal('8')
    assert equ.get_difference(['10', '20', '30', '40']) == ((Decimal('10') - Decimal('20')) - Decimal('30')) - Decimal('40')
    assert equ.get_difference(['10.45', '20.698', '30.547', '40.1']) == \
           ((Decimal('10.45') - Decimal('20.698')) - Decimal('30.547')) - Decimal('40.1')


def test_prod():
    assert equ.get_product(['10', 'twenty', '30', '40']) == 'ERROR'
    assert equ.get_product(['10', '2']) == Decimal('20')
    assert equ.get_product(['10', '20', '30', '40']) == ((Decimal('10') * Decimal('20')) * Decimal('30')) * Decimal('40')
    assert equ.get_product(['10.45', '20.698', '30.547', '40.1']) == \
           ((Decimal('10.45') * Decimal('20.698')) * Decimal('30.547')) * Decimal('40.1')


def test_quot():
    assert equ.get_quotient(['10', 'twenty', '30', '40']) == 'ERROR'
    assert equ.get_quotient(['10', '2']) == Decimal('5')
    assert equ.get_quotient(['10', '20', '30', '40']) == ((Decimal('10') / Decimal('20')) / Decimal('30')) / Decimal('40')
    assert equ.get_quotient(['10.45', '20.698', '30.547', '40.1']) == \
           ((Decimal('10.45') / Decimal('20.698')) / Decimal('30.547')) / Decimal('40.1')


def test_floor():
    assert equ.get_floor('fifty point two five') == 'ERROR'
    assert equ.get_floor('50.2541') == Decimal('50')
    assert equ.get_floor('104.2') == Decimal('104')
    assert equ.get_floor('26.65987542126598745') == Decimal('26')
    assert equ.get_floor('26.65987542126598745') == Decimal('26')
    assert equ.get_floor('45.345') == Decimal('45')
    assert equ.get_floor('-45.345') == Decimal('-46')


def test_ceil():
    assert equ.get_ceiling('fifty point two five') == 'ERROR'
    assert equ.get_ceiling('50.2541') == Decimal('51')
    assert equ.get_ceiling('104.2') == Decimal('105')
    assert equ.get_ceiling('26.65987542126598745') == Decimal('27')
    assert equ.get_ceiling('26.65987542126598745') == Decimal('27')
    assert equ.get_ceiling('45.345') == Decimal('46')
    assert equ.get_ceiling('-45.345') == Decimal('-45')


def test_trunc():
    assert equ.get_trunc('fifty point two five') == 'ERROR'
    assert equ.get_trunc('50.2541') == Decimal('50')
    assert equ.get_trunc('104.2') == Decimal('104')
    assert equ.get_trunc('26.65987542126598745') == Decimal('26')
    assert equ.get_trunc('26.65987542126598745') == Decimal('26')
    assert equ.get_trunc('-45.345') == Decimal('-45')


def test_round():
    assert equ.get_round('50.25', '2.5') == 'ERROR'
    assert equ.get_round('50.25', 2.5) == 'ERROR'
    assert equ.get_round('50.2541', '2') == Decimal('50.25')
    assert equ.get_round('104.2', '1') == Decimal('104.2')
    assert equ.get_round('26.65987542126598745', '1') == Decimal('26.7')
    assert equ.get_round('26.65987542126598745', '4') == Decimal('26.6599')
    assert equ.get_round('-45.345', '2') == Decimal('-45.34')


def test_avg():
    assert equ.get_average([]) == 'ERROR'
    assert equ.get_average(['1', '2', '3', 'four']) == 'ERROR'
    assert equ.get_average(['45', '52', '41', '63', '45', '46']) == \
           (Decimal('45') + Decimal('52') + Decimal('41') + Decimal('63') + Decimal('45') + Decimal('46')) / Decimal('6')
    assert equ.get_average(['1005.24', '2006.37', '1205.13', '1996.21', '1500.56', '46.58']) == \
           (Decimal('1005.24') + Decimal('2006.37') + Decimal('1205.13') + Decimal('1996.21') + Decimal('1500.56') + Decimal('46.58')) / Decimal('6')
    assert equ.get_average(['-1005.24', '2006.37', '-1205.13', '1996.21', '1500.56', '-46.58']) == \
           (Decimal('-1005.24') + Decimal('2006.37') + Decimal('-1205.13') + Decimal('1996.21') + Decimal(
               '1500.56') + Decimal('-46.58')) / Decimal('6')
    assert equ.get_average(['623.45653', '589.2365', '589.23659875', '490.2323245', '610.7', '503.2493156']) == \
           (Decimal('623.45653') + Decimal('589.2365') + Decimal('589.23659875') + Decimal('490.2323245') + Decimal(
               '610.7') + Decimal('503.2493156')) / Decimal('6')


def test_now():
    assert equ.get_current_date("%m/%/%y") == 'ERROR'
