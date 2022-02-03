import sys
x = float( sys.argv[1])

dod = 0.10
osig_rabotnik = 413.4
def osig_rabotodatel( bruto):
    return min( 3000, bruto ) * (10.92+0.4+2.8+4.8) / 100.0 #567.6

def neto( bruto):
    return ( bruto - osig_rabotnik ) * (1-dod)
def bruto( neto):
    return neto / (1-dod) + osig_rabotnik

def razhod( bruto):
    return bruto + osig_rabotodatel( bruto)

bx = bruto(x)
rbx = razhod(bx)
nx = neto(x)
rnx = razhod(x)
print( f'neto : {x} -> bruto= {bx:.2f}, razhod: {rbx:.2f}')
print( f'bruto: {x} -> neto = {nx:.2f}, razhod: {rnx:.2f}')

'''
брутно възнаграждение = БрВ >=3000
Осиг работник в/у 3000 = 3000*(8,38+2,2+3,2)/100 = 413,4
ДОД = (БрВ-413,4)*10%
Запл. за получаване = БрВ - 413,4 - ДОД = 0,9*(БрВ - 413,4)

За работодателя = БрВ+567,6
Осиг работодател = 3000*(10.92+0.4+2.8+4.8)/100 = 567.6
'''

