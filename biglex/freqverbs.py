#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import time
import datetime

freqverbs = open('norgramverb.txt')


verbs = set([])
for line in freqverbs:
    if not line[:1] == '#':
        items = line.split('\t')
        if len(items) == 2:
            num = int(items[0])
            stem = items[1][:-1]
            if '-' in stem:
                stems = stem.split('-')
                stem = stems[0]
            if '*' in stem:
                stems = stem.split('*')
                stem = stems[0]
            if '&' in stem:
                stems = stem.split('&')
                stem = stems[0]
            if '#' in stem:
                stems = stem.split('*')
                stem = stems[0]
            
            if num > 1:
                verbs.add(stem)

print len(verbs)

inverb = False
verbentry = ''
entries = []
nklIN=open('../nkl.tdl','r')
for line in nklIN:
    if '_v := main-verb-lxm' in line:
        inverb = True
        verbitems = line.split('_')
        vstem = verbitems[0]
    if inverb:
        verbentry = verbentry + line
    else:
        entries.append(line)
    if '_v ].' in line:
        inverb = False
        if vstem in verbs:
            entries.append(verbentry)
        verbentry = ''
        
        
    

nklOUT=open('../nkl-mid.tdl','w')
for line in entries:
    nklOUT.write(line)


predsIN=open('../preds.tdl','r')
predsOUT=open('../preds-mid.tdl','w')
for line in predsIN:
    if '_v ' in line:
        items = line.split()
        for item in items:
            if item[-2:] == '_v':
                stem = item[:-2]
                if stem in verbs:
                    predsOUT.write(line)
    elif not 'aldri_adv' in line:
        predsOUT.write(line)
            
trigg=True
triggerIN=open('../trigger.mtr','r')
triggerOUT=open('../trigger-mid.mtr','w')
for line in triggerIN:
    if '-v_rule' in line:
        trigg=False
        items = line.split('_')
        stem = items[0]
    elif '_v_rule' in line:
        trigg=True
        items = line.split('_')
        stem = items[0]
        if stem in verbs:
            triggerOUT.write(line)
    elif '_v ' in line:
        if stem in verbs and trigg:
            triggerOUT.write(line)
    elif '_v"' in line:
        if stem in verbs and trigg:
            triggerOUT.write(line)
        
    else:
        triggerOUT.write(line)
            
                
        
