import sys

n_min = int(sys.argv[1])
n_max = int(sys.argv[2])

for i in range( n_min, n_max+1):
    fn = 'IMG_%04d' % i
    for tfn in ( fn+'.JPG', 'thumb_'+fn+'.jpg'):
        try:
            f = file( tfn )
        except IOError:
            print 'missing', tfn
        else: f.close()

