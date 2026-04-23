#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collections import Counter
import itertools

frames = open('../preds-small.tdl')
frames2 = open('../preds-mid.tdl')
frames3 = open('../nor.tdl')

partcount = {}
prepset = set([])
allLines = []
for line in frames:
    if ' := ' in line and '*' in line:
        allLines.append(line)
for line in frames2:
    if ' := ' in line and '*' in line:
        allLines.append(line)
for line in frames3:
    if ' := ' in line and '*' in line:
        allLines.append(line)

for line in allLines:
    items = line.split()
    head = items[0]
    items = head.split('*')
    if '-' in items[0]:
        part = items[0].split('-')[1]
        prep = items[1].split('_')[0]
        if '-' in prep:
            prep = prep.split('-')[0]
        prepset.add(prep)
        partcount[part] = partcount.get(part,0)+1

def sortfunc(x,y):
    return cmp(y[1],x[1])
items=partcount.items()
items.sort(sortfunc)
for item in items:
    if item[0] in prepset:
        print item[0],
        print item[1]
