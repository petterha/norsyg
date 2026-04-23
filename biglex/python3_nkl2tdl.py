#!/usr/bin/env python
#-*- coding: utf-8 -*-
###
### Program for converting Norsk Komputasjonelt Leksikon (NKL) into an
### LKB lexicon file. The program takes as input the files
### 'nkl_bm_u_fon.txt' and 'alle_verb.nkl' (and the file 'special-irr'
### in the Norsyg directory). They should be in the same directory as
### the program when it runs.
###
### Petter Haugereid, 29-11-2011
###

###
### Converting latin-1 into utf-8
###
import codecs
#f = codecs.open('../../resources/nkl/nkl100K.txt','r','latin-1')
f = codecs.open('../../resources/nkl/nkl_bm_u_fon.txt','r','latin-1')
content = f.read()
f.close()
f = open('../../resources/nkl/nkl_bm_u_fon.u8.txt', 'w')
f.write(content.encode('utf8'))
f.close()

h = codecs.open('../../resources/nkl/alle_verb.nkl','r','latin-1')
content = h.read()
h.close()
h = open('../../resources/nkl/alle_verb.u8.nkl', 'w')
h.write(content.encode('utf8'))
h.close()
former = open('former.txt','w')

###
### Opening read and write files
###
f=open('../../resources/nkl/nkl_bm_u_fon.u8.txt','r')
h=open('../../resources/nkl/alle_verb.u8.nkl','r')
k=open('../../resources/nkl/id-irr','w')
g=open('../../resources/nkl/nkl.tdl','w')
i=open('../../resources/nkl/irregs_nkl.tab','w')
j=open('../../resources/nkl/nkl-predicates.tdl','w')
l=open('nkl2lkb.txt','r')
m=open('../nor.tdl','r')
n=open('../../resources/nkl/nkl-types.tdl','w')
o=open('../../resources/nkl/nklle.tdl','w')
p=open('../lexicon.tdl','r')
q=open('../../resources/nkl/extra-lex.tdl','w')
r=open('../../resources/nkl/mass-nouns.txt','r')
s=open('../../resources/nkl/linktypes.tdl','w')


###
### Writing initial lines of the lexicon file, the irregs file, the lexical
### entry type file, and the predicates file
###
import time
import datetime
g.write(';;  -*- Mode: TDL; Coding: utf-8; -*- \n;;\n')
g.write(';;  Lexicon automatically derived from \n;;  Norsk Komputasjonelt Leksikon (')
g.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
g.write(';;  See \'license.txt\' for licence conditions\n;;\n\n')

i.write(';;  -*- Coding: utf-8; -*- \n;;\n')
i.write(';;  Irregs file automatically derived from \n;;  Norsk Komputasjonelt Leksikon (')
i.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
i.write(';;  See \'license.txt\' for licence conditions\n;;\n\n"\n')

j.write(';;  -*- Mode: TDL; Coding: utf-8; -*- \n;;\n')
j.write(';;  Type file for predicates automatically derived from \n;;  Norsk Komputasjonelt Leksikon  (')
j.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
j.write(';;  See \'license.txt\' for licence conditions\n;;\n\n\n')

o.write(';;  -*- Mode: TDL; Coding: utf-8; -*- \n;;\n')
o.write(';;  Lexical entry types automatically derived from \n;;  Norsk Komputasjonelt Leksikon (')
o.write(datetime.datetime.now().strftime("%d/%m/%Y") + ')\n')
o.write(';;  See \'license.txt\' for licence conditions\n;;\n\n')

###
### Reading file with mass nouns
###

massnouns = set([])
for line in r:
    massnoun = line[:-1]
    massnouns.add(massnoun)

###
### Reading existing lexicon file
###

oldpartlists = []
smallex = set([])

for line in p:
    if 'STEM' in line and not 'FIRST' in line:
        items = line.split('<')
        items2 = items[1].split('>')
        stem = items2[0]
        if len(stem.split(',')) == 1:
            stem = stem.replace(' ','')
            stem = stem.replace('"','')
            smallex.add(stem)
    if '-p,' in line:
        items = line.split()
        pred = items[-1][:-3]
        predlist = pred.split('-')
        oldpartlists.append(predlist)
    if '_p_rel,' in line:
        items = line.split()
        pred = items[-1][1:][:-7]
        oldpartlists.append([pred])
    if '_p_rel ' in line:
        for item in line.split():
            if '_p_rel' in item:
                pred = item[1:][:-6]
                oldpartlists.append([pred])
#smallex = set([])
		

###
### Setting variables
###
lexicon = {}
allines = f.readlines()			# Read all the lines into 'allines'

###
### Sorting the information from 'fullform_bm.txt'
### Creating a lexicon with seven fields:
### lexicon[previd]=[pregrunn,paraset,argset,taglist,supertype,icode,shorttag]
###
print('Reading in fullform lexicon')

def accent(out):
    out = out.replace('$1e','é')
    out = out.replace('$2e','è')
    out = out.replace('$2a','à')
    out = out.replace('$2o','ò')
    out = out.replace('$3e','ê')
    out = out.replace('$3o','ô')
    out = out.replace('$4a','ä')
    out = out.replace('$4u','ü')
    out = out.replace('$7c','ç')
    out = out.replace('$8n','ñ')
    out = out.replace('\'','-')
    return out


blocklex = set(['ene','toe','åe'])
previd = '0'
prevstem = ''
prevpos = ''
paralist = []
triggerset = set([])
funcset = set([])
funcrels = set([])
id2spellings = {}
for line in allines:
    items = line[:-1].split('\t')
    if len(items) > 3:
      if len(items[2]) > 2 and not items[2] in smallex and not items[2] in blocklex and 'pos=' in items[1]:
        fullf = accent(items[0])
        stem = accent(items[2])
        cats = items[1]
        idnr = items[3]
        myid = idnr+'@'+stem
        taglist = cats.split()
        form = [fullf,taglist]
        if fullf == stem:
            for tagitem in taglist:
                if tagitem[:4] == 'pos=':
                    pos = tagitem[4:]
        if not previd == myid and not prevstem in smallex:# and len(pregrunn) > 2:
            # if previd in multispelling:
            #     id2spellings[previd] = id2spellings.get(previd,0) + 1
            #     previd = previd + '@' + str(id2spellings[previd])
            lexicon[previd] = [prevstem,paralist,prevpos,'','','','']
            paralist = [form]
        elif previd == myid and not prevstem in smallex:
            paralist.append(form)
        prevpos = pos
        previd = myid
        prevstem = stem

spellingkeys = set(id2spellings.keys())
lexkeys = set(lexicon.keys())
for line in h:
    info = line[2:].split(').')[0]
    items = info.split(',[')
    stem = items[0].split(',')[0]
    idnr = items[0].split(',')[1]
    myid = idnr+'@'+stem
    code = items[1][:-1]
    inpar = 0
    codes = []
    newcode = ''
    for letter in code:
        if letter == '(':
            inpar = 1
        if letter == ')':
            inpar = 0
        if letter == ',' and inpar == 0:
            codes.append(newcode)
            newcode = ''
        else:
            newcode = newcode + letter
    codes.append(newcode)
    if myid in lexkeys:
        lexicon[myid][3] = codes




###
### Reading in the NorKompLeks codes
###
nkllines = l.readlines()
nklcodes = {}
for line in nkllines:
    words = line.split("\t")
    nklcode = words[0]
    args = words[1]
    arg2 = words[2]
    arg3 = words[3]
    arg4 = words[4][:-1]
    nklcodes[nklcode] = [args,arg2,arg3,arg4]
###
### Reading in norsyg le-types
###
argstlists = []
norlines = m.readlines()
nortypes = []
nortypes2 = []
for line in norlines:
    argstlist = []
    if ':=' in line and '_le' in line:
        items = line.split(' := ')
        nortype = items[0]
        nortypes = nortypes + [nortype]
        subp = nortype.split('_')
        argst = subp[0]
        links = argst[3:]
        links2 = links.split('-')
        for link in links2:
            argstlist = argstlist + [link]
        argstlist.sort()
    argstlists = argstlists + [argstlist]
    if ':=' in line:
        items = line.split(' := ')
        mytype = items[0]
        nortypes2 = nortypes2 + [mytype]

###
### Creating a Norsyg lexicon
###
exceptions = []
z=0
zz=0
identifier = 'xxx'
x=0
xx=0

###
### Making the lexicon alphabetical
###
print('Sorting lexicon')
def sortfunc(x,y):
	return cmp(x[1],y[1])
items=list(lexicon.items())
items.sort(sortfunc)

def inflpattern(fullforms,infllist):
    x = len(infllist)
    y = len(infllist)
    checkset = set([])
    for data in infllist:
        check = data[0]
        attrlist = data[1]
#        attrlist.sort()
        for attr in attrlist:
            check = check + attr
        checkset.add(check)
    for form in fullforms:
        oldattrs = set([])
        fullform = form[0]
        tagset = set(form[1])
        taglist = form[1]
        taglist.sort()
        for infldata in infllist:
            infl = infldata[0]
            attrs = infldata[1]
#            attrs.sort()
            ilen = len(infl)
            if ilen > 0:
                affix = fullform[-ilen:]
                stem = fullform[:-ilen]
            else:
                affix = ''
                stem = fullform
            if x == y:
                prevstem = stem
            if infl == affix:
                if prevstem == stem:
                    if set(attrs).issubset(tagset):
                        check = infl
                        for attr in attrs:
                            check = check + attr
                        if check in checkset:
                            x=x-1
                            checkset.remove(check)
    return x

        


###
### Looping through all the lexical entries and writing lexical entries.
###
print('Printing lexical entries')
partlists = []
preplists = []
advlist = []
framesets = []
frametypes = []
frset = set(framesets)
newtypes = []
newinfo = []
tokenset = set([])
idset = set([])
vrbset = set([])
prpset = set([])
prtset = set([])
for item in items:
    parttype = 'prep-p'
    partlist = []
    z=0
    for ite in item:
        if z == 0:
            #Converting the id integer into a string
            item = str(ite)
            z = 1
        else:
            #Letting the list of properties be value
            value = ite
    # Accounting for multiple word expressions
    if len(value[0].split(" ")) > 1:
        words = value[0].split(" ")
        newstring = words[0]
        namestring = words[0]
        for word in words[1:]:
            newstring = newstring + '","' + word
            if word[-1] == '.':
                word = word[:-1]+'_'
            namestring = namestring + '*' + word
        value[0] = namestring
    # Accounting for abbriviations (cand.mag., m.o.h.)
    elif len(value[0].split(".")) > 1:
        words = value[0].split(".")
        newstring = words[0]
        namestring = words[0]
        for word in words[1:]:
            newstring = newstring + '.' + word
            namestring = namestring + '*' + word
        value[0] = namestring
    # Accounting for words with slashes (km/h)
    elif len(value[0].split("/")) > 1:
        words = value[0].split("/")
        newstring = words[0]
        namestring = words[0]
        for word in words[1:]:
            newstring = newstring + '/' + word
            namestring = namestring + '_' + word
        value[0] = namestring
    # Accounting for entries with parenthesis (falloskult(us))
    elif '(' in value[0] and ')' in value[0]:
        value[0] = value[0].replace('(','')
        value[0] = value[0].replace(')','')
    else:
        newstring = value[0]
			

    ### Verbs
    partlist = []
    preplist = []
    if value[2] == 'verb':
        if value[3] == '':
            value[3] = ['trans1']
        value[6] = 'v'
        # Setting inflectional codes
        if inflpattern(value[1],[['e',['vform=inf']],['et',['vform=pret']],['a',['vform=pret']],['er',['vform=pres']]]) == 0 and (len(value[1]) == 17 or len(value[1]) == 20):
            value[5] = 'v1'
            former.write(value[0] + ' v1\n')
        elif inflpattern(value[1],[['e',['vform=inf']],['er',['vform=pres']],['te',['vform=pret']],['t',['vform=part']]]) == 0 and len(value[1]) == 12:
            value[5] = 'v2'
            former.write(value[0] + ' v2\n')
        elif inflpattern(value[1],[['e',['vform=inf']],['er',['vform=pres']],['de',['vform=pret']],['d',['vform=part']]]) == 0 and len(value[1]) == 12:
            value[5] = 'v3'
            former.write(value[0] + ' v3\n')
        elif inflpattern(value[1],[['',['vform=inf']],['r',['vform=pres']],['dde',['vform=pret']],['dd',['vform=part']]]) == 0 and len(value[1]) < 13:
            value[5] = 'v4'
            former.write(value[0] + ' v4\n')
        else:
            value[5] = 'v1'
            former.write(value[0] + ' vv\n')
            k.write(item + "\n")
            
        ### Finding particle verbs
        yy=0
        frlist = []
        frametype = ''
        for ent in value[3]:
            nklcode = ent.split('([')[0]
            argcode = ''
            typeset = set(['arg1+','arg1-','arg2+','arg2-','arg3+','arg3-','arg4+','arg4-','prt-'])
            typelist = []
            supertypes = []
            if nklcode == 'ditrans11':
                nklcode = 'trans11'
            if nklcode == 'ref15':
                nklcode = 'refl5'
            if nklcode == 'ref9':
                nklcode = 'refl9'
            if nklcode == 'trans':
                nklcode = 'trans1'
            if nklcode == 'intrans':
                nklcode = 'intrans1'
            ## skye
            if nklcode == 'nullv4':
                nklcode = 'nullv3'
            if '1' in nklcodes[nklcode][0]:
                argcode = argcode + '1'
                typelist.append('1np')
            else:
                typelist.append('arg1-')
                
            arg2 = nklcodes[nklcode][1]
            special2 = ''
            if arg2 in ['np','cp','ip1','cp-np','ip3']:
                argcode = argcode+'2'
                if arg2 == 'np':
                    typelist.append('2np')
                if arg2 == 'cp':
                    typelist.append('2cp')
                    special2 = '-cp'
                if arg2 == 'ip1':
                    typelist.append('2ip1')
                    special2 = '-ip1'
                # TODO: This type must be split up into two frames: (2015-02-10; ph)
                if arg2 == 'cp-np':
                    typelist.append('2cp')
                    special2 = '-cp'
                if arg2 == 'ip3':
                    typelist.append('2ip3')
            elif arg2 in ['refl']:
                typelist.append('refl')
                special2 = '-refl'
            else:
                typelist.append('arg2-')
#            elif arg2 == 'refl':
#                argcode = argcode+
            
            arg3 = nklcodes[nklcode][2]
            refl3 = ''
            if '3' in nklcodes[nklcode][0]:
                if arg3 in ['refl']:
                    typelist.append('refl')
                    refl3 = '-refl'
#                    argcode = argcode+'3'
                else:
                    typelist.append('3np')
            else:
                typelist.append('arg3-')
            arg4 = nklcodes[nklcode][3]
            special4 = ''
            if arg4 in ['pp','advp','infbare2','pp+ip1','pp+ip2','pp+cp']:
                argcode = argcode+'4'
                if arg4 == 'pp':
                    typelist.append('4np')
                if arg4 == 'advp':
                    typelist.append('4advp')
                if arg4 == 'infbare2':
                    special4 = '-infbare2'
                    typelist.append('4infbare2')
                if arg4 == 'pp+ip1':
                    typelist.append('4ip1')
                    special4 = '-ip1'
                if arg4 == 'pp+ip2':
                    typelist.append('4ip2')
                    special4 = '-ip2'
                if arg4 == 'pp+cp':
                    typelist.append('4cp')
                    special4 = '-cp'
            elif arg4 in ['pp+refl']:
                typelist.append('refl')
                special4 = '-refl'
            else:
                typelist.append('arg4-')
            supertypes = ''

            vrbset.add(value[0])
            for supertype in typelist:
                supertypes = supertypes + supertype + ' & '
            supertypes = supertypes[:-3]
            if '([' in ent and ent[:4] == 'part':
                items = ent.split('([')
                part = items[0]
                parts = items[1][:-2].split(',')
                if 'a' in parts:
                    print(parts)
                yy = 1
                for p in parts:
                    frametype = value[0] + refl3 + special2 + '-'+ p + '_' + nklcodes[nklcode][0] + '_rel := ' + value[0] + '_v' + ' & ' + p + '_prt & ' + supertypes + '.\n'
                    frametypes.append(frametype)
                    prtset.add(p)
                    if p not in partlist:
                        partlist = partlist+[p]
                        partlist.sort()
                frlist.append(part)
            elif '([' in ent:
                items = ent.split('([')
                prep = items[0]
                if items[1][-2:] == '])':
                    preps = items[1][:-2].split(',')
                else:
                    preps = items[1].split(',')
                for p in preps:
                    if '+' in p:
                        prt = p.split('+')[0]
                        prp = p.split('+')[1]
                        prtset.add(prt)
                        prpset.add(prp)
                        frametype = value[0] + refl3 + special2 +'-'+ prt +'*'+ prp + '_' + nklcodes[nklcode][0] + '_rel := ' + value[0] + '_v' + ' & ' + prt + '_prt & ' + prp + '_prp & ' + supertypes + '.\n'
                        frametypes.append(frametype)
                    
                    else:
                        frametype = value[0] + refl3 + special2 +'*'+ p + special4 + '_' + nklcodes[nklcode][0] + '_rel := ' + value[0] + '_v' + ' & ' + p + '_prp & ' + 'prt- & ' + supertypes + '.\n'
                        if not '_12_' in frametype:
                            frametypes.append(frametype)
                    
                        prpset.add(p)
                    if p not in preplist:
                        preplist = preplist+[p]
                        preplist.sort()
                frlist.append(prep)
            else:
                frametype = value[0] + refl3 + special2 + '_' + nklcodes[nklcode][0] + '_rel := ' + value[0] + '_v' + ' & ' + 'prt- & ' + supertypes + '.\n'
                frametypes.append(frametype)
                frlist = frlist + [ent]
        value[3] = set(frlist)
        #partlist = partlist+preplist
        partlist.sort()
        preplist.sort()
        if partlist not in partlists and len(partlist) > 0:
            partlists = partlists + [ partlist ]
        if preplist not in preplists and len(preplist) > 0:
            preplists = preplists + [ preplist ]
            yy = 0
        if len(partlist) > 1:
            parttype = partlist[0]
            for part in partlist[1:]:
                parttype = parttype + '-' + part
            parttype = parttype + '-p'
        if len(partlist) == 1:
            parttype = '_' + partlist[0] + '_p_rel'
        if len(preplist) > 1:
            preptype = preplist[0]
            for prep in preplist[1:]:
                preptype = preptype + '-' + prep
            preptype = preptype + '-p'
        if len(preplist) == 1:
            preptype = '_' + preplist[0] + '_p_rel'
        # Setting supertype
        framelist = []
        for item in value[3]:
            framelist = framelist + [item]
        # Setting argtype
        arglist = []
        framelist2 = []
        for item in framelist:
            if item == 'part':
                item = 'part1'
            if item == 'ref15':
                item = 'refl5'
            if item == 'ref9':
                item = 'refl9'
            if item == 'ditrans11':
                item = 'trans11'
            # if item == 'part1refl4':
            #     item = 'part1'
            if item == 'nullv4':
                item = 'nullv'
            if item == 'trans':
                item = 'trans1'
            if item == 'intrans':
                item = 'intrans1'
            framelist2 = framelist2 + [item]
            nkl = item
            args = nklcodes[nkl][0]
            arglist = arglist + [args]
        framelist = framelist2
        arglist.sort()
        argset = set(arglist)
        arglist = []
        for item in argset:
            arglist = arglist + [ item] 
        arglist.sort()
        argstlists = argstlists + [arglist]
        argtype = 'arg'
        for args in arglist:
            argtype = argtype + args + '-'
        if argtype == 'arg':
            argtype = 'arg1-12_np'
        else:
            argtype = argtype[:-1]
        # Setting arg2type
        arg2list = []
        for item in framelist:
            nkl = item
            arg2 = nklcodes[nkl][1]
            if '-' in arg2:
                arg2s = arg2.split('-')
                for item in arg2s:
                    arg2list = arg2list + [item]
            else:
                arg2list = arg2list + [arg2]
        arg2list.sort()
        arg2set = set(arg2list)
        arg2list = []
        for item in arg2set:
            arg2list = arg2list + [ item] 
        arg2list.sort()
		
        arg2type = ''
        for arg2 in arg2list:
            if not arg2 == "":
                arg2type = arg2type + '-' + arg2
        arg2type = arg2type[1:]
        arg2type = arg2type.replace('np-refl','np')
        arg2type = arg2type.replace('ip1-refl','ip1-np')
        arg2type = arg2type.replace('cp-refl','cp-np')
        arg2type = arg2type.replace('cp-ip1-ip3-np','cp-ip1-np')
        arg2type = arg2type.replace('cp-ip3-np','cp-ip3-np')
		
        # Setting arg3type
        arg3list = []
        for item in framelist:
            nkl = item
            arg3 = nklcodes[nkl][2]
            if '-' in arg3:
                arg3s = arg3.split('-')
                for item in arg3s:
                    arg3list = arg3list + [item]
            else:
                arg3list = arg3list + [arg3]
        arg3list.sort()
        arg3set = set(arg3list)
        arg3list = []
        for item in arg3set:
            arg3list = arg3list + [ item] 
        arg3list.sort()
        arg3type = ''
        for arg3 in arg3list:
            if not arg3 == "":
                arg3type = arg3type + '-' + arg3
        arg3type = arg3type[1:]
        arg3type = arg3type.replace('np-refl3','')
        arg3type = arg3type.replace('refl3','refl')


        # Setting arg4type
        arg4list = []
        for item in framelist:
            nkl = item
            arg4 = nklcodes[nkl][3]
            if '-' in arg4:
                arg4s = arg4.split('-')
                for item in arg4s:
                    arg4list = arg4list + [item]
            else:
                arg4list = arg4list + [arg4]
        arg4list.sort()
        arg4set = set(arg4list)
        arg4list = []
        for item in arg4set:
            if not item == 'infbare2':
                arg4list = arg4list + [ item] 
        arg4list.sort()
        arg4type = ''
        for arg4 in arg4list:
            if not arg4 == "":
                arg4type = arg4type + '-' + arg4
        arg4type = arg4type[1:]
        arg4type = arg4type.replace('pp-pp+ip1','pp+ip1')
        arg4type = arg4type.replace('pp-pp+ip2','pp+ip2')
        arg4type = arg4type.replace('pp-pp+cp-pp+ip1','pp+cp')
        arg4type = arg4type.replace('pp-pp+cp','pp+cp')
        arg4type = arg4type.replace('pp+cp-pp+refl','pp+cp')
        arg4type = arg4type.replace('pp-pp+refl','pp')
        arg4type = arg4type.replace('pp+ip1-refl','pp+ip1')
        arg4type = arg4type.replace('pp+ip1-pp+refl','pp+ip1')
        arg4type = arg4type.replace('pp+ip1-pp+ip2','pp+ip1')
        arg4type = arg4type.replace('ap-pp+cp-pp+ip2-pp+refl','ap-pp')
        arg4type = arg4type.replace('pp+cp-pp+ip2-pp+refl','pp')
        arg4type = arg4type.replace('ap-pp+cp','ap-pp')
        arg4type = arg4type.replace('pp+ip1-pp+refl','pp+ip1')
        arg4type = arg4type.replace('pp+ip1-pp+refl','pp+ip1')

        # Setting supertype
        stype = argtype
        if len(partlist) > 0 and not parttype == 'prep-p':
            stype = stype + '_part'
        if arg2type == "":
            pass
        else:
            stype = stype + '_' + arg2type
        if arg3type == 'refl':
            stype = stype + '_refl'
        if len(arg4type)>0:
            stype = stype + '_' + arg4type
        stype = stype + "_le"
        
        types = [stype,argtype,arg2type,arg3type,arg4type,parttype]
        if not stype in nortypes:
            newtypes = newtypes + [stype]
            newinfo = newinfo + [types]
#        value[4] = stype
        value[4] = 'main-verb-lxm'

	### Abbreviations
	
#    if value[2] == 'fork':
#        print value[3]
#        value[3][0:1] = []
        
	### Proper Nouns
	
    # if value[3][0] == 'subst' and 'prop' in value[3]:
    #     value[4] = 'pn-word'
    #     value[6] = 'pn'
        
# 	### Non-inflecting nouns
	
    if [0] == 'subst' and len(value[1]) == 'appell':
        value[4] = 'non-infl-noun-word'
        value[6] = 'n'

# 	### Prepositions
	
    if value[2] == 'prep':
        value[4] = 'func-word'
        value[6] = 'func'

# 	### Adverbs
	
    if value[2] == 'adv':
        value[4] = 'func-word'
        value[6] = 'func'

    if value[2] == 'adv' or value[2] == 'prep':
        pred = value[0]
        partlist = [pred]
        if partlist not in partlists:
            partlists = partlists + [ partlist ]
            
# 	### Nouns

    if value[2] == 'subst':
        value[6] = 'n'
        # Deciding the gender
        if 'gend=f' in value[1][0][1]:
            discr = 'fem'
        elif 'gend=m' in value[1][0][1]:
            discr = 'masc'
        elif 'gend=n' in value[1][0][1]:
            discr = 'neut'
        else:
            discr = ""
        # Setting the supertype
        if inflpattern(value[1],[['',['num=sg','form=ind']],['en',['num=sg','form=def']],['a',['num=sg','form=def']],['er',['num=pl','form=ind']],['ene',['num=pl','form=def']]]) == 0 and len(value[1]) == 8:
            value[4] = 'comm-noun-lxm'
            value[5] = 'm1'
            former.write(value[0] + ' f1\n')
        l1 = value[0][-1]
        if inflpattern(value[1],[['',['num=sg','form=ind']],['en',['num=sg','form=def']],['er',['num=pl','form=ind']],['ene',['num=pl','form=def']]]) == 0 or inflpattern(value[1],[['e'+l1,['num=sg','form=ind']],['e'+l1+'en',['num=sg','form=def']],[l1+'er',['num=pl','form=ind']],[l1+'ene',['num=pl','form=def']]]) == 0:# and len(value[1]) == 8:
            value[4] = 'masc-noun-lxm'
            value[5] = 'm1'
            former.write(value[0] + ' m1\n')
        if inflpattern(value[1],[['',['num=sg','form=ind']],['en',['num=sg','form=def']],['e',['num=pl','form=ind']],['ne',['num=pl','form=def']]]) == 0:# and len(value[1]) == 4:
            value[4] = 'masc-noun-lxm'
            value[5] = 'm2'
            former.write(value[0] + ' m2\n')
        l1 = value[0][-1]
        if inflpattern(value[1],[[l1,['num=sg','form=ind']],[l1+l1+'en',['num=sg','form=def']],[l1+l1+'er',['num=pl','form=ind']],[l1+l1+'ene',['num=pl','form=def']]]) == 0 and len(value[1]) == 4:
            value[4] = 'masc-noun-lxm'
            value[5] = 'm3'
            former.write(value[0] + ' m3\n')
        elif inflpattern(value[1],[['',['num=sg','form=ind']],['et',['num=sg','form=def']],['',['num=pl','form=ind']],['ene',['num=pl','form=def']],['a',['num=pl','form=def']]]) == 0:
            value[4] = 'neut-noun-lxm'
            value[5] = 'n1'
            former.write(value[0] + ' n1\n')
        elif inflpattern(value[1],[['e',['num=sg','form=ind']],['et',['num=sg','form=def']],['er',['num=pl','form=ind']],['ene',['num=pl','form=def']],['a',['num=pl','form=def']]]) == 0:
            value[4] = 'neut-noun-lxm'
            value[5] = 'n2'
            former.write(value[0] + ' n2\n')
        else:
            if len(value[1]) == 1:
                value[5] = 'inflection'
                value[4] = 'non-infl-noun-word'
            if 'gend=f' in value[1][0][1]:
                value[4] = 'comm-noun-lxm'
                former.write(value[0] + ' ff\n')

                if len(value[1]) > 1:
                    value[5] = 'm1'
            elif 'gend=m' in value[1][0][1]:
                value[4] = 'masc-noun-lxm'
                former.write(value[0] + ' mm\n')
                if len(value[1]) > 1:
                    value[5] = 'm1'
            elif 'gend=n' in value[1][0][1]:
                value[4] = 'neut-noun-lxm'
                if len(value[1]) > 1:
                    value[5] = 'n2'
                former.write(value[0] + ' nn\n')
            else:
                 value[4] = 'non-infl-noun-word'
                 value[5] = 'inflection'
            if value[0] in massnouns:
                value[4] = value[4].replace('noun','mass-noun')
            k.write(item + "\n")

#            exceptions = exceptions + [value[0]]
	
	### Adjectives
    if value[2] == 'adj':
        # Setting the supertype
        value[4] = 'adj-lxm'
        value[6] = 'a'
        l1 = value[0][-1]
			# Setting the inflectional code
        if inflpattern(value[1],[['',['grad=posi','form=ind','num=sg','gend=fm']],['e',['grad=posi','form=def']],['e',['grad=posi','num=pl']],['t',['grad=posi','form=ind','num=sg','gend=n']]]) == 0:
            value[5] = 'a1'
            former.write(value[0] + ' a1\n')
        elif inflpattern(value[1],[['',['grad=posi','form=ind','num=sg','gend=fm']],['',['grad=posi','form=def']],['',['grad=posi','num=pl']],['tt',['grad=posi','form=ind','num=sg','gend=n']]]) == 0:
            value[5] = 'a2'
            former.write(value[0] + ' a2\n')
        elif inflpattern(value[1],[['',['grad=posi','form=ind','num=sg','gend=fm']],['',['grad=posi','form=def']],['',['grad=posi','num=pl']],['',['grad=posi','form=ind','num=sg','gend=n']]]) == 0 and len(value[1]) == 4:
            value[5] = 'a3'
            former.write(value[0] + ' a3\n')
        elif inflpattern(value[1],[['et',['grad=posi','form=ind','num=sg','gend=fm']],['ede',['grad=posi','form=def']],['ede',['grad=posi','num=pl']],['et',['grad=posi','form=ind','num=sg','gend=n']]]) == 0 and len(value[1]) == 6:
            value[5] = 'a4'
            former.write(value[0] + ' a4\n')
        elif inflpattern(value[1],[['e'+l1,['grad=posi','form=ind','num=sg','gend=fm']],[l1+'e',['grad=posi','form=def']],[l1+'e',['grad=posi','num=pl']],['e'+l1+'t',['grad=posi','form=ind','num=sg','gend=n']]]) == 0 and len(value[1]) == 8:
            value[5] = 'a5'
            former.write(value[0] + ' a5\n')
        elif set(['000']) == value[1]:
            value[4] = 'adj-word'
        else:
            value[5] = 'a1'
            former.write(value[0] + ' aa\n')
            k.write(item + "\n")
            
	# Counting lexical entries that begin with '-' as 'exceptions'
    try:
        if value[0][0] == '-':
            value[6] = 'exception'
            exceptions = exceptions + [value[0]]
    except:
        pass
        #print value
    else:
        for letter in value[0]:
            # Counting lexical entries with funny characters as exceptions
            if letter == '\'' or letter == '$' or letter == '%' or letter == '.' or letter == '/':
                value[6] = 'exception'
                exceptions = exceptions + [value[0]]
                
	# Conditions for being printed as a lexical item
    lexentry = ''
    if value[6] == 'v' or value[6] == 'pn' or value[6] == 'n' or value[6] == 'a' or value[6] == 'func':
        # Writing the lexical entries
        unique = 0
        if value[6] == 'n':
            prevident = identifier
            identifier = value[0] + '-' + value[6] + '-' + discr
            if not identifier == prevident:
                line1 = value[0] + '-' + value[6] + '-' + discr + ' := ' + value[4]
                if not str.lower(line1) in tokenset:
                    lexentry = lexentry + line1 + ' &\n'
                    tokenset.add(str.lower(line1))
                    unique = 1
        else:
            prevident = identifier
            identifier = value[0] + '_' + value[6]
            line1 = identifier + ' := ' + value[4]
            if identifier in idset and not line1 in tokenset:
                identifier = identifier + '2'
                value[6] = value[6] + '2'
                if identifier in idset:
                    identifier = identifier[:-1] + '3'
                    value[6] = value[6][:-1] + '3'
                    if identifier in idset:
                        identifier = identifier[:-1] + '4'
                        value[6] = value[6][:-1] + '4'
                        if identifier in idset:
                            identifier = identifier[:-1] + '5'
                            value[6] = value[6][:-1] + '5'
                tokenset.add(line1)
            idset.add(identifier)
            if not identifier == prevident and not identifier + ' := ' + value[4] in tokenset:
                line1 = identifier + ' := ' + value[4]
                if not str.lower(line1) in tokenset:
                    lexentry = lexentry + line1 + ' &\n'
                    tokenset.add(str.lower(line1))
                    unique = 1
        if unique == 1:
            lexentry = lexentry + '  [ STEM <"' + newstring + '">,\n'
            if value[6][0] == 'v' or value[6] == 'n' or value[6] == 'a':
                if not value[5] == 'inflection':
                    lexentry = lexentry + '    INFLECTION ' + value[5] + ',\n'
 #           if value[6][0] == 'v' or value[6] == 'n' or value[6] == 'a':
 #               if len(partlist) > 0 and not parttype == 'prep-p':
 #                   partsat = '-'
 #                   for item in value[2]:
 #                       if 'part' not in item:
 #                           partsat = 'bool'
#                    if partsat == '-':
#                        lexentry = lexentry + '    SYNSEM.LOCAL.CAT.VAL.PART.SAT -,\n'
#                    lexentry = lexentry + '    SYNSEM.LKEYS.ALTKEYREL.PRED ' + parttype + ',\n'
 #               elif value[6][0] == 'v':
 #                   lexentry = lexentry + '    SYNSEM.LOCAL.CAT.VAL.PART.SAT +,\n'
 #           if value[6][0] == 'v' or value[6] == 'n' or value[6] == 'a':
 #               if len(preplist) > 0:
 #                   lexentry = lexentry + '    SYNSEM.LOCAL.CAT.VAL.CMP4.LKEYS.KEYREL.PRED ' + preptype + ',\n'
            if value[6] == 'adv':
                advlist = advlist + [value[0]]
            if value[2] == 'prep' or value[2] == 'adv':
                triggerset.add(value[0]+'-func_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+value[0]+'_prd ] !>,\n    FLAGS.TRIGGER "'+value[0]+'-func" ].\n\n')
                lexentry = lexentry + '    SYNSEM.LKEYS.KEYREL.PRED '+value[0]+'_prd ].\n\n'
                funcset.add(lexentry)
                if value[2] == 'prep':
                    funcrels.add(''+value[0]+'_prd := predsort.\n')
                    funcrels.add(''+value[0]+'_prt := '+value[0]+'_prd & prt+.\n')
                    funcrels.add(''+value[0]+'_prp := '+value[0]+'_prd & prp+.\n')
                    funcrels.add('_'+value[0]+'_p_rel := '+value[0]+'_prp & arg1+ & 2np & arg3- & arg4- & prt-.\n')
                if value[2] == 'adv':
                    funcrels.add(''+value[0]+'_prd := predsort.\n')
                    funcrels.add(''+value[0]+'_prp := '+value[0]+'_prd & prp+.\n')
                    funcrels.add('_'+value[0]+'_adv_rel := '+value[0]+'_prd & adv-link.\n')
            elif value[6] == 'v':
                lexentry = lexentry + '    SYNSEM.LKEYS.KEYREL.PRED '+value[0]+'_' + value[6] + ' ].\n\n'
                triggerset.add(value[0]+'-v_rule := arg0e_gtr &\n  [ CONTEXT.RELS <! [ PRED '+value[0]+'_v ] !>,\n    FLAGS.TRIGGER "'+value[0]+'-v" ].\n\n')

            elif value[6] == 'pn':
                lexentry = lexentry + '    SYNSEM.LKEYS.KEYREL.CARG "'+value[0]+'" ].\n\n'
            else:
                lexentry = lexentry + '    SYNSEM.LKEYS.KEYREL.PRED "_'+value[0]+'_' + value[6] + '_rel" ].\n\n'
                xx = xx+1
        g.write(lexentry)

print('Printed ' + str(xx) + ' lexical entries in \'nkl.tdl\'')


frstr = []
for frames in framesets:
     newfr = ''
     for item in frames:
          newfr = newfr + item
     frstr = frstr + [newfr]
     
frset = set(frstr)
newlist = []
for fset in frset:
     number = frstr.count(fset)
     if number > 5:
          newitem = str(number) + fset
          newlist = newlist + [newitem]
newlist.sort()

###
### Creating a type hierarchy of particle constellations and writing them to
### nkl-predicates.tdl
###
typedefs = []
partlists = partlists + preplists + oldpartlists
partlists2 = []
for p in partlists:
	if not p in partlists2:
		partlists2 = partlists2 + [p]
partlists = partlists2
for p in partlists:
    if not p[0][0] == '\'' and not p[0][0] == '-':
        if len(p) > 1:
            subtype = p[0]
            for part in p[1:]:
                subtype = subtype + '-' + part
            subtype = subtype + '-p'
        elif len(p) == 1:
            subtype = p[0]
            if subtype in advlist:
                subtype =  '_' + subtype + '_p_rel'
            else:
               subtype = '_' + subtype + '_p_rel'
        type2 = ' := '
        types = []
        for q in partlists:
            if set(p) < set(q):
                z = 1
                for r in partlists:
                    if set(r) < set(q) and set(p) < set(r):
                        z = 0
            if z == 1:
                type2 = q[0]
                for part in q[1:]:
                    type2 = type2 + '-' + part
                types = types + [type2]
                z = 1
        typedef = subtype + ' := '
        if types == []:
            typedef = typedef + 'prep-p.'
        else:
            if len(types[:-1]) > 19:
                typedef1 = subtype + '-1 := '
                for suptype in types[:17]:
                    typedef1 = typedef1 + suptype + '-p & '
                typedef1 = typedef1 + types[18] + '-p.'
                typedef2 = subtype + '-2 := '
                for suptype in types[19:][:-1]:
                    typedef2 = typedef2 + suptype + '-p & '
                typedef2 = typedef2 + types[-1] + '-p.'
                typedef = subtype + ' := ' + subtype + '-1 & ' + subtype + '-2.'
                typedefs = typedefs + [typedef1,typedef2]
            else:
                for item in types[:-1]:
                    typedef = typedef + item + '-p & '
                lasttype = types[-1:][0]
                typedef = typedef + lasttype + '-p.'
        typedefs = typedefs + [typedef]

typedefs.sort()

xx = 0
for typedef in typedefs:
	j.write(typedef + '\n')
	xx = xx+1
	
j.close()


#print 'Printed ' + str(xx) + ' types in \'nkl-predicates.tdl\''

###
### Creating a hash with lexical entry types of verbs as keys, their
### supertypes, represented as a string, as value[0], and the argument frame
### constellation (ARGFRAME value) as value[1]
###
typedefs = []
x = 0
newinfo2 = []
for item in newinfo:
	if not item in newinfo2:
		newinfo2 = newinfo2 + [item]
newinfo = newinfo2
typehash = {}
alltypes = []
for type in newinfo:
	supertypes = ''
	superlist = []
	# stlist = []
	# if len(type[2]) > 0:
	# 	arg2 = type[2]
	# 	super = 'arg2_' + arg2
	# 	superlist = superlist + [super]
	# if len(type[3]) > 0:
	# 	arg3 = type[3]
	# 	super = 'arg3_' + arg3
	# 	superlist = superlist + [super]
	# if len(type[4]) > 0:
	# 	arg4 = type[4]
	# 	super = 'arg4_' + arg4
	# 	superlist = superlist + [super]
	# if len(type[5]) > 0 and not type[5] == 'prep-p':
	# 	super = 'part-verb'
	# else:
	# 	super = 'non-part-verb'
	# superlist = superlist + [super]
	if len(superlist) == 0:
            supertypes == 'main-verb-lxm'
	# for item in superlist:
	# 	supertypes = supertypes + item + ' & '
	# 	alltypes = alltypes + [item]
	typehash[type[0]] = [supertypes]

newtypes2 = []
for type in newtypes:
	if not type in newtypes2:
		newtypes2 = newtypes2 + [type]
newtypes = newtypes2
newtypes.sort()

###
### Writing the _le types to the file 'nklle.tdl'
###
for item in newtypes:
	o.write(item + ' := ' + typehash[item][0] + '\n')
	o.write('  [ SYNSEM.LOCAL.CAT.VAL.ARGFRAME link ].\n\n')
	x = x+1

# allset = set(alltypes)
# for item in allset:
# 	if not item in nortypes2:
# 		print item
#print 'Printed ' + str(x) + ' types in \'nklle.tdl\''

###
### Adding the arg constellations that 'arg1-', 'arg1+', 'arg2-', 'arg2+',
### 'arg3-', 'arg3+', 'arg4-', and 'arg4+' represent, to the list of argument
### frame constellations
###
argstlists = argstlists + [['0','2','23','234','234','24','4'],['1','12','123','1234','124','14'],['12','123','1234','124','2','23','234','234','24'],['0','1','14','4'],['123','1234','23','234','234'],['0','1','12','124','14','2','24','4'],['1234','124','14','234','234','24','4'],['0','1','12','123','2','23'],['1','12','123','13']]

argstlists2 = []
for p in argstlists:
	if not p in argstlists2:
		argstlists2 = argstlists2 + [p]
argstlists = argstlists2

###
### Creating a type hierarchy of argument frame constellations and writing
### them to nkl-types.tdl
###
for p in argstlists:
    if len(p) > 0 and not  p[0] == '':
        subtype = 'arg' + p[0]
        for part in p[1:]:
            subtype = subtype + '-' + part
        type2 = ' := '
        types = []
        for q in argstlists:
            if set(p) < set(q):
                z = 1
                for r in argstlists:
                    if set(r) < set(q) and set(p) < set(r):
                        z = 0
                if z == 1:
                    type2 = q[0]
                    for part in q[1:]:
                        type2 = type2 + '-' + part
                    types = types + [type2]
                    z = 1
        typedef = subtype + ' := arg'
        if types == []:
            typedef = subtype + ' := link.'
        else:
            for item in types[:-1]:
                typedef = typedef + item + ' & arg'
            lasttype = types[-1:][0]
            typedef = typedef + lasttype + '.'
            typedefs = typedefs + [typedef]

###
### Replacing argument structure constellations with 'arg1+', 'arg1-', and so
### on...
###
typedefs2 = []
for type in typedefs:
	type = type.replace('arg0-2-23-234-234-24-4','arg1-')
	type = type.replace('arg1-12-123-1234-124-14','arg1+')
	type = type.replace('arg12-123-1234-124-2-23-234-234-24','arg2+')
	type = type.replace('arg0-1-14-4','arg2-')
	type = type.replace('arg123-1234-23-234-234','arg3+')
	type = type.replace('arg0-1-12-124-14-2-24-4','arg3-')
	type = type.replace('arg1234-124-14-234-234-24-4','arg4+')
	type = type.replace('arg0-1-12-123-2-23','arg4-')
	typedefs2 = typedefs2 + [type]
typedefs = typedefs2
typedefs.sort()

xx = 0
for typedef in typedefs:
	n.write(typedef + '\n')
	xx = xx+1
	
n.close()

###
### Looping through all the irregular forms in 'id-irr' and writing irregular
### forms
###
k.close()

def irrcheck(form,regform,cats,inflcodes,checklist):
    x = 0
    old = set([])
    for infl in inflcodes:
        codes = infl[1]
        fullform = infl[0]
        if set(checklist) == set(codes) and not fullform in old:
            x = x+1
            old.add(fullform)
    if set(cats) == set(checklist) and not (regform == form and x == 1) and len(form.split()) == 1:
            return x
    else:
        return 0

y=0
z=0
irrlist = []
k=open('../../resources/nkl/id-irr','r')
irregs=k.readlines()
for irreg in irregs:
    irreg2 = irreg[:-1]
    irreg = str(irreg2)
    suffixarr = {}
    inflcodes = lexicon[irreg][1]
    stem = lexicon[irreg][0]
    icodecheck = inflcodes[:]
    # Looping through each form for every irregular item
    if not '_' in stem:
      for inflcode in inflcodes:
        fullform = inflcode[0]
        cats = inflcode[1]
        if lexicon[irreg][5]== 'v1':
            if irrcheck(fullform,stem+'r',cats,icodecheck,['vform=pres','pos=verb','status=nf']) > 0:
                irritem = fullform + ' PRES ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if irrcheck(fullform,stem+'s',cats,icodecheck,['vform=pres','spes=pass','pos=verb','status=nf']) > 0:
                irritem = fullform + ' S-PASSIVE-INF-PRES ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['vform=pret']).issubset(set(cats)):
                irritem = fullform + ' PRET-V1 ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['vform=part','pos=verb', 'status=nf']) == set(cats):
                irritem = fullform + ' PPART-V1 ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=posi','form=def','num=sg','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' PART-DEF-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=posi','num=pl','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' PART-INDEF-PL-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if irrcheck(fullform,stem+'nde',cats,icodecheck,['vform=prpart','pos=verb','status=nf']) > 0:
                irritem = fullform + ' PRES-PART ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['vform=imp','pos=verb','status=nf']) == set(cats):
                irritem = fullform + ' VERB-IMP ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
        elif lexicon[irreg][5]== 'm1':
            if set(['num=sg','form=def']).issubset(set(cats)):
                irritem = fullform + ' DEF-COMM-NOUN-M1-M2 ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['num=pl','form=ind']).issubset(set(cats)):
                irritem = fullform + ' INDEF-PL-M1-NOUN ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['num=pl','form=def']).issubset(set(cats)):
                irritem = fullform + ' DEF-PL-NOUN ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
        elif lexicon[irreg][5]== 'n2':
            if set(['num=sg','form=def']).issubset(set(cats)):
                irritem = fullform + ' DEF-SG-NOUN-NEUT ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['num=pl','form=ind']).issubset(set(cats)):
                irritem = fullform + ' INDEF-PL-N2-NOUN ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['num=pl','form=def']).issubset(set(cats)):
                irritem = fullform + ' DEF-PL-NOUN ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
        elif lexicon[irreg][5]== 'a1':
            if set(['grad=posi','num=pl','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' INDEF-PL-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=posi','form=def','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' DEF-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=posi','form=ind','num=sg','gend=n','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' SG-NEUT-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=komp','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' COMP-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=sup','form=ind','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' SUP-SAT-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
            if set(['grad=sup','form=def','pos=adj','status=nf']) == set(cats):
                irritem = fullform + ' SUP-UNSAT-ADJ ' + lexicon[irreg][0]
                irrlist = irrlist+[irritem]
        # elif lexicon[irreg][5]== 'no-infl':
        #     pass
        y=y+1


    for item in set(irrlist):
        items = item.split()
        item = items[0] + ' ' + items[1] + '_infl_rule ' + items[2]
        i.write(item + '\n')
        items = item.split(' ')
#        if items[1] == 'SUP-UNSAT-ADJ':
#            i.write(items[0] + ' SUP-ADJ-NUDE ' + items[2] + '\n')
        z = z+1
    irrlist=[]

try:
    k = open('../../resources/nkl/special-irr','r')
    newirr = k.readlines()
    i.write('\n;; Irregulars from \'special-irr\'\n')
    for irr in newirr:
        i.write(irr)
        z=z+1	
except:
    pass
i.write('"')
i.close()
k.close()

print('Printed ' + str(z) + ' irregular forms in \'irregs_nkl.tab\'')

###
### Writing exceptions
###
j=open('../../resources/nkl/exceptions.txt','w')
z=0
for exception in set(exceptions):
	j.write(exception + '\n')
	z=z+1
j.close()
h.close()
print('Printed ' + str(z) + ' exceptions in \'exceptions.txt\'')

for verb in vrbset:
    s.write(verb + '_v := vrb+.\n')
for prp in prpset:
    s.write(prp + '_prd := predsort.\n')
    s.write(prp + '_prp := '+prp+'_prd & prp+.\n')
    if not prp in smallex:
        g.write(prp+'_prp := prep-word &\n  [ STEM < "'+prp+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+prp+'_prp ].\n\n')
#    t.write(prp + '_prp_le := empty-prep-word &\n')
#    t.write('  [ STEM < "' +prp+ '" >,\n')
#    t.write('    SYNSEM.LKEYS.KEYREL.PRED ' +prp+ '_prp ].\n\n')
for prt in prtset:
    s.write(prt + '_prd := predsort.\n')
    s.write(prt + '_prt := '+prt+'_prd & prt+.\n')
    if not prt in smallex and not '+' in prt:
        g.write(prt+'_prt := part-word &\n  [ STEM < "'+prt+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+prt+'_prt ].\n\n')
#    t.write(prt + '_prt_le := empty-part-word &\n')
#    t.write('  [ STEM < "' +prt+ '" >,\n')
#    t.write('    SYNSEM.LKEYS.KEYREL.PRED ' +prt+ '_prt ].\n\n')
g.close()

norgramrels = set([])
norgramrelfile=open('../../resources/nkl/reltypes.tdl')
for line in norgramrelfile:
    predtype = line.split()[0]
    norgramrels.add(predtype)

for frametype in frametypes:
    predtype = frametype.split()[2]
    if not predtype in norgramrels:
        s.write(frametype)

u=open('../../resources/nkl/nkl-func.tdl','w')
funclist = []
for lex in funcset:
    funclist.append(lex)
    funclist.sort()
for lex in funclist:
    u.write(lex)
v=open('../../resources/nkl/nkl-funcrels.tdl','w')
funclist = []
for lex in funcrels:
    funclist.append(lex)
    funclist.sort()
for lex in funclist:
    v.write(lex)
w=open('../../resources/nkl/nkl-trigger.mtr','w')
triggerlist = []
for lex in triggerset:
    triggerlist.append(lex)
    triggerlist.sort()
for lex in triggerlist:
    w.write(lex)

###
### Remove files
###
import os
os.remove('../../resources/nkl/nkl_bm_u_fon.u8.txt')
os.remove('../../resources/nkl/id-irr')
