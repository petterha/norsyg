#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re

# Define the replacement pattern
replacement_pattern = r'om_func := func-word &\s*\[\s*STEM\s*<\s*"om"\s*>,\s*SYNSEM\.LKEYS\.KEYREL\.PRED\s*om_prd\s*\]\.'

# Define the replacement strings
replacement_strings = [
    'om_prp := prep-word & [ STEM < "om" >, SYNSEM.LKEYS.KEYREL.PRED om_prp ].',
    'om_prt := part-word & [ STEM < "om" >, SYNSEM.LKEYS.KEYREL.PRED om_prt ].'
]

# Function to replace the pattern
def replace_pattern(match):
    return replacement_strings.pop(0)

# Read the input file
input_filename = '../lexicon.tdl'
with open(input_filename, 'r') as file:
    file_contents = file.read()

# Perform the replacements
new_contents = re.sub(replacement_pattern, replace_pattern, file_contents, flags=re.MULTILINE)

# Write the modified content back to the file
output_filename = 'output_file.txt'
with open(output_filename, 'w') as file:
    file.write(new_contents)

#print(f"Replacements completed. Output saved to {output_filename}")

