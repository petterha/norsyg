import re

prepset = set([])
preps = open('preps.txt','r')
for line in preps:
    prep = line.split('_')[1]
    prepset.add(prep)

prtset = set([])
prts = open('prts.txt','r')
for line in prts:
    line = line.split(':')[1]
    prt = line.split('_')[0]
    prtset.add(prt)

cmpzset = set([])
cmpzs = open('cmpzs.txt','r')
for line in cmpzs:
    cmpz = line.split('_')[1]
    cmpzset.add(cmpz)

modset = set([])
mods = open('mods.txt','r')
for line in mods:
    mod = line.split('_')[1]
    modset.add(mod)

advset = set([])
advs = open('advs.txt','r')
for line in advs:
    adv = line.split('_')[1]
    advset.add(adv)

sadvset = set([])
sadvs = open('sadvs.txt','r')
for line in sadvs:
    sadv = line.split('_')[1]
    sadvset.add(sadv)

degadvset = set([])
degadvs = open('deg-advs.txt','r')
for line in degadvs:
    degadv = line.split('_')[1]
    degadvset.add(degadv)


with open('../lexicon-copy.tdl', 'r') as file:
    new_contents = file.read()

allcontents = ''
# Read the input file
input_file = open('../lexicon-copy.tdl','r')
for line in input_file:
    new_line = line
    if '_func :=' in line or '_deg' in line:
        items = line.split('_')
        func = items[0]
        mwe = func
        head = func
        pred = func
        newhead = func
        if '*' in func:
            mwe = mwe.replace('*','","')
            newhead = head.replace('*','-')
            pred = func
        if '-' in func:
            mwe = mwe.replace('-','","')
            pred = func.replace('-','*')
            newhead = func
        # Define the replacement pattern
        if '_func' in line:
#            replacement_pattern = r''+head+'_func := func-word &\s*\[\s*STEM\s*<\s*"'+mwe+'"\s*>,\s*SYNSEM\.LKEYS\.KEYREL\.PRED\s*'+pred+'_prd\s*\]\.'
            replacement_pattern = head+'_func := func-word &  [ STEM < "'+mwe+'" >,    SYNSEM.LKEYS.KEYREL.PRED '+pred+'_prd ].'
        elif '_deg' in line:
#            replacement_pattern = r''+head+'_deg := func-word &\s*\[\s*STEM\s*<\s*"'+mwe+'"\s*>,\s*SYNSEM\.LKEYS\.KEYREL\.PRED\s*'+pred+'_prd\s*\]\.'
            replacement_pattern = head+'_deg := func-word &  [ STEM < "'+mwe+'" >,    SYNSEM.LKEYS.KEYREL.PRED '+pred+'_prd ].'
        replacement_string = ''
        if pred in prepset:
            replacement_string = replacement_string +newhead+'_prp := prep-word &\n  [ STEM < "'+mwe+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+pred+'_prp ].\n\n'
        if pred in prtset:
            if '_prt' in new_line:
                new_line = new_line.replace('_prt','_prd')
            replacement_string = replacement_string +newhead+'_prt := part-word &\n  [ STEM < "'+mwe+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+pred+'_prt ].\n\n'
        if pred in advset:
            replacement_string = replacement_string +newhead+'_adv := adv-word &\n  [ STEM < "'+mwe+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+pred+'_adv_rel ].\n\n'
        if pred in sadvset:
            replacement_string = replacement_string +newhead+'_sadv := sadv-word &\n  [ STEM < "'+mwe+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+pred+'_sadv_rel ].\n\n'
        if pred in cmpzset:
            replacement_string = replacement_string +newhead+'_cadv := cadv-word &\n  [ STEM < "'+mwe+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED _'+pred+'_x_rel ].\n\n'
        if pred in degadvset:
            replacement_string = replacement_string +newhead+'_degadv := degadv-word &\n  [ STEM < "'+mwe+'" >,\n    SYNSEM.LKEYS.KEYREL.PRED '+pred+'_prd ].\n\n'
        new_line = new_line.replace(replacement_pattern,replacement_string[:-1])
        #new_contents = re.sub(replacement_pattern, replacement_string, new_contents, flags=re.MULTILINE)

    # Write the modified content back to the file
    if ' &  [' in new_line:
        new_line = new_line.replace(' &  [',' &\n  [')
    if ',    ' in new_line:
        new_line = new_line.replace(',    ',',\n    ')
    allcontents = allcontents+new_line
output_filename = 'output_file.txt'
with open(output_filename, 'w') as file:
    file.write(allcontents)

        
#print(f"Replacements completed. Output saved to {output_filename}")
