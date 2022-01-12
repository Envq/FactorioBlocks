#!/usr/bin/env python3
import math


def mcm(a, b):
    a = int(a)
    b = int(b)
    return (a*b)//math.gcd(a,b)


def dictMerge(a, b, delete=None):
    c = dict()
    for k,v in a.items():
        if k != delete:
            c[k] = v
    for k,v in b.items():
        if k != delete:
            if k in c:
                c[k] = c[k] + v
            else:
                c[k] = v
    return c


def getCommonLine(blockIN, blockOUT):
    for e in blockIN.outputs:
        for f in blockOUT.inputs:
            if e == f:
                return e
    return None