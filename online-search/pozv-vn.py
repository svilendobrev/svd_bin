#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
from pozvanete import optz, main
info_includes = 'ВАРНА'
text_excludes = '''
БОКСОНИЕРА
ДВУСТАЕН ДВУСТАЙНИ
ЕДНОСТАЕН
^ПОМЕЩЕНИЕ
ГАРСОНИЕРА ГАРСОНИЕРИ
ТРИСТАЕН
2-СТАЕН

^ПАРЦЕЛ
^ДВОР
^МЯСТО
^ГАРАЖ
^ПОДЗЕМЕН
^ОВОЩНА
ЗЕМЕДЕЛСКА ЗЕМЕДЕЛСКИ
НИВА
^ЛОЗЕ
^ПАРТЕРНО
ВИЛА

ФИРМА
ЗАВЕДЕНИЕ
СЛАДКАРНИЦА
^КАФЕ
МАГАЗИН
РАБОТЕЩ
ТУРИСТИЧЕСКА
цех
^МАСИВЕН
^МАСИВНА
ИНДУСТРИАЛЕН
ПРОМИШЛЕН
ПРОМИШЛЕНА
ОБОРУДВАН
ОФИС
^АТЕЛИЕ
хале
халета
СКЛАДОВЕ

www.karavellagreenhouse.com

с.
гр.

с.Каменар
Кранево

'''

if 1:
    main( info_includes=info_includes, text_excludes=text_excludes,)

# vim:ts=4:sw=4:expandtab
