#!/usr/bin/env python3
import math


def lcm(x, y):
    """Return the least common multiple of x and y."""
    x = int(x)
    y = int(y)
    return (x*y) // math.gcd(x, y)


def gcd(*args):
    res = args[0]
    for e in args[1:]:
        res = math.gcd(res, e)
    return res


def getSmallestFactor(x, limit=100):
    """Given a float number, return the smallest number which,
       multiplied by x, gives an integer."""
    for i in range(1, limit):
        if float(x*i).is_integer():
            return i
    raise RuntimeError(f'The smaller factor exceeds the limit of {limit}.')


def dictMerge(x, y, ignoreKey=None):
    """Return the dict of the union of x with y,
       adding the values of same keys. Ignore ignoreKey."""
    c = dict()
    for k,v in x.items():
        if k != ignoreKey:
            c[k] = v
    for k,v in y.items():
        if k != ignoreKey:
            if k in c:
                c[k] = c[k] + v
            else:
                c[k] = v
    return c


def getCommonLine(blockIN, blockOUT):
    """Return the common line i.e: the output of blockIn with
       the same type of an input of blockOut."""
    for e in blockIN.outputs:
        for f in blockOUT.inputs:
            if e == f:
                return e
    return None



# TEST
if __name__ == "__main__":
    # Test1
    to_delete = "HeavyOil"
    in1 =  {"HeavyOil": 40,"Water": 30}
    in2 =  {"Water": 30}
    res = dictMerge(in1, in2, to_delete)
    assert res == {'Water': 60}

    # Test2
    assert 2 == getSmallestFactor(0.5)
    assert 2 == getSmallestFactor(1.5)
    assert 10 == getSmallestFactor(0.1)
    assert 4 == getSmallestFactor(0.25)

    # Test3
    assert 2 == gcd(4,2,8)
    assert 4 == gcd(4,8)
    assert 2 == gcd(*{4,2,8})

    print('Successful Tests!')