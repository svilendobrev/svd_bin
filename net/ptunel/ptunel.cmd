#https://github.com/izderadicka/ptunnel.git 

set PTPY=apath\ptunnel\src\ptunnel.py
set PRXY=proxy.it:2345
set SRVIMAP=some.com
set SRVSMTP=some.com
\Python27\python.exe %PTPY%  -d -p %PRXY% 9993:%SRVIMAP%:993 5587:%SRVSMTP%:465

