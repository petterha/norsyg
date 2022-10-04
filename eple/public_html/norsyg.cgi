#!/bin/bash

# Script for parsing sentences and getting analyses as javascript trees
# and tables.
# The results are displayed in result.html
#
# $ sh parse.sh "Mannen beundrer skogen."
#

export LANG=nb_NO.UTF-8

#Sending the headers
cat <<EOF
Content-Type: text/html; charset=UTF-8

EOF

#echo "Content-Type: text/html; charset=UTF-8"
#echo

INPUT=$(mktemp -p ~/tmp)
ACETREES=$(mktemp -p ~/tmp)
ACEOUT=$(mktemp -p ~/tmp)

# Write some initial html code
cat ~/consttree/head.html

# Write input string into $INPUT
INPUTRAW=$(grep "string=" | cut -f2 -d"=")

[ -n "$INPUTRAW" ] && {
  php -r '$res=urldecode("'$INPUTRAW'");echo($res);' > $INPUT

  # Parse the input string and write the result into $ACEOUT
  ~/consttree/ace -g ~/consttree/norwegian-mid.dat -n 5 --maxent=norgram1000.mem < $INPUT > $ACEOUT

  # Write the trees into $ACETREES
  cut -d ";" -f 2 $ACEOUT | grep '(' > $ACETREES

  # Write some initial html code
  cat <<-EOF
	  <table border="0">
            <tr>
              Rangering av (inntil 5) analyser
            </tr>
	    <tr>
	      <th>Treanalyser</th> <th>Feltanalyser</th>
	    </tr>
	EOF

  NUM=1
  while read -r line
  do
    ACETREE=$(mktemp -p ~/tmp)
    AVM=$(mktemp -p ~/tmp)
    echo $line > $ACETREE
    ~/consttree/recons-0.1.9-x86-64-for-ace-0.9.26 -g ~/consttree/norwegian-mid.dat -tff < $ACETREE > $AVM
    ~/consttree/recons-0.1.9-x86-64-for-ace-0.9.26 -g ~/consttree/norwegian-mid.dat -tff < $ACETREE > ~/test.avm
    # Kommet hit
    python ~/consttree/incr2const.py $AVM $NUM
    NUM=$(($NUM+1))
    rm -f $ACETREE
    rm -f $AVM
  done < $ACETREES


  # Add some final HTML code
  echo "  </table>"
  rm -f $INPUT
  rm -f $ACETREES
  rm -f $ACEOUT
}

echo "</html>"


exit 0
#firefox result.html &
