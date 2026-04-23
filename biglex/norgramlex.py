#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import time
import datetime

dark = True
dark = False

f = open('/home/petter/xle/pargram/norwegian/bokmal/bokmal-lex-mrs.lfg')
g = open('/home/petter/xle/pargram/norwegian/bokmal/bokmal-nklvrblex.lfg')
gg = open('/home/petter/xle/pargram/norwegian/bokmal/bokmal-nkllex.lfg')
h = open('/home/petter/xle/pargram/norwegian/bokmal/bokmal-titles.lfg')
sub= open('/home/petter/xle/pargram/norwegian/bokmal/subtree-features.txt')
#reltypesTinyOUT=open('../reltypes-tiny.tdl','w')
reltypesSmallOUT=open('../reltypes-small.tdl','w')
funclexOUT=open('../funclex.tdl','w')
#reltypesOUT=open('../reltypes.tdl','w')
predsOUT=open('../preds.tdl','w')
generationOUT=open('../generation.tdl','w')
predsSmallOUT=open('../preds-small.tdl','w')
functriggerOUT=open('../functrigger.mtr','w')
#triggerTinyOUT=open('../trigger-tiny.mtr','w')
triggerSmallOUT=open('../trigger-small.mtr','w')
triggerOUT=open('../trigger.mtr','w')
triggerBaseIN=open('trigger-base.mtr')
tinylexIN=open('../tinylex.tdl')
lexiconIN=open('../lexicon.tdl')
norIN=open('../nor.tdl')
linktypesIN=open('../../resources/nkl/linktypes.tdl')
#linktypesOUT=open('../linktypes-mwe.tdl','w')
nklfuncrelsIN=open('../../resources/nkl/nkl-funcrels.tdl')
#nklfuncrelsOUT=open('../nkl-funcrels-mwe.tdl','w')
#verbrelsOUT=open('../verbrels.tdl','w')
verbsDarkOUT = open('../verbs-dark.tdl','w')
out=''

predsOUT.write(';;  -*- Mode: TDL; Coding: utf-8; -*- \n;;\n')
predsOUT.write(';;  Type file automatically derived from \n;;  Norsk Komputasjonelt Leksikon and NorGram (')
predsOUT.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
predsOUT.write(';;  See \'license.txt\' for licence conditions\n;;\n\n')

predsSmallOUT.write(';;  -*- Mode: TDL; Coding: utf-8; -*- \n;;\n')
predsSmallOUT.write(';;  Type file automatically derived from \n;;  Norsk Komputasjonelt Leksikon and  NorGram (')
predsSmallOUT.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
predsSmallOUT.write(';;  See \'license.txt\' for licence conditions\n;;\n\n')

def removecomment(infile):
    nocomm = ''
    incomment = False
    for line in infile:
        for char in line:
            if char == '"' and incomment == False:
                incomment = True
            elif char == '"' and incomment == True:
                incomment = False
            if not char == '"' and incomment == False:
                nocomm = nocomm+char
    return nocomm
out = out + removecomment(f)
out = out + removecomment(g)
out = out + removecomment(gg)
#out = out + removecomment(h)

out = " ".join(out.split())
import re
entries = re.split('ONLY.|ETC.',out)
catcount = {}
framecount = {}
catset = set([])
lexicon = {}
frameset=set([])
funcwords=set(['rett'])
qwords=set([])
prps=set([])
postps=set([])
pvbobjs=set([])
ijs=set([])
cadvs=set([])
prts=set([])
advs=set([])
sadvs=set([])
degadvs=set(['rett'])
deglocs=set(['rett'])
degnums=set([])
degqnts=set([])
ttls=set([])
ttlnums=set([])
qs={}
degrees={}
adjs=set([])
nouns=set([])
idiomnouns=set([])
intrans=set([])
trans=set([])
skipwords=set(['være'])
singleframes = set([''])
uniqentries = set([])
allprds=set([])
verbrels=set([])
massnouns = set([])
countnouns = set([])
templocnouns = set([])

for entry in entries[1:]:
    entryitems = entry.split('-<')
    entry = entryitems[0]
    entry = entry.replace('` ','*')
    entry = entry.replace('`','*')
    entry = entry.replace('.','PERIOD')
    entry = entry.replace('/','SLASH')
    items = entry.split()
    lexid = items[0]
    lexid = lexid.lower()
    body = " ".join(items[1:])
    categories = body.split(';')
    for category in categories:
        catlist = category.split()
        if len(catlist) > 0 and not lexid in skipwords and not lexid+category in uniqentries and not 'FALSE' in category:
#        try:
            cat = catlist[0]
            catcount[cat] = catcount.get(cat,0)+1
            catset=set(['PRT', 'P', 'Pabs', 'Ppost', 'DApost', 'ADVqnt', 'ADV', 'ADVatt', 'ADVloc', 'ADVs', 'ADVcmt', 'ADVprt', 'ADVneg', 'ADVdeg', 'TTL', 'TTLnum', 'ADVdegloc', 'ADVdegnum', 'ADVdegqnt', 'Cadv','Pvbobj','Pvbobj'])
            if cat in catset and not 'BOKMAL' in lexid and not 'FALSE' in category and not lexid == '----' and not '<' in lexid:
                allprds.add(lexid)
                funcwords.add(lexid)
                catset.add(cat)
                if cat == 'ADVdeg':
                    degadvs.add(lexid)
                if cat == 'ADVdegloc':
                    deglocs.add(lexid)
                if cat == 'ADVdegnum':
                    degnums.add(lexid)
                if cat == 'ADVdegqnt':
                    degqnts.add(lexid)
                if cat == 'TTLnum':
                    ttlnums.add(lexid)
                if cat == 'TTL':
                    ttls.add(lexid)
                if cat == 'ADVs' or cat == 'ADVneg' or cat == 'ADVcmt' or cat == 'ADVprt':
                    sadvs.add(lexid)
                if cat == 'PRT':
                    prts.add(lexid)
                if cat == 'Cadv':
                    cadvs.add(lexid)
                if cat == 'P':
                    prps.add(lexid)
                if cat == 'Ppost' or cat == 'DApost' or cat == 'ADVqnt':
                    postps.add(lexid)
                if cat == 'Pvbobj':
                    pvbobjs.add(lexid)
                if cat == 'ADV' or cat == 'ADVloc' or cat == 'ADVatt' or cat == 'Pabs':
                    advs.add(lexid)
            frames = " ".join(catlist[2:])
            if cat == 'ADVdeg':
                allprds.add(lexid)
                if '(^ DEGREE)=positive' in frames:
                    degrees[lexid]=degrees.get(lexid , []) + ['pos']
                if '(^ DEGREE)=comparative' in frames:
                    degrees[lexid]=degrees.get(lexid , []) + ['cmp']
                if '(^ DEGREE)=superlative' in frames:
                    degrees[lexid]=degrees.get(lexid , []) + ['sup']
            if cat == 'Q':
                allprds.add(lexid)
                if ' (^ NTYPE NSEM COMMON)=mass' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['mass']
                if ' @FEM' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['fem']
                if ' @COMMON' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['comm']
                if ' @NEUT' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['neut']
                if ' (^ NUM)=sg' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['sg']
                if ' (^ NUM)=pl' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['pl']
                if '~(^ DEF)=+' in frames:
                    qs[lexid]=qs.get(lexid , []) + ['indef']
            if cat == 'INTERJ':
                allprds.add(lexid)
                ijs.add(lexid)
            if cat == 'V' or cat == '+V' or cat == 'A' or cat == 'N' or cat == '+N':
                allprds.add(lexid)
                if '{' in frames:
                    if frames[0] == '{':
                        framelist = frames[1:-1].split('|')
                    else:
                        framelist = frames.split('{')[1][:-1].split('|')
                else:
                    framelist = [frames]
                framelen = len(framelist)
                for frame in framelist:
                    try:
                        frameitems = re.split('\(|\)',frame)[1].split()
                    except:
                        pass
                    framename = frameitems[0]
                    framecount[framename] = framecount.get(framename,0)+1
                    preds = frameitems[2:]
                    if len(preds) > 1:
                        preds[1] = preds[1].split('`')[0]
                        preds[1] = preds[1].split('&')[0]
                        preds[1] = preds[1].split('*')[0]
                    if len(preds) > 2 :
                        preds[2] = preds[2].split('`')[0]
                        preds[2] = preds[2].split('&')[0]
                        preds[2] = preds[2].split('*')[0]

                    if framename == 'V-SUBJexpl':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_0_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ':
                        #lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & arg4- & prt-.']
                        #if framelen==1:
                        #    intrans.add(lexid)
                        #else:
                            lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJpl':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJunacc':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_2_rel := ' + lexid+'_v & arg1- & 2np & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ':
                        if framelen==1:
                            trans.add(lexid)
                        else:
                          lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & arg4- & prt-.']
#                          lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_a_rel := ' + lexid+'_v & adj+ & 1np & 2np & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJfin-OBJ':
                        if framelen==1:
                            trans.add(lexid)
                        else:
                            lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & arg4- & prt-.']
#                            lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_a_rel := ' + lexid+'_v & adj+ & 1np & 2np & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJcogn':
                        if framelen==1:
                            trans.add(lexid)
                        else:
                            lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & arg4- & prt-.']
#                            lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_a_rel := ' + lexid+'_v & adj+ & 1np & 2np & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_123_rel := ' + lexid+'_v & 1np & 2np & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-ACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ap_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-ACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ap_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-ACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ap_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-NCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-OBJNCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-OBJNCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-NCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJexpl-ACOMPorNCOMP-XCOMPorCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip-ap_124_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & 4ap & prp- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_124_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & 4np & prp- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp-ap_124_rel := ' + lexid+'_v & arg1- & 2cp & arg3- & 4ap & prp- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_124_rel := ' + lexid+'_v & arg1- & 2cp & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJexpl-NCOMP-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_24_rel := ' + lexid+'_v & arg1- & 2cp & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJexpl-NCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJexpl-AorNCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ap_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4ap & prp- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-OBJACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_124-ap_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-OBJACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ap_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-OBJ-OBJACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_134_rel := ' + lexid+'_v & 1np & refl & arg2+ & 3np & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-ACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ap_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4ap & prp- & prt-.']
                    elif framename == 'V-SUBJ-XCOMPellbare':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3- & arg4- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-infbare_12_rel := ' + lexid+'_v & 1np & 2vp & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-XCOMPbare':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-infbare_12_rel := ' + lexid+'_v & 1np & 2vp & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-ACCINF':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-infbare_123_rel := ' + lexid+'_v & 1np & 2vp & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-XCOMPbareobjcont':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip3_123_rel := ' + lexid+'_v & 1np & 2ip3 & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_123_rel := ' + lexid+'_v & 1np & 2cp & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-COMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-wh_123_rel := ' + lexid+'_v & 1np & 2wh & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-COMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-wh_12_rel := ' + lexid+'_v & 1np & 2wh & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-COMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-wh_2_rel := ' + lexid+'_v & arg1- & 2wh & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_2_rel := ' + lexid+'_v & arg1- & 2cp & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-COMPat':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-COMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-wh_12_rel := ' + lexid+'_v & 1np & 2wh & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-COMPintarg3':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-wh_12_rel := ' + lexid+'_v & 1np & 2wh & arg3- & arg4- & prt-.']
                    elif framename == 'Vinq-SUBJ-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-inq_12_rel := ' + lexid+'_v & 1np & 2inq & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-XCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_2_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJinf-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_2_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-COMPinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_2_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-INFCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_2_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & arg4- & prt-.']
#                    elif framename == 'V-SUBJexpl-OBJ-INFCOMP':
#                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_24_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & 4np & prp- & prt-.']
                    elif framename == 'V-SUBJ-INFCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_12_rel := ' + lexid+'_v & 1np & 2ip & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-XCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-XCOMParg3':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3- & arg4- & prt-.']
                    elif framename == 'V-RAISINGinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3- & arg4- & prt-.']
                    elif framename == 'V-OBJrefl-RAISINGinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-XCOMPobjcont':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip3_123_rel := ' + lexid+'_v & 1np & 2ip3 & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-XCOMPsubjcont':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip1_123_rel := ' + lexid+'_v & 1np & 2ip1 & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJrefl-XCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-ip1_2_rel := ' + lexid+'_v & arg1- & 2ip1 & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-XCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_2_rel := ' + lexid+'_v & arg1- & 2np & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJrefl':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl_0_rel := ' + lexid+'_v & arg1- & refl & arg2+ & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJrefl-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-cp_2_rel := ' + lexid+'_v & arg1- & 2cp & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJ-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_23_rel := ' + lexid+'_v & arg1- & 2cp & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJ-COMPorSUBJfin':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_23_rel := ' + lexid+'_v & arg1- & 2cp & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJ-XCOMPorCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip3_23_rel := ' + lexid+'_v & arg1- & 2ip3 & 3np & arg4- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-cp_23_rel := ' + lexid+'_v & arg1- & 2cp & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJ-XCOMPorSUBJinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip3_23_rel := ' + lexid+'_v & arg1- & 2ip3 & 3np & arg4- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_23_rel := ' + lexid+'_v & arg1- & 2ip & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJexpl-OBJ-INFCOMPorSUBJinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip3_23_rel := ' + lexid+'_v & arg1- & 2ip3 & 3np & arg4- & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-ip_23_rel := ' + lexid+'_v & arg1- & 2ip & 3np & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJ-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-INDOBJ-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-POBJNCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-OBLBEN':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*til_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & til_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-OBJNCOMPsom':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*som_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & som_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-NCOMPsom':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl*som_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4np & som_prp & prt-.']
                    elif framename == 'V-SUBJ-NCOMPsom':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-*som_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4np & som_prp & prt-.']
                    elif framename == 'V-SUBJ-PRT-NCOMPsom':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*som_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4np & som_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ap_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ap & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-PACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ap_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ap & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-POBJACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ap_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ap & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJexpl-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PCOMParg3':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PCOMPat':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PCOMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-wh_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4wh & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJexpl-PCOMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-wh_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4wh & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-PCOMPinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ip & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJexpl-PCOMPinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4ip & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-PCOMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-wh_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4wh & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-PCOMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl*'+preds[1]+'-wh_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4wh & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl*'+preds[1]+'-cp_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip1_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ip1 & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-P-RAISING':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip1_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ip1 & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PXCOMPprosbj':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip1_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ip & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-PRT-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-ip1_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ip1 & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-PRT-P-RAISING':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-ip1_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ip1 & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJrefl-PRT-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-'+preds[1]+'*'+preds[2]+'-ip1_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4ip1 & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-OBJ-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-ip1_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ip1 & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJ-PXCOMPobjcont':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip2_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ip2 & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip2_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ip2 & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJ-PXCOMPsubjcont':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip1_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4ip1 & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl*'+preds[1]+'_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-PCOMPat':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-*'+preds[1]+'-cp_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl*'+preds[1]+'-ip1_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4ip1 & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-POBJrefl':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-refl_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & arg4+ & refl & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-POBJrefl-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-refl_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & arg4+ & refl & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-POBJrefl-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-refl-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3- & arg4+ & refl & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJexpl-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-POBJarg3':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-PRT':
                        lexicon[lexid] = lexicon.get(lexid , []) + [ lexid+'-refl-'+preds[1]+'_1_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'_0_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-cp_2_rel := ' + lexid+'_v & arg1- & 2cp & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT-OBJ-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-cp_23_rel := ' + lexid+'_v & arg1- & 2cp & 3np & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJinf-PRT':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-ip_2_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT-COMPinf':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-ip_2_rel := ' + lexid+'_v & arg1- & 2ip & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-OBJ-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'_123_rel := ' + lexid+'_v & 1np & 2np & 3np & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-ACOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-ap_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4ap & prp- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJrefl-PRT-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-'+preds[1]+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3+ & refl & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJrefl-PRT-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-'+preds[1]+'-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3+ & refl & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-OBJnonarg-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-COMPat':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-COMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-wh_12_rel := ' + lexid+'_v & 1np & 2wh & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-XCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3- & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJrefl-PRT-XCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'-refl-ip1_12_rel := ' + lexid+'_v & 1np & 2ip1 & arg3+ & refl & arg4- & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4np & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT-POBJ-COMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-wh_24_rel := ' + lexid+'_v & arg1- & 2wh & arg3- & 4np & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4np & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-PCOMPat':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-cp_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4cp & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-cp_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4cp & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJexpl-PRT-PCOMPat':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-cp_4_rel := ' + lexid+'_v & arg1- & arg2- & arg3- & 4cp & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-PCOMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'-wh_14_rel := ' + lexid+'_v & 1np & arg2- & arg3- & 4wh & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-PRT-OBJ-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-'+preds[1]+'*'+preds[2]+'_124_rel := ' + lexid+'_v & 1np & 2np & arg3- & 4np & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJrefl-PRT-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-'+preds[1]+'*'+preds[2]+'_14_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & 4np & '+preds[2]+'_prp & '+preds[1]+'_prt.']
                    elif framename == 'V-SUBJ-OBJrefl':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl_1_rel := ' + lexid+'_v & 1np & refl & arg2+ & arg3- & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl_12_rel := ' + lexid+'_v & 1np & 2np & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'V-SUBJ-OBJrefl-COMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'-refl-cp_12_rel := ' + lexid+'_v & 1np & 2cp & arg3+ & refl & arg4- & prt-.']
                    elif framename == 'VPIDIOM-INDEFOBJ' or framename == 'VPIDIOM-INDEFPREDLINK':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'_1_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2indsg & arg3- & arg4- & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    elif framename == 'VPIDIOM-INDEFOBJ-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'_14_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2indsg & arg3- & 4np & '+preds[2]+'_prp & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    elif framename == 'VPIDIOM-DEFOBJ-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'_14_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2defpl & arg3- & 4np & '+preds[2]+'_prp & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    elif framename == 'VPIDIOM-INDEFOBJ-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'-cp_14_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2indsg & arg3- & 4cp & '+preds[2]+'_prp & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    elif framename == 'VPIDIOM-INDEFOBJ-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'-ip1_14_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2indsg & arg3- & 4ip1 & '+preds[2]+'_prp & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    elif framename == 'VPIDIOM-DEFOBJ-PXCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'-ip1_14_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2defsg & arg3- & 4ip1 & '+preds[2]+'_prp & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    elif framename == 'VPIDIOM-INDEFOBJ-PCOMPint':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'-wh_14_rel := ' + lexid+'_v & 1np & '+preds[1]+'_n & 2indsg & arg3- & 4wh & '+preds[2]+'_prp & prt-.']
                        idiomnouns.add(preds[1])
                        nouns.add(preds[1])
                    # elif framename == 'VPIDIOM-PSELOBJ':
                    #     lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & '+preds[1]+'_prp & 4defpl & '+preds[2]+'_n & prt-.']
                    #     print '_'+lexid+'*'+preds[1]+'*'+preds[2]+'_1_rel := ' + lexid+'_v & 1np & arg2- & arg3- & '+preds[1]+'_prp & 4defpl & '+preds[2]+'_n & prt-.'
                    #     idiomnouns.add(preds[2])
                    #     nouns.add(preds[2])
                    elif framename == 'VPIDIOM-OBJ-PSELOBJindef':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & '+preds[1]+'_prp & 4indsg & '+preds[2]+'_n & prt-.']
                        idiomnouns.add(preds[2])
                        nouns.add(preds[2])
                    elif framename == 'VPIDIOM-OBJ-PSELOBJdef':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'*'+preds[2]+'_12_rel := ' + lexid+'_v & 1np & 2np & arg3- & '+preds[1]+'_prp & 4defsg & '+preds[2]+'_n & prt-.']
                        idiomnouns.add(preds[2])
                        nouns.add(preds[2])
                    # ADJECTIVES
                    elif framename == 'ADJECTIVE-PCOMPL':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & 4cp & '+preds[1]+'_prp & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip1_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & 4ip1 & '+preds[1]+'_prp & prt-.']
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-np_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & 4np & '+preds[1]+'_prp & prt-.']
                        adjs.add(lexid)
                    elif framename == 'ADJECTIVE-OBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_np_rel := ' + lexid+'_prd & arg1- & 2np & arg3- & arg4- & prt-.']
                        adjs.add(lexid)
                    # NOUNS
# PH 2019-05-27: Commented out these in order to reduce the number of 
# types.
                    elif framename == 'MASSNOUN':
                       massnouns.add(lexid)
                    elif framename == 'COUNTNOUN':
                       countnouns.add(lexid)
                    elif framename == 'N-PCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-cp_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & '+preds[1]+'_prp & 4cp & prt- & atom.']
                        nouns.add(lexid)
                    elif framename == 'N-PINFCOMP':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-ip1_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & 4ip1 & '+preds[1]+'_prp & prt- & atom.']
                        nouns.add(lexid)
                    elif framename == 'N-POBJ':
                        lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'*'+preds[1]+'-np_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & '+preds[1]+'_prp & 4np & prt- & atom.']
                        nouns.add(lexid)
                    else:
                        frameset.add(framename) # 
            elif cat == 'Nmeas':
                allprds.add(lexid)
                lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_meas_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & arg4- & prt- & meas+.'] # 
                nouns.add(lexid)
            if cat == 'N':
                if '@TEMPLOCNOUN' in frames:
                    lexicon[lexid] = lexicon.get(lexid , []) + ['_'+lexid+'_n_rel := ' + lexid+'_prd & arg1- & arg2- & arg3- & arg4- & prt- & atom & time-loc_prd.']
                    templocnouns.add(lexid)
                    nouns.add(lexid)
        uniqentries.add(lexid+category)
#        except:
#            pass


def sortfunc(x,y):
	return cmp(x[1],y[1])
items=framecount.items()
items.sort(sortfunc)
# for item in items:
#     if item[0] in frameset:# and 'VPIDIOM' in item[0]:
#         print item

items=catcount.items()
items.sort(sortfunc)
# for item in items:
#     if not item[0] in catset:
#         print item


idiomset=set([])
idiomlex=set([])
for idiom in idiomnouns:
    idiomset.add(idiom + '_prd := link.')
    idiomset.add(idiom + '_n := '+idiom+'_prd & idiomform.')
    if not idiom in templocnouns:
        idiomset.add('_' +idiom + '_n_rel := '+idiom+'_prd & arg1- & arg2- & arg3- & arg4- & prt- & atom.')
    idiomitems = idiom.split('*')
    orth = ''
    for item in idiomitems:
        orth = orth + item + '", "'
    orth = orth[:-4]
#    idiomlex.add(idiom+'_idiom := empty-noun-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+idiom+'_n ].\n\n')

allverbs = set([])
for lexid in lexicon.keys():
    relations = lexicon[lexid]
    for relation in relations:
        items = relation[:-1].split()
        for item in items:
            if len(item)>2:
                if item[-2:]=='_v':
                    allverbs.add(item[:-2])
            if len(item)>4:
                if item[-4:]=='_prp':
                    prps.add(item[:-4])
                    funcwords.add(item[:-4])
                if item[-4:]=='_prt':
                    prts.add(item[:-4])
                    funcwords.add(item[:-4])

funcset=set([])
singleadvs = set([])
for adv in advs:
    adv = adv.replace('PERIOD','')
#    if adv in prps or adv in sadvs or adv in cadvs or adv in degadvs or adv in prts or adv in pvbobjs or adv in postps:
    funcset.add(adv + '_prp := ' +adv+ '_prd & prp+.')
    funcset.add('_' + adv + '_adv_rel := ' +adv+ '_prd & adv-link.')
#    else:
#        singleadvs.add(adv)
for prp in prps:
    prp = prp.replace('PERIOD','')
    funcset.add(prp + '_prp := ' +prp+ '_prd & prp+.')
    funcset.add('_'+ prp + '_p_rel := ' +prp+ '_prp & arg1+ & 2np & arg3- & arg4- & prt-.')
for postp in postps:
    funcset.add('_'+ postp + '_postp_rel := ' +postp+ '_prd & arg1- & arg2- & arg3- & arg4- & prt- & postp+.')
for prp in pvbobjs:
    funcset.add(prp + '_prp := ' +prp+ '_prd & prp+.')
    funcset.add('_'+ prp + '-cp_p_rel := ' +prp+ '_prp & arg1+ & 2cp & arg3- & arg4- & prt-.')
    funcset.add('_'+ prp + '-ip_p_rel := ' +prp+ '_prp & arg1+ & 2ip & arg3- & arg4- & prt-.')
for degloc in deglocs:
    degloc = degloc.replace('PERIOD','')
    funcset.add('_'+ degloc + '_deg-adv_rel := ' + degloc + '_prd & deg-adv.') 

for degadv in degadvs:
    degadv = degadv.replace('PERIOD','')
    if degadv in degrees.keys():
        if 'pos' in degrees[degadv]:
            funcset.add('_'+ degadv + '_deg-pos_rel := ' + degadv + '_prd & deg-pos.') 
        if 'cmp' in degrees[degadv]:
            funcset.add('_'+ degadv + '_deg-cmp_rel := ' + degadv + '_prd & deg-cmp.') 
        if 'sup' in degrees[degadv]:
            funcset.add('_'+ degadv + '_deg-sup_rel := ' + degadv + '_prd & deg-sup.')
    else:
        funcset.add('_'+ degadv + '_deg-pos_rel := ' + degadv + '_prd & deg-pos.') 
        funcset.add('_'+ degadv + '_deg-cmp_rel := ' + degadv + '_prd & deg-cmp.') 
        funcset.add('_'+ degadv + '_deg-sup_rel := ' + degadv + '_prd & deg-sup.') 

for degnum in degnums:
    degnum = degnum.replace('PERIOD','')
    funcset.add('_'+ degnum + '_deg-num_rel := ' + degnum + '_prd & deg-num.') 
for degqnt in degqnts:
    degqnt = degqnt.replace('PERIOD','')
    funcset.add('_'+ degqnt + '_deg-qnt_rel := ' + degqnt + '_prd & deg-qnt.') 

for ttl in ttls:
    ttl = ttl.replace('PERIOD','')
    funcset.add('_'+ ttl + '_ttl_rel := ' + ttl + '_prd & deg-nom.') 

for ttl in ttlnums:
    ttl = ttl.replace('PERIOD','')
    funcset.add('_'+ ttl + '_ttlnum_rel := ' + ttl + '_prd & deg-num.') 

    
funclex=set([])
trigger = set([])
triggerTiny = set([])
triggerSmall = set([])
triggerNouns = {}
alltrigger = set([])
for func in funcwords:
    func = func.replace('PERIOD','')
    funcset.add(func + '_prd := link.')
    funcitems = func.split('*')
    orth = ''
    for item in funcitems:
        orth = orth + item + '", "'
    orth = orth[:-4]
    if func in prps:
        trigger.add(func+'-prep_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+func+'_prp ] !>,\n    FLAGS.TRIGGER "'+func+'_prp" ].\n\n')
    if func in prts:
        trigger.add(func+'-part_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+func+'_prt ] !>,\n    FLAGS.TRIGGER "'+func+'_prt" ].\n\n')
#    alltrigger.add(func+'-func_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+func+'_prd ] !>,\n    FLAGS.TRIGGER "'+func+'_func" ].\n\n')
    if dark == False:
        #if func in qwords or func in prps or func in cadvs or func in prts or (func in advs and not func in singleadvs) or func in sadvs or func in pvbobjs or func in postps or func in degadvs or func in ttlnums or func in ttls:
        if func in cadvs:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_cadv := cadv-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+func+'_x_rel ].\n\n')
            trigger.add(func+'-cadv_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_x_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_cadv" ].\n\n')
        if func in ttls:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_ttl := title-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+func+'_ttl_rel ].\n\n')
            trigger.add(func+'-ttl_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_ttl_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_ttl" ].\n\n')
        if func in ttlnums:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_ttl := number-mod-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+func+'_ttlnum_rel ].\n\n')
            trigger.add(func+'-ttlnum_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_ttlnum_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_ttlnum" ].\n\n')
        if func in degadvs:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_degadv := degadv-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+func+'_prd ].\n\n')
            trigger.add(func+'-degnum_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+func+'_prd ] !>,\n    FLAGS.TRIGGER "'+func+'_degnum" ].\n\n')
        if func in sadvs:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_sadv := sadv-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+func+'_sadv_rel ].\n\n')
            trigger.add(func+'-sadv_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_sadv_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_sadv" ].\n\n')
        if func in postps:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_postp := postp-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+func+'_postp_rel ].\n\n')
            trigger.add(func+'-postp_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_postp_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_postp" ].\n\n')
        if func in prts:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_prt := part-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+func+'_prt ].\n\n')
            trigger.add(func+'-part_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+func+'_prt ] !>,\n    FLAGS.TRIGGER "'+func+'_prt" ].\n\n')
        if func in prps or func in pvbobjs:
            orth = orth.replace('PERIOD','.')
            funclex.add(func+'_prp := prep-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+func+'_prp ].\n\n')
            trigger.add(func+'-prep_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+func+'_prp ] !>,\n    FLAGS.TRIGGER "'+func+'_prp" ].\n\n')
        if func in singleadvs:
            funclex.add(func+'_adv := adv-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+func+'_adv_rel ].\n\n')
            trigger.add(func+'-adv_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_adv_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_adv" ].\n\n')
            alltrigger.add(func+'-adv_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED _'+func+'_adv_rel ] !>,\n    FLAGS.TRIGGER "'+func+'_adv" ].\n\n')

for q in qs.keys():
    qitems = q.split('*')
    orth = ''
    for item in qitems:
        orth = orth + item + '", "'
    orth = orth[:-4]
    features = qs[q]
    gend = 'gender'
    num = 'pn'
    if 'fem' in features:
        gend = 'fem'
    if 'comm' in features:
        gend = 'comm'
    if 'masc' in features:
        gend = 'masc'
    if 'sg' in features:
        num = 'sg'
    if 'pl' in features:
        num = 'pl'
    if 'sg' in features and 'pl' in features:
        num = 'pn'
    if q not in set(['fleste', 'færreste']):
        funclex.add(q+'_q := quant-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.Q.QREL [ ARG0.PNG [ GEN '+gend+',\n                                     PN '+num+' ],\n                          PRED _'+q+'_q_rel ] ].\n\n')
        funcset.add('_'+q+'_q_rel := quant_m_rel.')

pnheads = set([])
proper = set([])
for line in sub:
    if 'INTERJ_BASE' in line:
        items = line.split()
        if len(items) == 6:
            if not 'INTERJ' in items[5]:
                ijs.add(items[5])
    if 'PROP_BASE' in line:
        items = line.split()
        if len(items) == 6:
            if not 'PROP_BASE' in items[5] and not '.' in items[5]:
                proper = items[5]
                if proper not in set(['TIL']) and proper.lower() + '_pn' not in pnheads:
                    funclex.add(proper+'_pn := pn-word &\n  [ STEM < "'+proper+'" >,\n    SYNSEM.LKEYS.KEYREL.CARG "'+proper+'" ].\n\n')
                    alltrigger.add(proper+'_pn_rule := pn_rule &\n  [ CONTEXT.RELS <! [ CARG "'+proper+'" ] !>,\n    FLAGS.TRIGGER "'+proper+'_pn" ].\n\n')
                    pnheads.add(proper.lower()+'_pn')
                
for ij in ijs:
    ijitems = ij.split('*')
    orth = ''
    for item in ijitems:
        orth = orth + item + '", "'
    orth = orth[:-4]
    ij=ij.replace('*,*','*komma*')
    funclex.add(ij+'_ij := interj-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+ij+'_prd ].\n\n')
    funcset.add('_'+ ij + '_ij_rel := ' +ij+ '_prd & init_rel.')
    funcset.add(ij+ '_prd := link.')
    

for cadv in cadvs:
    funcset.add('_'+ cadv + '_x_rel := ' +cadv+ '_prd & cadv+.')

for sadv in sadvs:
    sadv = sadv.replace('PERIOD','')
    funcset.add('_' + sadv + '_sadv_rel := ' +sadv+ '_prd & sadv+ & arg1- & arg2- & arg3- & arg4- & prt-.')
for prt in prts:
    funcset.add(prt + '_prt := ' +prt+ '_prd & prt+.')
#for q in qs:
#    funcset.add('_'+ q + '_q_rel := ' +q+ '_prd & q+.')


lexkeys = set(lexicon.keys())
verb2inflcode = {}
def verbs2rels(infile):
    verbset = set([])
    for line in infile:
        items = line.split()
        if len(items)>1:
            if len(items[0])>2:
                if items[0][-2:] == '_v' or  '-n-' in items[0] or items[0][-2:] == '-a':
                    if items[0][-2:] == '_v':
                        pred = items[0].split('_')[0]
                    else:
                        pred = items[0].split('-')[0]
                    
                    verbset.add(pred)
                    if not pred in lexkeys and not pred in skipwords and pred in allverbs:
                        lexicon[pred] = ['_'+pred+'_1_rel := ' + pred+'_v & 1np & arg2- & arg3- & arg4- & prt-.','_'+pred+'_12_rel := ' + pred+'_v & 1np & 2np & arg3- & arg4- & prt-.','_'+pred+'_adj_rel := ' + pred+'_v & adj+ & 1np & 2np & arg3- & arg4- & prt-.']
                    if 'INFLECTION' in line:
                        if 'v1' in line:
                            inflcode = 'v1'
                        if 'v2' in line:
                            inflcode = 'v2'
                        if 'v3' in line:
                            inflcode = 'v3'
                        if 'v4' in line:
                            inflcode = 'v4'
                        verb2inflcode[pred] = inflcode
    return verbset
tinylex = verbs2rels(tinylexIN)
smalllex = verbs2rels(lexiconIN)

funclist = []
for func in funcset:
    funclist.append(func)

for idiom in idiomset:
    funclist.append(idiom)

predset = set([])
funclist.sort()
for func in funclist:
    func = func.replace('%','prosent')
    if '_rel := ' in func and dark == True:
        funcrel = func.split()[0]
        funcwords = funcrel.split('_')[1]
        funcitems = funcwords.split('*')
        orth = ''
        for item in funcitems:
            orth = orth + item + '", "'
        orth = orth[:-4]
        verbsDarkOUT.write(funcrel+'_func := func-word &\n  [ STEM < "'+orth+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+funcrel+' ].\n\n')
    reltypesSmallOUT.write(func+'\n')
    predset.add(func+'\n')
    #reltypesOUT.write(func+'\n')
    #print func
baseHeads = set([])
mweAdj = set([])
for line in triggerBaseIN:
    if ' := ' in line:
        baseHeads.add(line.split()[0][:-5])
    triggerOUT.write(line)
    triggerSmallOUT.write(line)
    

verbs = lexicon.keys()
lexIN=open('../lexicon.tdl')
smallverbpreds = set([])
pred2head = {}
for line in lexIN:
    if not ';' in line:
        if ' := ' in line:
            head = line.split()[0]
            if 'mwe-adj-lxm' in line:
                mweAdj.add(head)
            if '-' in head:
                headitems = head.split('-')
                if len(headitems) > 1:
                    pred = headitems[0]
                    pred2head[pred]=head
            elif '_' in head:
                headitems = head.split('_')
                if len(headitems) > 1:
                    pred = headitems[0]
                    pred2head[pred]=head
            if '-np' in head and not head in baseHeads and not 'det-meste' in head:
                triggerSmall.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! pronoun-relation !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
                alltrigger.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! pronoun-relation !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
        if 'PRED ' in line and not head in baseHeads and not head in mweAdj:
            mweAdj.add(head)
            items = line.split('PRED ')
            pred = items[1].split()[0]
            if pred[-1] == ',':
                pred = pred[:-1]
            triggerSmall.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ PRED '+pred+' ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
            alltrigger.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ PRED '+pred+' ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
        if 'CARG ' in line and not head in baseHeads and '"' in line:
            items = line.split('CARG ')
            pred = items[1].split('"')[1]
            if '-card' in head:     
                alltrigger.add(head+'_rule := card_rule &\n  [ CONTEXT.RELS <! [ CARG "'+pred+'" ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
                triggerSmall.add(head+'_rule := card_rule &\n  [ CONTEXT.RELS <! [ CARG "'+pred+'" ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n') # 
            elif '_pn' in head:# and head.lower() not in pnheads:     
                alltrigger.add(head+'_rule := pn_rule &\n  [ CONTEXT.RELS <! [ CARG "'+pred+'" ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
                pnheads.add(head.lower())
                triggerSmall.add(head+'_rule := pn_rule &\n  [ CONTEXT.RELS <! [ CARG "'+pred+'" ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
            elif head.lower() not in pnheads:
                triggerSmall.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ CARG "'+pred+'" ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
                alltrigger.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ CARG "'+pred+'" ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')

nklIN=open('../../resources/nkl/nkl.tdl')

for line in nklIN:
    if ' := ' in line:
        head = line.split()[0]
        headitems = head.split('-')
        if len(headitems) > 1:
            pred = headitems[0]
            pred2head[pred]=head
    # Restricting trigger rules to short lexemes
#    if 'PRED ' in line and not head in baseHeads and not len(head) > 17:
    if 'PRED ' in line and not head in baseHeads and not 'func' in head:
        items = line.split('PRED ')
        pred = items[1].split()[0]
        alltrigger.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ PRED '+pred+' ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')
    if 'CARG ' in line and not head in baseHeads:
        items = line.split('CARG ')
        pred = items[1].split()[0]
        alltrigger.add(head+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ CARG '+pred+' ] !>,\n    FLAGS.TRIGGER "'+head+'" ].\n\n')

reltypessmall = set([])

verbs.sort()
for item in verbs:
    item = item.replace('%','prosent')
    if item in nouns:
        #reltypesOUT.write(item+'_prd := link.\n')
        predset.add(item+'_prd := link.\n')
        try:
            if '_v' in pred2head[item]:
                alltrigger.add(pred2head[item]+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ PRED '+item+'_v ] !>,\n    FLAGS.TRIGGER "'+pred2head[item]+'" ].\n\n')
            else:
                alltrigger.add(pred2head[item]+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ PRED '+item+'_prd ] !>,\n    FLAGS.TRIGGER "'+pred2head[item]+'" ].\n\n')
        except:
            pass
    elif item in adjs:
        #reltypesOUT.write(item+'_prd := link.\n')
        predset.add(item+'_prd := link.\n')
        alltrigger.add(item+'-a_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+item+'_prd ] !>,\n    FLAGS.TRIGGER "'+item+'_a" ].\n\n')
    if item in allverbs:
        #reltypesOUT.write(item+'_prd := link.\n')
        #reltypesOUT.write(item+'_v := '+ item + '_prd & vrb+.\n')
        predset.add(item+'_v := vrb+.\n')
        alltrigger.add(item+'-v_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+item+'_v ] !>,\n    FLAGS.TRIGGER "'+item+'_v" ].\n\n')
    if item in tinylex and item in allverbs:
        triggerTiny.add(item+'-v_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+item+'_v ] !>,\n    FLAGS.TRIGGER "'+item+'_v" ].\n\n')
    # if item in smalllex and item in intrans:
    #     predsSmallOUT.write('_'+ item+'_1_rel := link.\n')
    # if item in smalllex and item in trans:
    #     predsSmallOUT.write('_'+ item+'_12_rel := link.\n')
    if item in smalllex:# and not item in trans and not item in intrans:
        if item in nouns and not item == 'sum' and not item == 'skål' and not item == 'minimum' and not item == 'mot' and not item in templocnouns and not pred2head[item][-2:]=='_v' and not pred2head[item][-2:]=='_p':
            reltypessmall.add(item+'_prd := link.\n')
            reltypessmall.add('_'+item+'_n_rel := '+item+'_prd & arg1- & arg2- & arg3- & arg4- & prt- & atom.\n')
            triggerSmall.add(pred2head[item]+'_rule := generator_rule &\n  [ CONTEXT.RELS <! [ PRED '+item+'_prd ] !>,\n    FLAGS.TRIGGER "'+pred2head[item]+'" ].\n\n')
        elif item in adjs:
            reltypessmall.add(item+'_prd := link.\n')
            reltypessmall.add('_'+item+'_a_rel := '+item+'_prd & prp- & arg1+ & arg2- & arg3- & arg4- & prt- & adj+ & atom.\n')
            triggerSmall.add(item+'-a_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+item+'_prd ] !>,\n    FLAGS.TRIGGER "'+item+'_a" ].\n\n')
        elif item in smallverbpreds:
            reltypessmall.add(item+'_v := link.\n')
            triggerSmall.add(item+'-v_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+item+'_v ] !>,\n    FLAGS.TRIGGER "'+item+'_v" ].\n\n')

    if item in nouns and not item in templocnouns:

        verbrels.add('_'+item+'_n_rel := '+item+'_prd & arg1- & arg2- & arg3- & arg4- & prt- & atom.\n')
    if item in adjs:
        verbrels.add('_'+item+'_a_rel := '+item+'_prd & prp- & arg1+ & arg2- & arg3- & arg4- & prt- & adj+ & atom.\n')
    for rel in lexicon[item]:
        verbrels.add(rel + '\n')
        if item in tinylex:
            if '_rel := ' in rel and dark == True:
                funcrel = rel.split()[0]
                funcwords = funcrel.split('_')[1]
                funcitems = funcwords.split('*')
                orth = ''
                for funcitem in funcitems:
                    orth = orth + funcitem + '", "'
                orth = orth[:-4]
                verbsDarkOUT.write(funcrel+'_v := main-verb-lxm &\n  [ STEM < "'+item+'" >,\n    INFLECTION '+verb2inflcode[item]+',\n    SYNSEM.LKEYS.KEYREL.PRED '+funcrel+' ].\n\n')
        if item in smalllex:
            reltypessmall.add(item+'_prd := link.\n')
            reltypessmall.add(rel + '\n')

def sortfunc(x,y):
	return cmp(len(x[1]),len(y[1]))
items=lexicon.items()
items.sort(sortfunc)

# for item in items:
#     print item[0],
#     print item[1],
#     print len(item[1])


triglist = []
for trig in trigger:
    triglist.append(trig)
triglist.sort()

#    triggerTinyOUT.write(line)
for trig in triglist:
    functriggerOUT.write(trig)

#for trig in triggerTiny:
#    triggerTinyOUT.write(trig)

lexiconIN=open('../lexicon.tdl')
lexheads = set([])
for line in lexiconIN:
    if ':=' in line and not ';' in line:
        lexhead = line.split()[0]
        lexheads.add(lexhead)


for trigger in triggerSmall:
    if trigger.split()[0][:-5] in lexheads:
        triggerSmallOUT.write(trigger)

funcpreds = set([])
def mwelex(IN,OUT):
    for line in IN:
        if '-a := adj-lxm' in line:
            items = line.split('-a')
            adj = items[0]
            if adj in adjs:
                line = line.replace('adj-lxm','mwe-adj-lxm')
        if '_a_rel"' in line:
            items = line.split('_')
            adj = items[1]
            if adj in adjs:
                line = line.replace('"_'+adj+'_a_rel"',adj+'_prd')
        
        if '-noun-lxm' in line:
            items = line.split('-n')
            noun = items[0]
            line = line.replace('mass-noun-lxm','noun-lxm')
            if noun in nouns:
                line = line.replace('noun-lxm','mwe-noun-lxm')
            else:
                line = line.replace('noun-lxm','cmp-noun-lxm')
            if not noun in massnouns and noun in countnouns:
                line = line.replace('noun-lxm','count-noun-lxm')
        if '_n_rel"' in line:
            items = line.split('_')
            noun = items[1]
            if noun in nouns:
                line = line.replace('"_'+noun+'_n_rel"',noun+'_prd')
            generationOUT.write('_'+ noun+'_n_rel := link.\n')

        if 'main-verb-lxm' in line:
            items = line.split('_v :=')
            verb = items[0]
            # if verb in intrans:
            #     line=line.replace('main-verb-lxm','intrans-verb-lxm')
            #     generationOUT.write('_'+ verb+'_1_rel := link.\n')
            # if verb in trans:
            #     line=line.replace('main-verb-lxm','trans-verb-lxm')
            #     generationOUT.write('_'+ verb+'_12_rel := link.\n')
        if '_v ].' in line:
            items = line.split('PRED ')
            items2=items[1].split()
            verb = items2[0][:-2]
            # if verb in intrans:
            #     line=line.replace(verb+'_v','"_'+verb+'_1_rel"')
            # if verb in trans:
            #     line=line.replace(verb+'_v','"_'+verb+'_12_rel"')
        if '_func :=' in line:
            items = line.split('_')
            funcpreds.add(items[0])
        OUT.write(line)
#    OUT.close()

nklIN=open('../../resources/nkl/nkl.tdl')
nklOUT=open('nkl.tdl','w')
mwelex(nklIN,nklOUT)


    
lexpreds = set([])
lexentries = set([])
lexentry = ''
inentry = False
lexIN=open('../lexicon.tdl')
for line in lexIN:
    if ':=' in line:
        inentry = True
    if inentry:
        lexentry = lexentry+line
    if '].' in line:
        inentry = False
        lexentries.add(lexentry+'\n')
        lexentry = ''
    if 'PRED' in line:
        items = line.split()
        for item in items:
            if '_' in item:
                if not '"' in item:
                    preditems = item.split('_')
                    if preditems[0] == '':
                        form = preditems[1]
                    else:
                        form = preditems[0]
                    lexpreds.add(form)
                    formitems=re.split('\*|-',form)
                    for formitem in formitems:
                        lexpreds.add(formitem)


lexlist = []
for lex in idiomlex:
    lexlist.append(lex)
lexlist.sort()
for lex in lexlist:
    if not lex in lexentries:
        items=lex.split('_')
        pred = items[0]
        if not pred in funcpreds and not pred in lexheads:
            nklOUT.write(lex)


for line in linktypesIN:
    items=line.split('_')
    items = items[0].split('-')
    items = items[0].split('*')
    prd = items[0]
    predset.add(line)

for line in nklfuncrelsIN:
    items=line.split('_')
    if items[0] == '':
        prd = items[1]
    else:
        prd = items[0]
    if not prd in funcwords:
        predset.add(line)
        #nklfuncrelsOUT.write(line)



predset = predset|verbrels

newset = set([])
exset = set([])
expreds = set(['_hvor_adv_rel','_hvordan_adv_rel','_hvorfor_adv_rel','_mye_q_rel','_smile_12_rel','_sove_1_rel'])
for line in predset:
    line = line.replace(' := link',' := predsort')
    line = line.replace('Gud_','gud_')
    for pred in expreds:
        newset.add(line)
        if pred in line:
            exset.add(line)
predset=newset

    
norlines = set([])
norheads = set([])
for line in norIN:
    if ':=' in line:
        norhead = line.split(' := ')[0]
        norheads.add(norhead)
    if line in predset:
        predset.remove(line)
        norlines.add(line)

for line in exset:
    if line in predset:
        predset.remove(line)
    
predslist = []
advset = set(['c_o'])
degadvset = set([])
prpset = set([])
allpredset = set(['c_o'])
for pred in predset:
    if '_adv_rel' in pred:
        advset.add(pred.split('_')[1])
    if '_deg-num_rel' in pred:
        degadvset.add(pred.split('_')[1])
    if '_p_rel' in pred:
        prpset.add(pred.split('_')[1])
    predslist.append(pred)
    if '_rel' in pred:
        allpredset.add(pred.split('_')[1])
predslist.sort()

headset = set([])
smallpreds = set([])
for pred in predslist:
  if not pred.split(' := ')[0] in norheads and not pred.split(' := ')[0] in headset:
    headset.add(pred.split(' := ')[0])  
    predset.add(pred)
    predsOUT.write(pred)
    typeitems = pred[:-2].split()
    preditems = typeitems[0].split('_')
    if preditems[0] == '':
        form = preditems[1]
    else:
        form = preditems[0]
    if form in lexpreds:
        smallpreds.add(pred)
    formitems=re.split('\*|-',form)
    if formitems[0] in lexpreds:
        smallpreds.add(pred)
        for typeitem in typeitems:
            if typeitem[-2:] == '_n':
                form = typeitem[:-2]
                smallpreds.add(form+'_n := '+form+'_prd & idiomform.\n')
                smallpreds.add(form+'_prd := predsort.\n')
                if not form in templocnouns:
                    smallpreds.add('_'+form+'_n_rel := '+form+'_prd & arg1- & arg2- & arg3- & arg4- & prt- & atom.\n')
            if typeitem[-4:] == '_prp':
                form = typeitem[:-4]
                smallpreds.add(form+'_prp := '+form+'_prd & prp+.\n')
                smallpreds.add(form+'_prd := link.\n')
                preptype = '_'+form+'_p_rel := '+form+'_prp & arg1+ & 2np & arg3- & arg4- & prt-.\n'
                if preptype in predset:
                    smallpreds.add(preptype)
            if typeitem[-4:] == '_prt':
                form = typeitem[:-4]
                smallpreds.add(form+'_prt := '+form+'_prd & prt+.\n')
                smallpreds.add(form+'_prd := predsort.\n')

for item in smallpreds:
    item = item.replace(' := link',' := predsort')
    reltypessmall.add(item)

reltypessmalllist = []
for item in reltypessmall:
    reltypessmalllist.append(item)

reltypessmalllist.sort()

smallpredslist = []
for pred in reltypessmalllist:
    if not pred in norlines and not pred.split(' := ')[0] in norheads:
        smallpredslist.append(pred)


predssmall = set([])
predheadsmall = set([])
for pred in smallpredslist:
    head = pred.split()[0]
    predheadsmall.add(head)
    pred = pred.replace(' := link',' := predsort')
    item = pred.split()[2]
    if '_v' in item and not item[:-2]+'_v' in norheads:
        predssmall.add(item[:-2]+'_v := vrb+.\n')
    predssmall.add(pred)

smallpredslist = []
for pred in predssmall:
    smallpredslist.append(pred)

smallpredslist.sort()

    
for pred in smallpredslist:
    if not 'aldri_adv' in pred:
        predsSmallOUT.write(pred)

lexlist = []
for lex in funclex:
    lexlist.append(lex)
lexlist.sort()

for lex in lexlist:
    head = lex.split()[0]
    #if head in norheads:
    #    print head
    if not lex in lexentries and (not head in headset or not head in norheads):
        items=lex.split('_')
        pred = items[0]
        if not pred+ '_q' in lexheads and not pred+ '_func' in lexheads and not pred in set(['Ica', 'Lo', 'Marianne', 'Nav', 'bar', 'deb', 'gud']):
            nklOUT.write(lex)

nklOUT.close()

nklIN=open('nkl.tdl')
nklOUT=open('../nkl.tdl','w')
lexentries = {}
heads = set([])
for line in nklIN:
    if ':=' in line:
        head = line.split()[0]
        heads.add(head)
        line1 = line
    if '[ STEM ' in line:
        line2 = line
    if 'INFLECTION' in line:
        line2 = line2+line
    if 'Q.QREL' in line:
        line2 = line2+line
    if '            PN ' in line:
        line2 = line2+line
    if '].' in line:
        line3 = line
        lexentries[head] = line1+line2+line3+'\n'

newheads = set([])
newpreds = set([])
newadvs = set([])
for head in heads:
    pred = head.split('_')[0]
    if pred+'_func' in heads and not head == pred+'_func':
        newheads.add(head)
        newpreds.add(pred)
    if pred+'_func' in heads and pred in advs:
        newadvs.add(pred)

print 'Sorting lexicon'
def sortfunc(x,y):
	return cmp(x[0],y[0])
items=lexentries.items()
items.sort(sortfunc)
for item in items:
    if item[0][-5:] == '_func' and (item[0][:-5] in newadvs or item[0][:-5] in advset):
        newentry = item[1].replace('_func','_adv')
        newentry = newentry.replace('func-word','adv-word')
        newentry = newentry.replace('PRED ','PRED _')
        newentry = newentry.replace('_prd','_adv_rel')
        nklOUT.write(newentry)
    elif item[0][-5:] == '_func' and (item[0][:-5] in newadvs or item[0][:-5] in degadvset):
        newentry = item[1].replace('_func','_degadv')
        newentry = newentry.replace('func-word','degadv-word')
        newentry = newentry.replace('PRED ','PRED _')
        newentry = newentry.replace('_prd','_deg-num_rel')
        nklOUT.write(newentry)
    elif item[0][-5:] == '_func' and (item[0][:-5] in newadvs or item[0][:-5] in prpset):
        newentry = item[1].replace('_func','_prp')
        newentry = newentry.replace('func-word','prep-word')
        newentry = newentry.replace('_prd','_prp')
        nklOUT.write(newentry)
    elif not(item[0][-5:] == '_func'):
        nklOUT.write(item[1])
nklOUT.close()

alltriglist = []
for alltrig in alltrigger:
    alltriglist.append(alltrig)
alltriglist.sort()

trigheads = set([])
for alltrig in alltriglist:
    trighead = alltrig.split()[0]
    if not trighead in trigheads:
        triggerOUT.write(alltrig)
    trigheads.add(trighead)
    
predsMidIN=open('../preds-mid.tdl','r')
predsMid=set([])
for line in predsMidIN:
    predsMid.add(line)
predsMidOUT=open('../preds-mid.tdl','w')
predsMidOUT.write(';;  -*- Mode: TDL; Coding: utf-8; -*- \n;;\n')
predsMidOUT.write(';;  Type file automatically derived from \n;;  Norsk Komputasjonelt Leksikon and  NorGram (')
predsMidOUT.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
predsMidOUT.write(';;  See \'license.txt\' for licence conditions\n;;\n\n')

predheadmid = set([])
for line in predsMidIN:
    head = line.split()[0]
    if head not in predheadsmall and head not in predheadmid:
        predsMidOUT.write(line)
        predheadmid.add(head)
