def Rkabel( l_m,S_mm2,ro= 0.017): return ro*(l_m/float(S_mm2))

if __name__ == '__main__':
    import sys
    print( Rkabel( *(float(x) for x in sys.argv[1:])))

# vim:ts=4:sw=4:expandtab
