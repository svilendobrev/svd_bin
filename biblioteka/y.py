# -*- coding: utf-8 -*-

import yaml
import yaml_align, yaml_anydict
from yaml.constructor import Constructor

if 'default-list-is-tuple':  #so is hashable
    yaml_anydict.load_list_as_tuple()
    yaml_anydict.dump_tuple_as_list()
    #yaml.add_constructor( 'tag:yaml.org,2002:seq', Constructor.construct_python_tuple)

if 'default-mapping-is-ordered':
    from collections import OrderedDict as dictOrder
    class Loader( yaml_anydict.Loader_map_as_anydict, yaml.Loader):
        anydict = dictOrder
    Loader.load_map_as_anydict()
    yaml_anydict.dump_anydict_as_map( dictOrder)


yaml.add_constructor(   #force list->tuple
        ':somet:shape',
                Constructor.construct_python_tuple)

yaml.add_constructor(   #force list->tuple
        '!shape',
                Constructor.construct_python_tuple)

qa='''
-
  name\:it: Mark McGwire
  hr:   65
  avg:  0.278
-
  name: Sammy Sosa
  hr:   63
  avg:  0.28
'''

a='''
- [name        , hr, avg  ]
- [Mark McGwire, 65, 0.278]
- [Sammy Sosa  , 63, 0.288]
'''

a='''
# Ranking of 1998 home runs
---
- Mark McGwire
- Sammy Sosa
- Ken Griffey

# Team ranking
---
- Chicago Cubs
- St Louis Cardinals
'''

a='''
---
time: 20:03:20
player: Sammy Sosa
action: strike (miss)
...
---
time: 20:03:47
player: Sammy Sosa
action: grand slam
...
'''

a='''
hr: # 1998 hr ranking
  - Mark McGwire
  - Sammy Sosa
rbi:
  # 1998 rbi ranking
  - Sammy Sosa
  - Ken Griffey
'''

a='''
hr:
  - Mark McGwire
  # Following node labeled SS
  - &SS Sammy Sosa
rbi:
  - *SS # Subsequent occurrence
  - Ken Griffey
'''


a='''
? - Detroit Tigers
  - Chicago cubs
:
  - 2001-07-23

? [ New York Yankees,
    Atlanta Braves ]
: [ 2001-07-02, 2001-08-12,
    2001-08-14 ]
'''
za='''
# products purchased
- item    : Super Hoop
  quantity: 1
- item    : Basketball
  quantity: 4
- item    : Big Shoes
  quantity: 1
'''

a='''
name: Mark McGwire
accomplishment: >
  Mark set a major league
  home run record in 1998.
stats: |
  65 Home Runs
  0.278 Batting Average
'''
a='''
>
 Sammy Sosa completed another
 fine season with great stats.

   63 Home Runs
   0.288 Batting Average

 What a year!
 an more
'''

xa='''
#%TAG ! somet:
--- !shape
  # Use the ! handle for presenting
  # tag:clarkevans.com,2002:circle
- !circle
  center: &ORIGIN {x: 73, y: 129}
  radius: 7
- !line
  start: *ORIGIN
  finish: { x: 89, y: 102 }
- !label
  start: *ORIGIN
  color: 0xFFEEBB
  text: Pretty vector drawing.
'''
a='''
име: Разни - стихове, откъси, интервюта

свойства: [ без-номер , възрастни ]
издание: радио
качество-съдържание/запис: +/~
описание2:
 85 години от рождението на ЛедаТасева:
 - откъс от интервю с нея през 1984г с размисли за театъра и литературата
 - Леда Тасева изпълнява стихотворенията “Самотният човек” и “Вечерен тромпет” от БорисХристов и говори за посланията на поезията му
 - Павел Павлов, Иван Теофилов и Илка Зафирова за ЛедаТасева
 - Откъс от драматичната миниатюра по Бърнард Шоу “Мургавата лейди на сонетите”, с ЛедаТасева (Кралицата) и НаумШопов (Шекспир)
 - Откъс от драматичната миниатюра “Човекът, който дойде от Америка” по разказ на Светослав Минков (1970г)
 За изтъкнатия писател и драматург Станислав Стратиев:
 - откъс в предаването „Разговор с вас”
 - интервю – за абсурда на българския живот, за празнословието, за илюзиите;
 - изказване пред конференция на СБП през 1979г за възпитанието на творческо мислене, за нивелирането на личността;
 - откъс от „Римска баня”, поставена в Сатиричния театър през 1974г;
 - откъс от „Упражнение по другост – Българският модел 2”, постановка на Борислав Чакринов в Малък градски театър зад канала, 90-те.
откога: 110911
произход: [ svd , zoy ]
преводи:
 muzika--v.petrov--radio               :
    име: Музика (стихотворение)
    автор: ВалериПетров
 zlaten.fond-apostol.karamitev--radio  :  Златният фонд - Апостол Карамитев
 zlaten.fond-leda.taseva--radio        :
    име: Златният фонд - Леда Тасева
    описание2:
     - 85 години от рождението на ЛедаТасева
     - откъс от интервю с нея през 1984г с размисли за театъра и литературата
     - Леда Тасева изпълнява стихотворенията “Самотният човек” и “Вечерен тромпет” от БорисХристов и говори за посланията на поезията му
     - Павел Павлов, Иван Теофилов и Илка Зафирова за ЛедаТасева
     - Откъс от драматичната миниатюра по Бърнард Шоу “Мургавата лейди на сонетите”, с ЛедаТасева (Кралицата) и НаумШопов (Шекспир)
     - Откъс от драматичната миниатюра “Човекът, който дойде от Америка” по разказ на Светослав Минков (1970г)
 zlaten.fond-stanislav.stratiev--radio :
    име: Златният фонд - Станислав Стратиев
    описание2:
     - За изтъкнатия писател и драматург Станислав Стратиев
     - откъс в предаването „Разговор с вас”
     - интервю – за абсурда на българския живот, за празнословието, за илюзиите;
     - изказване пред конференция на СБП през 1979г за възпитанието на творческо мислене, за нивелирането на личността;
     - откъс от „Римска баня”, поставена в Сатиричния театър през 1974г;
     - откъс от „Упражнение по другост – Българският модел 2”, постановка на Борислав Чакринов в Малък градски театър зад канала, 90-те.
 pritcha.za.dyzhda--radio              :  Притча за дъжда :китайска
'''
p = yaml.load( a, Loader= Loader)

#p={ 'уио': 'уът'}
import pprint
pprint.pprint( p)

# vim:ts=4:sw=4:expandtab
