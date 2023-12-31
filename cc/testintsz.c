#include <stdint.h>
#include <stdio.h>
#define DECL(t)  { t x; printf( #t "=%d\n", sizeof x); }
int main() {
    DECL( int8_t )
    DECL( int16_t )
    DECL( int32_t )
    DECL( int64_t )
    DECL( char)
    DECL( short)
    DECL( int )
    DECL( long)
    DECL( long long)
    printf( "wordsz %d\n", __WORDSIZE);
    return 0;
}
