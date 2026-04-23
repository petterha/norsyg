# Script for creating a big lexicon for Norsyg. The resouces needed are not
# distributed with Norsyg, but the resulting tdl lexicon files are.
# See 'norsyg/nkl.tdl' and 'norsyg/preds.tdl'


# Create a big lexicon based on NorKompLeks
python nkl2tdl.py
# Add information from NorGram
python norgramlex.py
# Make a lexicon with verbs that are in use (from NorGramBank)
python freqverbs.py
# Cleanup
python cleanup.py
# Add wordnet onotology
python wordnet.py
# Change file names
mv ../preds-small-wn.tdl ../preds-small.tdl
mv ../preds-mid-wn.tdl ../preds.tdl
mv ../nkl-mid.tdl ../nkl.tdl
mv ../trigger-mid.mtr ../trigger.mtr
