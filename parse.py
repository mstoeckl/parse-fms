#!/usr/bin/env python3

import re
import os,sys
from collections import defaultdict

# DATA

trigger = "#FRC"
# MICMP TY P MC 43 RF 312 BF 0 RA 3604 1506 314 BA 33 4391 1189 RFP 0  BFP 0  RHS 0  BHS 0  RTS 312 BTS 0
# 0     1  2 3  4  5  6   7  8 9  10   11   12  13 14 15   16   17  18 19  20 21  22 23  24 25  26  27  28
rules = {0:"Key",
        2:"Type",
        4:"No.",
        6:"RedPts",
        8:"BluPts",
        10:"Red1",
        11:"Red2",
        12:"Red3",
        14:"Blu1",
        15:"Blu2",
        16:"Blu3",
        18:"RedFoul",
        20:"BluFoul",
        22:"RedAuto",
        24:"BluAuto",
        26:"RedTele",
        28:"BluTele"}

# CODE

def hook(output, data, rules):
    for k in rules:
        output[rules[k]].append(data[k])

def toTSV(name, key):
    dat = defaultdict(list)
    text = map(lambda u: u.split(), open(name).read().split(trigger)[1:])
    for block in text:
        if key is None or block[0] == key:
            hook(dat, block[0:29], rules)
    return dat

def printTSV(doc):
    fields = list(map(lambda i: rules[i], sorted(rules.keys())))
    l = len(next(iter(doc.values())))
    print("\t".join(fields))
    for i in range(l):
        jk = [str(doc[k][i]) for k in fields]
        print("\t".join(jk))

if __name__ == "__main__":
    args = sys.argv[1:]
    name = args[0]
    if len(args) > 1:
        key = args[1]
    else:
        key = None
    printTSV(toTSV(name, key))
