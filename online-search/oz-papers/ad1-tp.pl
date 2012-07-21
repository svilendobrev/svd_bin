while (<>) {
        if ($a ne $ARGV) { $a= $ARGV; print "<br><br>---------<br>$a\n"; }
        if (/#e6e6e6/i) { $on++; next; }
        next if !$on;
        $on = 0 if m,</table>,i;
        print;
}
