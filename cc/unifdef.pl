#!/usr/bin/perl
die "$0 [-]condition file[s]\n default gives ifndef ;\n with '-' gives ifdef\n" if ($ARGV[0] eq '--') ;

#filter things that are ifdef(=1) or ifndef(=0)
$ifdef = ($ARGV[0] =~ s/^-//);
$COND = shift;
print STDERR "if".($ifdef?"":"n")."def\n";

$inside =0; #0:plain; 1: #ifdef / #else of ifndef; 2: #ifndef / #else of #ifdef
$level  =0;

while(<>) {
   if (/^\s*#\s*ifdef/) {
      $ifs++;
      if (/^\s*#\s*ifdef\s*$COND/)  {
         die "nested ifdef SAME's not supported" if $inside;
         $inside=1; $level = $ifs; }
      next;
   }
   if (/^\s*#\s*ifndef\s*$COND/) {
      $ifs++;
      if (/^\s*#\s*ifndef\s*$COND/) {
         die "nested ifdef SAME's not supported" if $inside;
         $inside=2; $level = $ifs; }
      next;
   }
   if (/^\s*#\s*else/) {
     $inside = 3-$inside if $inside && $level == $ifs;
     next;
   }
   if (/^\s*#\s*endif/) {
     $inside=0 if $level == $ifs;
     --$ifs;
     next;
   }

   print if !$inside || $ifdef == $inside-1;
}
