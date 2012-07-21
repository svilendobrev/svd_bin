if x%1==x ( qt ^ echo %@SUBSTR[%_DATE,1,1]%@SUBSTR[%_DATE,3,2] ^ quit)
if isdir %1 (echo %1 already there ^ dir %1 ^ quit)
nd %1
call \bin\bin\wget.btm -F -i..\getrent.htm
..\newclasf.pl br* >all
up
ffndhous.pl %1\all > %1\z
