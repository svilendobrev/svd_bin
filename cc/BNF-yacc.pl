%toks=(	 
 "TOK_NEG_INF"             ,"-inf"
,"TOK_INF"                 ,"[+]inf"
,"TOK_NOT"                 ,"!"	
,"TOK_MULT"                ,"*"	
,"TOK_MINUS"               ,"-"	
,"TOK_ADD"                 ,"+"	
,"TOK_EQUALS"              ,"="	
,"TOK_LESS"                ,"<"	
,"TOK_GREAT"               ,">"	
,"TOK_DIVIDE"              ,"/"	
,"TOK_LOGI_AND"            ,"&&"
,"TOK_LOGI_OR"             ,"||"
,"TOK_CONTRIBUTION"        ,"<+"
,"TOK_GREAT_EQU"           ,">="
,"TOK_LESS_EQU"            ,"<="
,"TOK_EQU_TO"              ,"=="
,"TOK_NOT_EQU"             ,"!="
,"TOK_OPEN_BRACK"          ,"("	
,"TOK_CLOSE_BRACK"         ,")"	
,"TOK_OPEN_SQUARE_BRACK"   ,"["	
,"TOK_CLOSE_SQUARE_BRACK"  ,"]"	
,"TOK_COMMA"               ,","	
,"TOK_SEMICOLON"           ,";"	
,"TOK_PERCENT"             ,"%"	
,"TOK_AT"                  ,"@"	
,"TOK_DOT"                 ,"."	
,"TOK_COLON"               ,":"	
,"TOK_QUESTION"            ,"?"	
,"TOK_CARET"               ,"^"	
,"TOK_OR"                  ,"|"	
,"TOK_AND"                 ,"&"	
,"TOK_TILDE"               ,"~"	
,"TOK_RIGHT_SHIFT"         ,">>"
,"TOK_LEFT_SHIFT"          ,"<<"
,"TOK_XNOR"                ,"^~"
#,"TOK_XNOR"                ,"~^"
,"TOK_HASH"                ,"#" 

,"TOK_INOUT", 		"inout"
,"TOK_INPUT", 		"in"
,"TOK_OUTPUT", 		"out"
,"TOK_INTEGER", 	"integer"
,"TOK_REAL",		"real"
,"TOK_BRANCH",		"branch"
,"TOK_PARAMETER",	"parameter"
,"TOK_EXCLUDE",		"exclude"
,"TOK_FROM",		"from"
,"TOK_ENDMODULE",	"endmodule"
,"TOK_DISCIPLINE",	"discipline"
,"TOK_ENDDISCIPLINE",	"enddiscipline"

,"TOK_NATURE",		"nature"
,"TOK_ENDNATURE",	"endnature"
,"TOK_MODULE",		"module"
,"TOK_GENVAR",		"genvar"
#,"TOK_DEFPARAM",	"defparam"
,"TOK_FLOW",		"flow"
,"TOK_POTENTIAL",	"potential"
,"TOK_ANALOG",	"analog"
,"",	""
,"",	""
,"",	""
,"",	""
);

while (<>) {
	$yy += /^%%/; last if $yy>=2; next if !$yy || /^%%/;;

#	print  1+/^[a-zA-Z_]*[ \t]+:/;
#	     print  1+!/^[ \t]+\|/;
#	next if !/^[a-zA-Z_]*[ \t]+:/ && !/^[ \t]+\|/;
	$off++ if /[^']\{[^']/ || /^\{/;
	if (/[^']\}[^']/ || /^\}/) { $off--; next; }
	next if $off;
	s/^[ \t]+/ /;
	next if /^ *;/;
	next if /^[ \t\n]*$/;
if ($TRANSLATE) {
	foreach $k (keys %toks) {
	 $v=$toks{$k};
	 s/$k(?=\W)/$v/g;  #lookahead for nonwordchar
	}
}
	s/^(\w+)[ \t]*:/\n$1 ::=\n/;
	print if !/ *\| *error/i;

#last if $i++>15;
}
