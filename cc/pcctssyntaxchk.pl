#!/usr/bin/perl
## sd '2k check pccts produced grammar for syntaxerror failactions
$NAME = shift;
print "--$NAME--\n";
$NAME = "^\s*$NAME"."::";
#print "--$NAME--\n";

while (<>) {
  if (/$NAME/) {
	print "\tnone: $a" if $b ne $a; 	#no matches found there
	$a=$_;
   } 
#  print $a if /$NAME/; 
  if (/FAIL|zz(set)*match\(/ && $b ne $a) { 	#do we need the FAIL ???
	$b=$a; print $a; }			#print once
}

	print "\tnone: $a" if $b ne $a; 	#no matches found there
