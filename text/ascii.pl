#!/usr/bin/perl
$A1 = shift; $A1 = 32 if $A1 eq '';
$A2 = shift; $A2 =256 if $A2 eq '';

for ($i=$A1; $i<$A2; $i++) { 
	printf "%c", $i; 
	print "\n" if $i%16==15;
}
