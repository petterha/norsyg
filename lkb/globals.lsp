;;; LinGO grammar specific globals file
;;; parameters only - grammar specific functions 
;;; should go in user-fns.lsp


(defparameter *active-parsing-p* t)

;;; Strings

(defparameter *toptype* '*top*)

(defparameter *string-type* 'string
   "a special type name - any lisp strings are subtypes of it")

;;; Lexical files

(defparameter *orth-path* '(stem))

(defparameter *list-tail* '(rest))

(defparameter *list-head* '(first))

(defparameter *empty-list-type* 'null)

(defparameter *list-type* 'list)

(defparameter *diff-list-type* 'diff-list)

(defparameter *diff-list-list* 'list)

(defparameter *diff-list-last* 'last)

(defparameter *lex-rule-suffix* "_INFL_RULE"
 "creates the inflectional rule name from the information
  in irregs.tab - for PAGE compatability")

(defparameter *irregular-forms-only-p* t)

;;;
;;; input characters to be ignored (i.e. suppressed) in tokenization
;;;
(defparameter *punctuation-characters*
  (append
   '(#\space #\! #\" #\& #\' #\(
     #\) #\* #\+ #\, #\- #\. #\/ #\;
     #\< #\= #\> #\? #\@ #\[ #\\ #\] #\^
     #\_ #\` #\{ #\| #\} #\~)
   #+:ics
   '(#\ideographic_full_stop #\fullwidth_question_mark 
     #\horizontal_ellipsis #\fullwidth_full_stop
     #\fullwidth_exclamation_mark #\black_circle
     #\fullwidth_comma #\ideographic_space
     #\katakana_middle_dot #\white_circle)))

(defparameter *display-type-hierarchy-on-load* nil)

;;; Parsing

(defparameter *chart-limit* 100)

(defparameter *maximum-number-of-edges* 400)

(defparameter *mother-feature* NIL
  "The feature giving the mother in a grammar rule")

(defparameter *start-symbol* '(root root_np root_advp_pp)
  "specifing valid parses")

(defparameter *maximal-lex-rule-applications* 5
   "The number of lexical rule applications which may be made
   before it is assumed that some rules are applying circularly")

(defparameter *maximal-morphological-rule-depth* 3)
(setf *maximal-morphological-rule-depth* 3)

(defparameter *deleted-daughter-features* 
  '(ARGS HD-DTR NH-DTR DTR)
  "features pointing to daughters deleted on building a constituent")

;;;
;;; to enable local ambiguity packing
;;;

#+:null
(defparameter *chart-packing-p* t)

(defparameter *packing-restrictor*
  ;'(STEM RELS HCONS RNAME PUNCT)
  '(STEM RELS PUNCT)
  "restrictor used when parsing with ambiguity packing")

;;; Parse tree node labels

;;; the path where the name string is stored
(defparameter *label-path* '(LABEL-NAME))

;;; the path for the meta prefix symbol
(defparameter *prefix-path* '(META-PREFIX))

;;; the path for the meta suffix symbol
(defparameter *suffix-path* '(META-SUFFIX))

;;; the path for the recursive category
(defparameter *recursive-path* '(SYNSEM NON-LOCAL SLASH FIRST))

;;; the path inside the node to be unified with the recursive node
(defparameter *local-path* '(SYNSEM LOCAL))

;;; the path inside the node to be unified with the label node
(defparameter *label-fs-path* '())

(defparameter *label-template-type* 'label)

;;; for the compare function 
(defparameter *duplicate-lex-ids* 
    '(openbracket closebracket colon hyphen
      ))
(defparameter *discriminant-path* '(synsem local keys key pred))
(setf *gen-ignore-rules*
  '(exclam-mark-punct quest-mark-punct period-punct
   ))

;(defparameter *last-parses* '("jon smiler"))

#+:smaf
(progn
  ;; enable clobbering
  (setf smaf::*clobber-p* nil)
  ;; ... and log clobbered edges
  ;(setf smaf::*warning-clobber* t)
  ;; warn on all unanalysed tokens
  (setf *generate-messages-for-all-unanalysed-tokens* t)
  ;; abort parse if no spanning path
  (setf *abort-parse-if-no-spanning-morph-edge-path* t)
  
  ;; unknown word fallback
;  (setf *fallback-pos-p* t)
;  (setf smaf::*unknown-word-type* 'uk-noun-phrase)
  ;(setf smaf::*unknown-word-type* nil)
  
  ;; insert surface form of ersatzes at end of this path
  (defparameter smaf::*ersatz-carg-path* '(SYNSEM LKEYS KEYREL CARG))
  
  )

(setf *translate-grid* '(:no :no))


;;;
;;; as we move into the chart mapping universe, lexical entries behave similar
;;; to rules: the list of input tokens that license a lexical entry are unified
;;; into *lexicon-tokens-path* (when set).  furthermore, to give the grammarian
;;; easier access to the token in the right periphery, the last element of the 
;;; tokens list is made re-entrant with *lexicon-last-token-path*.
;;;
(setf *lexicon-tokens-path* '(TOKENS +LIST))
(setf *lexicon-last-token-path* '(TOKENS +LAST))
(setf *token-id-path* '(+ID))
