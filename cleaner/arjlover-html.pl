#chall.pl 's/<tr.*?(<a href)/\1/g + s,<td>\d+</td>,,g + s,</td>,,g + s,<td><a.*?</a>,,g' "$@"
chall.pl 's,<tr.*?(<a href.*?</a>).*?<td.*?>([.\d]+).*?<td.*?<td.*?>([\d-:]+).*,\1 \2 <t>\3,g' "$@"
chall.pl 's,^[\s\S]+?(Название),, + s/<tr class=head[\s\S]+$// + s/Copyright[\s\S]+$//' "$@"
chall.pl 's/(<t[rhd])[^>]+>/\1>/g + s,</t[rhd]>,,g' "$@"
