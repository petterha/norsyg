#!/usr/bin/python
#-*- encoding: utf-8 -*-

# python ~/consttree/incr2const.py /home/phau/tmp/tmp.AJa2RgYBgV 1

#
# Script for extracting trees out of AVMs. To be executed after 
# a sentence is parsed,
# and the resulting AVMs are written to '/tmp/output.dag':
#
# ./ace -g norwegian-small.dat -1 < input.txt > /tmp/result.txt
# cut -d ";" -f 2 /tmp/result.txt | grep '(' > /tmp/my-derivation.txt
# ./recons -g norwegian-small.dat -tff < /tmp/my-derivation.txt > /tmp/avm.txt

#
# The script is executed with the following command:
#
# python incr2const.py
#
# This produces a bracketed representation. In order to produce latex
# trees, add the opional argument 'tex':
#
# python incr2const.py tex
# 
# Petter Haugereid, petterha@gmail.com
# 

import sys,os

#resultFile= open('result.html','a')
#treeFile=open('analyses/' + sys.argv[1][5:-4]+'.tree.html','w')
#tabularFile=open('analyses/' + sys.argv[1][5:-4]+'.tab.html','w')
#treeDataFile=open('analyses/' + sys.argv[1][5:-4]+'.js','w')

try:
    exported = open(sys.argv[1])
    number = sys.argv[2]
#    exported = open('/tmp/avm.txt')
except:
    print 'AVM missing in \''+sys.argv[1]+'\'.' 
    quit()

try:
    texopt = sys.argv[1]
    if texopt == 'tex':
        tex = True
    else:
        tex = False
    if texopt == 'funcgram':
        funcgram = True
    else:
        funcgram = False
except:
    tex = False
    funcgram = True

# treeData = open('treeData.html','a')
# tabularData = open('tabularData.html','a')
#print exported
# Converting AVMs from ACE format into LKB format.
for line in exported:
    items = line.split()
    newavm = ''
    oldstring = ''
#    level = 0
    value = False
    for item in items:
        if item[:3] == '#D[' and item[-1:] == ']':
            item = item[3:-1]
        if not item == ']':
            if value == True:
#                newavm = newavm + ',\n' + 2*level*' '
                newavm = newavm + ',\n'
            value = False
        if item[:3] == '#D[':
#            newavm = newavm + item[3:] + ' & [\n'  + 2*level*' '
#            level = level+1
            newavm = newavm + item[3:] + ' & [\n'
        elif item[-1:] == ':':
            newavm = newavm + item[:-1] + ' '
        elif item[-2:] == '>=':
                newavm = newavm + '#' + item[1:-2] + ' & '
        else:
            value = True
            if item[-1] == '>':
                newstring = '#' + item[1:-1]
            elif item == ']':
                newstring = ' ]'
#                level = level-1
            else:
                newstring = item
            newavm = newavm + newstring
    if '[' in newavm:
        newavm = newavm+'.'
        exported = newavm

def path2string(inlist):
    pathstring = ''
    for feature in inlist:
        pathstring = pathstring + '$' + feature
    return pathstring

avms = []
newlines = []
#exported = exported.read().strip().split('\n')
exported = exported.split('\n')
for line in exported:
    newlines.append(line)
    if ']main' in line:
        avms.append(newlines)
        newline = 'main' + line.split(']main')[1]
        newlines = [newline]
avms.append(newlines)

prevline = newlines[0]
def checkstack(lasttag,stacklist):
    values = tag2value[lasttag]
    for value in values:
        if value[0] == 'FIRST':
            lasttag = value[1]
            values = tag2value[lasttag]
            for value in values:
                if value[0] == 'LOCAL':
                    lasttag = value[1]
                    values = tag2value[lasttag]
                    for value in values:
                        if value[0] == 'CAT':
                            lasttag = value[1]
                            values = tag2value[lasttag]
                            for value in values:
                                if value[0] == 'HEAD':
                                    lasttag = value[1]
                                    stacklist.append(lasttag)
                            for value in values:
                                if value[0] == 'STACK':
                                    lasttag = value[1]
                                    return [lasttag,stacklist]

def path2tag(path):
    tag = '$0'
    for feature in path:
        for value in tag2value[tag]:
            possfeat = value[0]
            if possfeat == feature:
                tag = value[1]
                mytype = tag2type[tag]
                lasttag = tag
                lastfeat = feature
    if lastfeat == path[-1]:
        return lasttag
    else:
        return ''

def path2type(path):
    return tag2type[path2tag(path)]

def gramfunc(arg,subjtype,tense,head,mtype,perf,keypred):
    if arg == '':
        arg = '0'
    else:
        arg = arg[:1]
    if (subjtype == '+' and (not head == 'V' and not head == 'Aux' and not head == 'AuxP' and not head == 'SAdv' and not head == 'SAdvP' and not head == 'P' and not head == 'PP' and not head == '')) or ('-su-' in mtype and not 'non-su' in mtype):
        gram = 'Subj'
    else:
        if arg == '2':
            if keypred == '_være_12_rel' or keypred == '_bli_12_rel' or keypred == '_hete_12_rel':
                gram = 'Pred'
            else:
                gram = 'DO'
        elif arg == '3':
            gram = 'IO'
        elif arg == '4':
            if head == 'AP' or head == 'Adj' or mtype == 'arg4-extr-ap-struc':
                gram = 'Pred'
            else:
                gram = 'PPobj'
        elif head == 'V' or head == 'Aux':
            if (tense == 'present' or tense == 'pret') and perf == '-':
                gram = 'Vfin'
            else:
                gram = 'Vinfin'
        elif head == 'RFL':
            gram = 'RFL'
        elif head == 'PRT':
            gram = 'PRT'
        elif head == 'SAdv':
            gram = 'SAdv'
        elif head == 'Conj':
            gram = 'Conj'
        elif mtype == 'prepsel-binary':
            gram = 'PPobj'
        elif mtype[:4] == 'deg-' or mtype == 'mwe-conj-phrase':
            gram = 'DegAdv'
        else:
            gram = 'Adv'
    return gram
    
type2word = {'aux': 'Aux', 'adv-prep': 'P', 'prep': 'P', 'prep-min': 'P', 'part': 'PRT', 'refl-pron-light': 'RFL', 'noun': 'N', 'nominal': 'N', 'noun-pn': 'N', 'mainverb': 'V', 'verb': 'V', 'aux-verb': 'V', 'subcompl-infcompl-verb': 'V','pron': 'PRON','expl-pron': 'Expl_Subj','cop-pron': 'PRON', 'proper-noun': 'PN', 'det': 'Det', 'card': 'Det', 'carddef': 'Det', 'det-quant': 'Det', 'quant': 'Det', 'poss': 'Det', 'adj': 'Adj', 'adj-adv': 'Adj', 'mod-mod': 'Adv', 'sadv': 'SAdv', 'cadv': 'C', 'complementizer': 'C', 'subcompl': 'C', 'subcompl-omcompl': 'C', 'adv': 'Adv', 'condcompl': 'C', 'subcompl': 'C', 'atfull': 'C', 'relcompl': 'R', 'infcompl': 'Inf', 'conj': 'Conj', 'start': 'S', 'continuative': 'Forb'} 
type2phrase = {'aux': 'AuxP', 'adv-prep': 'PP', 'prep': 'PP', 'prep-min': 'PP', 'noun': 'NP', 'nominal': 'NP', 'noun-pn': 'NP', 'pron': 'NP', 'expl-pron': 'NP', 'det': 'NP', 'card': 'NP', 'carddef': 'NP', 'det-quant': 'NP', 'quant': 'NP', 'poss': 'NP', 'proper-noun': 'NP', 'adj': 'AP', 'adj-adv': 'AP', 'mainverb': 'VP', 'verb': 'VP', 'aux-verb': 'VP', 'subcompl-infcompl-verb': 'VP', 'sadv': 'SAdvP', 'cadv': 'CP', 'complementizer': 'CP', 'infcompl': 'InfP', 'subcompl': 'CP', 'condcompl': 'CP', 'subcompl-omcompl': 'CP', 'atfull': 'CP', 'relcompl': 'RP', 'adv': 'AdvP', 'verb': 'VP', 'conj': 'ConjP', 'start': 'S', 'continuative': 'Forb', 'adj-subcompl-infcompl-noun-prep': 'XP'} 


coord = False
interj = False
for avm in avms:
    # for functional analysis:
    functions = {}
    #
    parsetree = ''
    if 'interj-phrase & [' in avm:
        interj = True
    avmin = False
    spaces = 0
    arglevel = 0
    signembs = []
    orthin = False
    orthnr = 0
    stackin = False
    path = []
    pathtypes = []
    orth2rootpath = {}
    tag2type = {}
    orth = ''
    orthlist = []
    stackvalue = ''
    orthpath = ''
    path2pathtype = {}
    tags = ['$0']
    tag2value = {}
    tag2type = {}
    tag2tag = {}
    x = 1
    sadvinv = False
    sadvanal = False
    word = ''
    gram = ''
    prevgram = ''
    for line in avm[1:]:
        if 'coord-vp-phrase' in line or 'conj-s-phrase' in line:
            coord = True

        items = line.lstrip().split()
        feature = items[0]
        if items[1][0] == '#':
            tag = items[1]
            if tag[-1] == ',':
                tag = tag[:-1]
            if len(items) > 3 and not items[3] == ']':
                mytype = items[3]
                if mytype[-1] == ',':
                    mytype = mytype[:-1]
                tag2type[tag] = mytype
        else:
            tag = '$'+str(x)
            x = x+1
            mytype = items[1]
            if mytype[-1] == ',':
                mytype = mytype[:-1]
            tag2type[tag] = mytype

        if not '[' in prevline:
            path.pop()
            pathtypes.pop()
            if ']' in prevline:
                previtems = prevline.lstrip().split()
                for item in previtems:
                    if ']' in item:
                        path.pop()
                        pathtypes.pop()
                        tags.pop()
                tags.pop()
                tags.append(tag)
            else:
                tags.pop()
                tags.append(tag)
        else:
            tags.append(tag)
        mothertag = tags[-2]
        tag2value[mothertag] = tag2value.get(mothertag, []) + [[feature, tag]]
        path.append(feature)
        pathtypes.append(feature+'@'+tag+'@'+mytype)
        emb = len(path)
        if 'ARGS cons & [\n' in line:
            arglevel = arglevel+1
            signemb = emb
            signembs.append(signemb)
            parsetree = parsetree + '['
        try:
            if 'REST cons & [\n' in line and signembs[-1]+1 == emb:
                parsetree = parsetree + ']'
                parsetree = parsetree + '['
        except:
            pass
        if len(signembs)>0:
         if 'REST null ]' in line and signembs[-1]-1 == emb:
            parsetree = parsetree + ']'
            signembs.pop()
            arglevel = arglevel-1
        if 'STEM ' in line and 'orthography & [' in line:
            orthin = True
        if 'REST null' in line and orthin:
            orthin = False
        if orthin and 'FIRST' in line:
            items = line.split()
            orth = items[-1]
            if orth[0] == '"':
                orth = orth + '_' + str(orthnr)
                orthnr = orthnr+1
                orthlist.append(orth)
                orth2rootpath[orth] = path[:]
            parsetree = parsetree + orth
        if len(path) > 3:
            if path[-4:] == ['SYNSEM', 'LOCAL', 'CAT', 'STACK'] and not 'STACK' in path[:-4]:
                stackin = True
                stackemb = len(path)

        if stackin:
            if not 'STACK' in path:
                stackin = False

        prevline = line
    lastpath = ['ARGS','FIRST']
    while not mytype == 'start-word' and not mytype == 'string':
        lastpath = lastpath + ['ARGS','FIRST']
        tag = path2tag(lastpath)
        mytype = tag2type[tag]
    
    def listlen(path):
        tag = path2tag(path)
        mytype = tag2type[tag]
        x=0
        while not mytype == 'null':
            path = path + ['REST']
            tag = path2tag(path)
            mytype = tag2type[tag]
            x=x+1
        return x
    
    
    olddepth = 0
    oldslash = 'null'
    gapbranch = 'gapbranch'
    if tex:
        stacktree = '\\Tree [.S '
    else:
        stacktree = '[ S '
        javatree = '<div class="tree">\n<ul>\n<li>\n<a href="#">S</a>\n<ul>\n'
    tag2ind = {}
    ind2gram = {}
    indices = ['n','m','l','k','j','i']
    elist = set(['null','0-1-list',''])
    nelist = set(['cons','1-list'])
    while len(lastpath) > 0:
        tag = path2tag(lastpath)
        mytype = tag2type[tag]
        stackpath = lastpath + ['SYNSEM','LOCAL','CAT','STACK']
        stacktype = path2type(stackpath)
        mstackpath = lastpath[2:] + ['SYNSEM','LOCAL','CAT','STACK']
        mstacktype = path2type(mstackpath)
        newdepth = listlen(mstackpath)
        slashpath = lastpath + ['SYNSEM','NON-LOCAL','SLASH']
        try:
            slashtype = path2type(slashpath)
            slashtag = path2tag(slashpath + ['FIRST','CAT','HEAD'])
        except:
            slashtype = ''
            slashtag = ''
        mslashpath =  lastpath[:-2] + ['SYNSEM','NON-LOCAL','SLASH']
        try:
            mslashtag = path2tag(mslashpath)
            mslashtype = path2type(mslashpath)
        except:
            mslashtype = ''
            mslashtag = ''
        vblpath = lastpath + ['SYNSEM', 'LOCAL', 'CAT', 'VBL']
        vbltype = path2type(vblpath)
        mvblpath = lastpath[:-2] + ['SYNSEM', 'LOCAL', 'CAT', 'VBL']
        mvbltype = path2type(mvblpath)
        subjpath = lastpath + ['SYNSEM', 'LOCAL', 'CAT', 'ARGUMENT', 'LOCAL', 'CAT', 'CASE', 'SU']
        msubjpath =  lastpath[:-2] + ['SYNSEM','LOCAL', 'CAT', 'CASE', 'SU']
        try:
            subjtype = path2type(msubjpath)
        except:
            subjtype = 'bool'
        tensepath = vblpath + ['LOCAL', 'CONT', 'HOOK', 'INDEX', 'E', 'TENSE']
        try:
            tensetype = path2type(tensepath)
        except:
            tensetype = 'tense'
        headpath = lastpath[:-2] + ['SYNSEM', 'LOCAL', 'CAT', 'HEAD']
        perfpath = lastpath[:-2] + ['ARGS','REST','FIRST','SYNSEM','LOCAL', 'CAT', 'HEAD', 'PERFPART' ]
        try:
            perf = path2type(perfpath)
        except:
            perf = '-'
        headtag = path2tag(headpath)
        indpath = lastpath + ['SYNSEM', 'LOCAL', 'CONT', 'HOOK','INDEX']
        indtag = path2tag(indpath)
        mindpath = lastpath[:-2] + ['SYNSEM', 'LOCAL', 'CONT', 'HOOK','INDEX']
        mindtag = path2tag(mindpath)
        try:
            mheadtag = path2tag(headpath[2:])
        except:
            mheadtag = headtag
        headtype = path2type(headpath)
        argrestpath = lastpath[:-1] + ['REST']
        argresttype = path2type(argrestpath)
        try:
            mtype = path2type(lastpath[2:])
        except:
            mtype = ''
        try:
            phrkey = path2type(lastpath[2:] + ['SYNSEM','--PHR-KEY'])
        except:
            phrkey = 'relation'
        try:
            keypred = path2type(lastpath + ['SYNSEM','LKEYS','KEYREL','PRED'])
        except:
            keypred = 'predtype'
        head = type2phrase[headtype]
        prevprevgram = prevgram
        prevgram = gram
        gram = gramfunc(phrkey[3],subjtype,tensetype,head,mtype,perf,keypred)
        if word == 'Conj':
            gram = prevprevgram
        if 'arg' in phrkey:
            if phrkey[3] == '1':
                gram = 'Subj'
            arg = '_' + gram + '_' + phrkey[3]
        else:
            arg = '_' + gram
        index = ''
        if stacktype in elist and mstacktype in nelist:
            mstackslashpath = mstackpath + ['FIRST','NON-LOCAL','SLASH']
            try:
                mstackslashtype = path2type(mstackslashpath)
            except:
                mstackslashtype = '0-1-list'
            if (mstackslashtype in nelist and slashtype in elist) or (mslashtype in nelist and slashtype in elist and mstackslashtype in elist):
                slashtag = mindtag
                tag = slashtag[1:]
                if not tag in tag2ind.keys():
                    tag2ind[tag] = indices.pop()
                if tex:
                    index = '_{' + tag2ind[tag]+ '}'
                else:
                    index = '_' + tag2ind[tag]
                    ind2gram[index[1:]] = gram
        try:
            phrase = type2phrase[headtype] + arg
        except:
            phrase = '?'
        if newdepth > olddepth:
            x = newdepth - olddepth
            while x > 0:
                if tex:
                    stacktree = stacktree + '[.'
                else:
                    stacktree = stacktree + '[ '
                    javatree = javatree + '<li>\n'
                phrase = phrase + index
                stacktree = stacktree + phrase + ' '
                javatree = javatree + '<a href="#">'+phrase + '</a>\n<ul>\n'
                x=x-1
        elif newdepth < olddepth:
            x = olddepth - newdepth
            while x > 0:
                stacktree = stacktree + '] '
                javatree = javatree + '</li>\n</ul>\n'
                x=x-1
        elif argresttype in elist and mslashtype in elist and slashtype in nelist:
            tag = path2tag(slashpath + ['FIRST','CAT','HEAD'])
            slashhead = tag2type[tag]
            slashindtag = path2tag(slashpath + ['FIRST','CONT','HOOK','INDEX'])
            tag = slashindtag[1:]
            try:
                if tex:
                    index = '_{' + tag2ind[tag]+ '} '
                else:
                    index = '_' + tag2ind[tag]#+ ' '
            except:
                if tex:
                    index = '_{j} '
                else:
                    index = '_j'
#            falsefunc = ind2gram[index[1:-1]]+index[:-1]
#            rightfunc = gram+index[:-1]
#            stacktree = stacktree.replace(falsefunc,rightfunc)
#            javatree = javatree.replace(falsefunc,rightfunc)
            phrase = type2phrase[slashhead] + arg + index
            stacktree = stacktree + phrase + ' '
            # Add empty node with gap
            # javatree = javatree + '<li><a href="#">'+phrase + '</a>\n'
            gapbranch = phrase

        elif argresttype == 'null' and vbltype == 'synsem' and mvbltype == 'anti-synsem':
            word = type2word['pron']
            stacktree = stacktree + word + ' '
            javatree = javatree + '<a href="#">'+word + '</a>\n<ul>\n'

        # Words
        if not argresttype == 'null':
            head = path2type(argrestpath + ['FIRST','SYNSEM','LOCAL','CAT','HEAD'])
            try:
                word = type2word[head]
                gram = gramfunc(phrkey[3],subjtype,tensetype,word,mtype,perf,keypred)
                if gram in set(['Vfin','Vinfin','SAdv','PPobj']):
                    word = word + '_' + gram
            except:
                if interj:
                    word = 'Interj'
                else:
                    word = '?'
            if gram == 'DegAdv':
                word = 'DegAdv'
            if tex:
                stacktree = stacktree + '[.' + word + ' '
            else:
                stacktree = stacktree + '[ ' + word + ' '
                javatree = javatree + '<li>\n<a href="#">'+word + '</a>\n<ul>\n'

            orth = path2type(argrestpath + ['FIRST','STEM','FIRST'])
            orthpath = argrestpath + ['FIRST','STEM','REST']
            rest = path2type(orthpath)
            while rest == 'cons':
                orth = orth[:-1] + ' ' + path2type(orthpath + ['FIRST'])[1:]
                orthpath.append('REST')
                rest = path2type(orthpath)
            if orth == '"unknown"' or orth == '*top*':
                orth = path2type(argrestpath + ['FIRST','STEM','FORM'])
                # use stems instead of fullforms
                # orth = path2type(argrestpath + ['FIRST','STEM','FIRST'])

            if 'cons' in path2type(argrestpath + ['REST']):
                print path2type(argrestpath + ['FIRST','REST','FIRST','STEM','FORM'])
            z = 0
            while not orth[0] == '"':
                argrestpath = argrestpath + ['FIRST','ARGS']
                head = path2type(argrestpath + ['FIRST','SYNSEM','LOCAL','CAT','HEAD'])
                z = z+1
                orth = path2type(argrestpath + ['FIRST','STEM','FIRST'])
            if orth[0] == '"':
                orth = orth[1:-1]
            orth = orth
            stacktree = stacktree + orth  + ' ] '
            javatree = javatree + '<li>\n<a href="#">'+orth + '</a>\n</li>\n</ul>\n'
        lastpath = lastpath[2:]
        olddepth = newdepth
        oldslash = slashtype
    stacktree = stacktree + ']'
    javatree = javatree + '</li>\n</ul>\n</li>\n</ul>\n</div>\n'
    gapitems = gapbranch.split('_')
    javatree = javatree.replace('Forb_Adv','Forb')
    javatree = javatree.replace('RP_Adv','RelS')
    javatree = javatree.replace('SAdv_SAdv','SAdv')
    javatree = javatree.replace('_1','')
    javatree = javatree.replace('_2','')
    javatree = javatree.replace('_3','')
    javatree = javatree.replace('_4','')
    if len(gapitems) == 4:
        javatree = javatree.replace(gapitems[0]+'_'+gapitems[3],gapitems[0]+'_'+gapitems[1])
    if 'Conj' in javatree:
        items = javatree.split('\n')
        restitems = items[:]
        parsed = []
        depth = 0
        conjnum = 0
        for item in items:
            if item == '<ul>':
                depth = depth + 1
            elif item == '</ul>':
                depth = depth - 1
            parsed2 = parsed[:]
            if item == '<a href="#">Conj</a>':
                catdepth = depth
                cat = restitems[7][12:].split('_')[0]
                parsed.reverse()
                parsed2 = []
                for item2 in parsed:
                    if item2[12:].split('_')[0] == cat:
                        try:
                            func = item2[12:].split('_')[1]
                            item2 = '<a href="#">'+cat+'_'+func+'</a>'
                        except:
                            item2 = '<a href="#">'+cat+'</a>'
                        if conjnum == 0:
                            javatree1 = javatree
                            javatree = ''
                            parsed2=parsed2+['<a href="#">'+cat+'</a>', '<li>', '<ul>']
                    parsed2.append(item2)
                parsed2.reverse()
                conjnum = conjnum + 1
                depth2=catdepth
                rest2 = []
                inconj = False
                for item2 in restitems:
                    if item2 == '<ul>':
                        depth2 = depth2 + 1
                    elif item2 == '</ul>':
                        depth2 = depth2 - 1
                    if depth2 == catdepth and inconj and restitems[3] == '<a href="#">og</a>':
                        rest2 = rest2+ ['</ul>','</li>']
                        inconj = False
                    if depth2 == catdepth:
                        if item2[12:].split('_')[0] == cat and not inconj:
                            inconj = True
                            item2 = '<a href="#">'+cat+'</a>'
                    rest2.append(item2)
                newlist = parsed2+rest2
                if restitems[3] == '<a href="#">og</a>':
                    for item3 in newlist:
                        javatree = javatree + item3 + '\n'
            restitems = restitems[1:]
            parsed = parsed2
            parsed.append(item)
    javatree = javatree.replace('NP_Adv','NP')
    if javatree == '':
        try:
            javatree = javatree1
        except:
            javatree = ''
            
#    treeFile.write(javatree)
 

    if '_Adv_i' in stacktree:
        treeitems = stacktree.split()
        for item in treeitems:
            if '_i' in item:
                func = item.split('_')[1]
        stacktree = stacktree.replace('_Adv_i','_'+func+'_i')
        javatree = javatree.replace('_Adv_i','_'+func)
#    if 'NP_Adv' in javatree:
#        javatree = javatree.replace('NP_Adv','NP_'+func)
    javatree = javatree.replace('_Subj_i','_Subj')
    treeData = '[ { "name": "S", "parent": "null", "children": [ '
    treeitems = stacktree.split()
    mother = 'S'
    levelnode = {}
    level = 0
    levelnode[0] = 'S'
    previtem = ''
    item = ''
    for nextitem in treeitems[2:]:
        if previtem == ']':
            if item == ']':
                treeData = treeData + ' } ]'
            else:
                treeData = treeData + ' }, '
        if item == ']':
            level = level -1
        elif item == '[':
            level = level + 1
        elif not item == '[' and not item == ']' and not item == '':
            if previtem == '[':
                levelnode[level] = item
                treeData = treeData + '{ "name": "'+item+'", "parent": "'+levelnode[level-1]+'", "children": [ '
            elif not previtem == '[' and not previtem == ']':
                treeData = treeData + '{ "name": "'+item+'", "parent": "'+levelnode[level]+'" } ]'
            else:
                if nextitem == ']':
                    treeData = treeData + '{ "name": "'+item+'", "parent": "'+levelnode[level]+'" '
                else:
                    treeData = treeData + '{ "name": "'+item+'", "parent": "'+levelnode[level]+'" }, '
                    
        previtem = item
        item = nextitem
    treeData = treeData.replace('Forb_Adv','Forb')
    
    treeData = treeData.replace('_Adv_i','_i')
    treeData = treeData.replace('_1','')
    treeData = treeData.replace('_2','')
    treeData = treeData.replace('_3','')
    treeData = treeData.replace('_4','')
    treeData = 'var treeData = ' + treeData + ' } ] } ]'
    treeData = treeData.replace('_Subj','su')
    treeData = treeData.replace('_Vfin','fin')
    treeData = treeData.replace('_Vinfin','infin')
    treeData = treeData.replace('_DO','do')
    treeData = treeData.replace('_IO','io')
    treeData = treeData.replace('_Adv','adv')
    treeData = treeData.replace('_SAdv','sa')
#    treeDataFile.write(treeData)
#    Attempt to bulild a field analysis
    fields = '<table border="1">\n  <tr>\n    <th>Forbinder</th> <th>Forfelt</th> <th colspan="3">Midtfelt</th> <th colspan="3">Sluttfelt</th>\n  </tr>\n  <tr>\n    <td></td> <td></td> <td>v</td> <td>n</td> <td>a</td> <td>V</td> <td>N</td> <td>A</td>\n  </tr>\n  <tr>\n'
    fields1 = '<table border="1">\n  <tr>\n    <th>Forbinder</th> <th>Forfelt</th> <th colspan="3">Midtfelt</th> <th colspan="3">Sluttfelt</th>\n  </tr>\n  <tr>\n    <td></td> <td></td> <td>v</td> <td>a</td> <td>n</td> <td>V</td> <td>N</td> <td>A</td>\n  </tr>\n  <tr>\n'
    level = 0
    inbr = False
    orth = False
    func = ''
    constnr = 0
    const2func = {}
    const2string = {}
    n = False
    analysis = {'Forbinder': '', 'Forfelt': '', 'v': '', 'a': ''}
    constituents = ['','','','','','','','',]
    line1 = '<th>Forbinder</th>'
    line2 = ''
    line3 = ''
    fffunc = ''
    forbinder = False
    degadv = False
    stacktree = stacktree.replace(' NP_Subj_1_i ', ' ')
    stacktree = stacktree.replace(' NP_Subj_2_i ', ' ')
    stacktree = stacktree.replace(' NP_Subj_1_j ', ' ')
    stacktree = stacktree.replace(' NP_Subj_2_j ', ' ')
    if 'DegAdvXXX' in stacktree:
        degitems = stacktree.split()
        previtems = []
        restitems = degitems[:]
        x = 0
        for degitem in degitems:
            if x == 0:
                previtems.append(degitem)
                restitems=restitems[1:]
                if degitem == 'DegAdv':
                    previtems = previtems[:-1] + [restitems[3]] + [restitems[4]] + [degitem] + restitems[:2] 
                    restitems = restitems[4:]
                    x=4
                stacktree = ''
                for previtem in previtems:
                    stacktree = stacktree + previtem + ' '
                stacktree = stacktree[:-1]
            else:
                x = x-1    
    if 'DegAdv' in javatree:
        javaitems = javatree.split('\n')
#        print javaitems
        previtems = []
        restitems = javaitems[:]
        x = 0
        for javaitem in javaitems:
            if x == 0:
                previtems.append(javaitem)
                restitems=restitems[1:]
                if javaitem == '<a href="#">DegAdv</a>':
                    previtems = previtems[:-1] + [restitems[6]] + [restitems[7]] + [restitems[8]] + [javaitem] + restitems[:5] 
                    restitems = restitems[8:]
                    x=8
                javatree = ''
                for previtem in previtems:
                    javatree = javatree + previtem + ' '
                javatree = javatree[:-1]
            else:
                x = x-1
    for item in stacktree.split():
        if item == '[':
            level = level+1
            inbr = True
            orth = False
            if level == 2:
                constnr = constnr + 1
        elif item == ']':
            inbr = False
            orth = False
            level = level-1
        elif inbr == True and orth == False:
            orth = True
            if level == 2:
                if len(item.split('_')) > 1:
                    func = item.split('_')[1]
                    cat = item.split('_')[0]
                else:
                    func = item
                    cat = item
               #        if level == 2 and not item == ']' and not item == '[' and not constnr == 1:
#            print item

        elif inbr == True and orth == True:
            const2string[str(constnr)]=const2string.get(str(constnr),'')+item + ' '
            if constnr>1:
                if const2func[str(constnr-1)]=='Conj':
                    item = const2string[str(constnr-1)]+item
                    #func = const2func[str(constnr-2)]
                    constnr = constnr-2
            if item[0] == ',':
                item = item[2:]
            if constnr == 1 and cat == 'Forb':
                analysis['Forbinder'] = analysis['Forbinder'] + item + ' '
                forbinder = True
            if constnr == 1 and func == 'DegAdv':
                degadv = True
            vforms = set(['Vfin','Vinfin'])
            if (constnr == 1 and not forbinder and not func in vforms) or (constnr == 2 and forbinder and not func in vforms) or (constnr == 2 and degadv and not func in vforms):
            #if (constnr == 1 and not forbinder and not func == 'Vfin' and not func == 'Vinfin') or (constnr == 2 and forbinder and not func == 'Vfin') or (constnr == 2 and degadv and not func == 'Vfin'):
                analysis['Forfelt'] = analysis['Forfelt'] + item + ' '
                fffunc = func
            elif func == 'Vfin':
                analysis['v'] = analysis['v'] + item + ' '
            elif func == 'Vinfin' and constnr == 1:
                analysis['V'+str(constnr)] = analysis.get('V'+str(constnr), '') + item + ' '
            else:# (not forbinder and constnr > 1) or (forbinder and constnr > 2):
                if func == 'Subj':
                    analysis['n'+str(constnr)] = analysis.get('n'+str(constnr), '') + item + ' '
                    if sadvanal:
                        fields = fields1
                        sadvinv = True
                if func == 'SAdv':
                    analysis['a'+str(constnr)] = analysis.get('a'+str(constnr), '') + item + ' '
                    sadvanal = True
                    if n:
                        keylist = analysis.keys()
                        for key in keylist:
                            if key[:1] == 'N':
                                analysis['n'+key[1:]] = analysis[key]
                                del analysis[key]
                if func == 'PRT':
                    if n:
                        analysis['A'+str(constnr)] = analysis.get('A'+str(constnr), '') + item + ' '
                    else:
                        analysis['V'+str(constnr)] = analysis.get('V'+str(constnr), '') + item + ' '
                if func == 'Adv' or func == 'PPobj':
                    analysis['A'+str(constnr)] = analysis.get('A'+str(constnr), '') + item + ' '
                if func == 'DO' or func == 'IO' or func == 'Pred' or func == 'DegAdv' or func == 'RFL':
                    analysis['N'+str(constnr)] = analysis.get('N'+str(constnr), '') + item + ' '
                    n = True
                if func == 'Vinfin':
                    analysis['V'+str(constnr)] = analysis.get('V'+str(constnr), '') + item + ' '
            const2func[str(constnr)] = func

    funckeys = analysis.keys()
    mouseOverStyle = 'style="background-color:#DDFFFF;color:#000000;text-decoration:none">'
    fields = fields + '    <td>' + analysis['Forbinder'] + '</td>'
    fields = fields + '<td><a href=" " title="'+fffunc+'"' + mouseOverStyle + analysis['Forfelt'] + '</a></td>'
    fields = fields + '<td><a href="syntaksveiledning/syntaks-kap-h003.html#sec8" title="Finitt verbal"'+ mouseOverStyle  + analysis['v'] + '</a></td>'
    if sadvinv:
        fields = fields + '<td>'
        keylist = analysis.keys()
        keylist.sort()
        for key in keylist:
            if key[:1] == 'a':
                fields = fields + '<a href=" " title="Setningsadverbial"'+ mouseOverStyle  + analysis['a'+key[1:]][:-1] + ' </a>'

        fields = fields + '</td>'
        keylist = analysis.keys()
        keylist.sort()
        for key in keylist:
            if key[:1] == 'n':
                fields = fields + '<td><a href=" " title="Subjekt"'+ mouseOverStyle + analysis['n'+key[1:]][:-1] + '</a>'
        fields = fields + '</td>'
    else:
        fields = fields + '<td>'
        keylist = analysis.keys()
        keylist.sort()
        for key in keylist:
            if key[:1] == 'n':
                fields = fields + '<a href=" " title="'+const2func[key[1:]]+'"'+ mouseOverStyle + analysis['n'+key[1:]][:-1] + '</a> '

        fields = fields + '</td>'
        fields = fields + '<td>'
        keylist = analysis.keys()
        keylist.sort()
        for key in keylist:
            if key[:1] == 'a':
                fields = fields + '<a href=" " title="Setningsadverbial"'+ mouseOverStyle  + analysis['a'+key[1:]][:-1] + ' </a>'
        fields = fields + '</td>'
    fields = fields + '<td>'
    keylist = analysis.keys()
    keylist.sort()
    for key in keylist:
        if key[:1] == 'V':
            fields = fields + '<a href=" " title="'+const2func[key[1:]]+'"'+ mouseOverStyle  + analysis['V'+key[1:]][:-1] + ' </a>'    
    fields = fields + '</td>'
    fields = fields + '<td>'
    keylist = analysis.keys()
    keylist.sort()
    for key in keylist:
        if key[:1] == 'N':
            fields = fields + '<a href=" " title="'+const2func[key[1:]]+'"'+ mouseOverStyle  + analysis['N'+key[1:]][:-1] + '</a> '
    fields = fields + '</td><td>'
    keylist = analysis.keys()
    keylist.sort()
    for key in keylist:
        if key[:1] == 'A':
            fields = fields + '<a href=" " title="'+const2func[key[1:]]+'"'+ mouseOverStyle  + analysis['A'+key[1:]][:-1] + '</a> '
    fields = fields + '</td>\n  </tr>\n</table>'
    fields = fields.replace('<a href=" " title="Subj"','<a href="syntaksveiledning/syntaks-kap-h003.html#sec9" title="Subjekt"')
    fields = fields.replace('<a href=" " title="DO"','<a href="syntaksveiledning/syntaks-kap-h003.html#sec13" title="Direkte objekt"')
    fields = fields.replace('<a href=" " title="IO"','<a href="syntaksveiledning/syntaks-kap-h003.html#sec13" title="Indirekte objekt"')
    fields = fields.replace('<a href=" " title="Pred"','<a href="syntaksveiledning/syntaks-kap-h003.html#sec17" title="Predikativ"') # 
    fields = fields.replace('<a href=" " title="Adv"','<a href="syntaksveiledning/syntaks-kap-h003.html#sec20" title="Adverbial"')
    fields = fields.replace('<a href=" " title="PRT"','<a href="syntaksveiledning/syntaks-kap-h004.html#sec42" title="Partikkel"')
    fields = fields.replace('<a href=" " title="PPobj"','<a href="syntaksveiledning/syntaks-kap-h004.html#sec42" title="Preposisjonsobjekt"')
    fields = fields.replace('<a href=" " title="Vinfin"','<a href="syntaksveiledning/syntaks-kap-h003.html#sec8" title="Infinitt verbal"')
    fields = fields.replace(' ,',',')
    fields = fields.replace(', og',' og')
#    tabularData.write(fields)
#    tabularFile.write(fields)
#    resultFile.write('    <tr>\n      <td>\n        '+str(number)+'\n')
    print '    <tr>\n      <td>\n        '+str(number)
#    javatree = javatree.replace('<a href="#">NP_Subj_i </a>','<a href="syntaksveiledning/syntaks-kap-h003.html#sec9" title="Subjekt"style="background-color:#DDFFFF;color:#000000;text-decoration:none">NP_i </a>')
    if coord:
        print 'Analysen har flere koordinerte setninger eller verbfraser. Del setningen opp og prøv igjen med én og én setning.'
    else:
        print javatree
    #<div w3-include-html="analyses/' + sys.argv[1][5:-4]+'.tree.html"></div>\n
    print '      </td>\n      <td>'
    if not coord:
        print fields
    #<script>\n          w3IncludeHTML();\n        </script>\n        <br>\n        <div w3-include-html="analyses/' + sys.argv[1][5:-4]+'.tab.html"></div>\n        <script>\n          w3IncludeHTML();\n        </script>\n
    print '</td></tr>'

