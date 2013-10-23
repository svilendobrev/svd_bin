_afun() {
	#echo azzz $COMP_CWORD $COMP_KEY $COMP_WORDS $COMP_WORDBREAKS $COMP_TYPE $COMP_POINT $COMP_LINE
	export COMP_CWORD COMP_KEY COMP_WORDS COMP_WORDBREAKS COMP_TYPE COMP_POINT COMP_LINE
    COMPREPLY=( `py co.py` )
	#echo zzz$COMPREPLY
	return 0
}
complete -F _afun echo

#echo '
#import os,re
#print( "\n".join( a+"="+repr(os.environ.get(a,"")) 
#	for a in "COMP_CWORD COMP_KEY COMP_WORDS COMP_WORDBREAKS COMP_TYPE COMP_POINT COMP_LINE".split() ))
#print( re.split( os.environ["COMP_WORDBREAKS"].replace( "(", r"\("), os.environ["COMP_LINE"] ))
#' >co.py
