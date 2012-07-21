#!/usr/bin/perl
##time to/from number

(@mon) = ( "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" );
$now =0;

if ($#ARGV>=0) {
  if ($ARGV[0] =~ /^\d+$/ || $ARGV[0] =~ /^0x[\da-f]+/i ) {
      $now = $ARGV[0]; shift;
  } else {
  if ($ARGV[0] =~ s,(\d+)[/\.](\d+|[a-z]+)[/\.](\d+)[ :/](\d+)[:\.](\d+)[:\.](\d+),$1/$2/$3:$4:$5:$6,
  ) { (@tm) = ($6,$5,$4, $1,$2,$3 );
      $tm[5] = $3>=1000 ? $3 : 2000+$3;
      if ($tm[4] =~ /[a-z]+/i) {
        for ($m=0; $m<=$#mon; $m++) {
           if ($tm[4] =~ /$mon[$m]/i) { $tm[4] = $m+1; last; }
        }
      }
      print "$now= $tm[2]:$tm[1]:$tm[0] $tm[3].$tm[4].$tm[5]\n";
      print 'mktime or strftime into $now?'
    }
  }
}

if ($now>0) {
   (@tm) = gmtime( $now); $tm[4]++; $tm[5]+=1900;
   print "$now= $tm[2]:$tm[1]:$tm[0] $tm[3].$tm[4].$tm[5]\n";
}

$now = time();
(@tm) = gmtime( $now); $tm[4]++; $tm[5]+=1900;
print "now: $now= $tm[2]:$tm[1]:$tm[0] $tm[3].$tm[4].$tm[5]\n";
