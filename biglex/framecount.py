#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collections import Counter
import itertools

frames = open('../preds.tdl')
frames2 = open('../nor.tdl')
pred2frames = {}
pred2all = {}
frames2count = {}
x = 0
verbs = set([])
listoflists = []
for line in frames:
    if ' := ' in line:
        items = line.split()
        pred = items[2]
        if pred[-2:] == '_v':
            pred2frames[pred] = pred2frames.get(pred,0)+1
            y=len(pred)
            pred2all[pred] = pred2all.get(pred,[])+[items[0][y:]]
            x = x+1
            verbs.add(pred)
for line in frames2:
    if ' := ' in line:
        items = line.split()
        pred = items[2]
        if pred[-2:] == '_v':
            pred2frames[pred] = pred2frames.get(pred,0)+1
            y=len(pred)
            pred2all[pred] = pred2all.get(pred,[])+[items[0][y:]]
            x = x+1
            verbs.add(pred)
def sortfunc(x,y):
	return cmp(x[1],y[1])
items=pred2frames.items()
items.sort(sortfunc)
for item in items:
    frames=item[1]
    frames2count[frames] = frames2count.get(frames,0)+1

def sortfunc(x,y):
	return cmp(x[0],y[0])
items=frames2count.items()
items.sort(sortfunc)
for item in items:
    print item
print x
print len(verbs)

frameComb = {}
# for item in pred2all:
#     frames = pred2all[item]
#     if len(frames) > 1:
#         cpframes = frames[:]
#         for frame in frames:
#             newframes = cpframes[:]
#             for newframe in newframes:
#                 if not newframe == frame:
#                     comb = frame + ' ' + newframe
#                     if not newframe + ' ' + frame in frameComb.keys():
#                         frameComb[comb] = frameComb.get(comb,0) +1

def sortfunc(x,y):
	return cmp(x[1],y[1])
items=frameComb.items()
items.sort(sortfunc)

for item in items:
    print item

print 'test '
for key in pred2all.keys():
#    if '1_rel' in pred2all[key] and '12_rel' in pred2all[key] and 'opp_12_rel' in pred2all[key] and 'refl_1_rel' in pred2all[key] and 'ut_12_rel' in pred2all[key] and 'på_14_rel' in pred2all[key]:
#    if '1_rel' in pred2all[key] and 'refl_1_rel' in pred2all[key] and 'ned_12_rel' in pred2all[key] and 'på_14_rel' in pred2all[key]:
#        print key
    listoflists.append(pred2all[key])
    

def get_three_item_combinations(lists):
    combinations = []
    for lst in lists:
        if len(lst) >= 4:
            for combination in itertools.combinations(lst, 4):
                combinations.append(combination)
    return combinations

def rank_combinations(combinations):
    counter = Counter(combinations)
    ranked_combinations = counter.most_common()
    return ranked_combinations


lists = listoflists

if lists:
    combinations = get_three_item_combinations(lists)
    ranked_combinations = rank_combinations(combinations)
        
    print("Ranked combinations by frequency:")
    for combination, frequency in ranked_combinations:
        print("Items: " + ', '.join(combination) + " \t Frequency: " + str(frequency))
        if frequency == 5:
            print combination
            for key in pred2all.keys():
                if combination[0] in pred2all[key] and combination[1] in pred2all[key] and combination[2] in pred2all[key] and combination[3] in pred2all[key]:
                    print key


        


#    for frame in item[1]:
#        print frame

