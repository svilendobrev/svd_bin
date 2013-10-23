/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: ansiterm.cpp,v 1.3 2003/01/21 19:56:35 cade Exp $
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ansiterm.h"

  int Ansi_MAXX = 80;
  int Ansi_MAXY = 25;
  int Ansi_X    =  1;
  int Ansi_Y    =  1;

  int a_fg;
  int a_bg;
  int a_ta;

  int ansi_o_ta;

  int ANSI = 0;

  static int colortab( int color ) // convert normal colors to ANSI ones
  {
    switch(color)
      {
      case cBLACK   : return 0;
      case cBLUE    : return 4;
      case cGREEN   : return 2;
      case cCYAN    : return 6;
      case cRED     : return 1;
      case cMAGENTA : return 5;
      case cYELLOW  : return 3;
      case cWHITE   : return 7;
      }
    return 7;
  }

  int AnsiInit( int pANSI )
  {
    if ( pANSI != -1)
      ANSI = pANSI;
    else
      {
      ANSI = 0;
      char *buf = getenv( "TERM" );
      if ( buf && strcasecmp( buf, "ANSI"  ) == 0 ) ANSI = 1;
      if ( buf && strcasecmp( buf, "vt100" ) == 0 ) ANSI = 1;
      }
    if (getenv( "TERMX" )) Ansi_MAXX = atoi( getenv( "TERMX" ) );
    if (getenv( "TERMY" )) Ansi_MAXY = atoi( getenv( "TERMY" ) );
    if ( Ansi_MAXX == 0 ) Ansi_MAXX = 80;
    if ( Ansi_MAXY == 0 ) Ansi_MAXY = 25;
    Ansi_X = 1;
    Ansi_Y = 1;
    AnsiTA( cNORMAL );

    return 0;
  };

  void AnsiDone()
  {
    if (!ANSI) return;
    AnsiTA( cNORMAL );
  };


  void AnsiSuspend() // suspends console (before system() for example)
  {
    if (!ANSI) return;
    ansi_o_ta = a_ta;
    AnsiTA( cNORMAL );
  }

  void AnsiRestore() // restores console after suspend
  {
    if (!ANSI) return;
    AnsiTA( ansi_o_ta );
  }

  void AnsiCE( int attr ) // clear to end-of-line
  {
    if (!ANSI) return;
    if ( attr != -1 )
      {
      int save_ta = a_ta;
      AnsiTA( attr );
      printf( "\033[K" );
      AnsiTA( save_ta );
      }
    else
      {
      printf( "\033[K" );
      }
  };

  void AnsiCS( int attr ) // clear screen
  {
    if (!ANSI) return;
    if ( attr != -1 )
      {
      int save_ta = a_ta;
      AnsiTA( attr );
      printf( "\033[2J" );
      AnsiTA( save_ta );
      }
    else
      {
      printf( "\033[2J" );
      }
  };


  void AnsiOut( int x, int y, const char *s )
  {
    AnsiXY( x, y );
    AnsiPuts( s );
  };

  void AnsiOut( int x, int y, const char *s, int attr )
  {
    AnsiXY( x, y );
    AnsiPuts( s, attr );
  };

  void AnsiPuts( const char *s )
  {
    printf( s );
  };

  void AnsiPuts( const char *s, int attr )
  {
    int _ta = a_ta;
    AnsiTA( attr );
    printf( s );
    AnsiTA( _ta  );
  };

  void AnsiCHide() { return; } // cursor hide
  void AnsiCShow() { return; } // cursor show

  int AnsiMaxX() { return Ansi_MAXX; }
  int AnsiMaxY() { return Ansi_MAXY; }
  int AnsiX() { return -1; }
  int AnsiY() { return -1; }

  void AnsiFG( int color )
  {
    AnsiTA( CONCOLOR(color, a_bg) );
  }

  void AnsiBG( int color )
  {
    AnsiTA( CONCOLOR( a_fg, color ) );
  }

  void AnsiTA( int attr )
  {
    if (!ANSI) return;
    a_ta = attr;
    a_fg = COLORFG( a_ta );
    a_bg = COLORBG( a_ta );

    int _l = (a_bg>7)?5:0;    // blink
    int _h = (a_fg>7)?1:0;    // hi
    int _f = a_fg;
    int _b = a_bg;
    if ( _f > 7 ) _f -= 8;
    if ( _b > 7 ) _b -= 8;
    _f = colortab(_f)+30;  // fore
    _b = colortab(_b)+40;  // back

    // hi,blink,fg,bg
    printf( "\033[0;%s%s%d;%dm", _h?"1;":"", _l?"5;":"", _f, _b );
  }

  void AnsiXY( int x, int y ) // go to x,y
  {
    if (!ANSI) return;
    if ( x < 1 || y < 1 || x > Ansi_MAXX || y > Ansi_MAXY ) return;
    printf( "\033[%d;%dH", y, x );
  }

  int AnsiKbHit() { return 1; }
  int AnsiGetch() { return fgetc(stdin); }
  void AnsiBeep()  { printf( "\007" ); }


#ifdef TEST3
int main()
{
  AnsiInit();
  AnsiCS();

  AnsiOut( 1, 1, "<-" );
  AnsiXY( 10, 10 );
  AnsiTA( 79 );
  AnsiPuts( "  ANSI terminal Test  " );
  AnsiXY( 1, 11 );
  int z;
  for ( z = 0; z < 256; z++ )
    {
    char tmp[16];
    sprintf( tmp, " %3d ", z );
    AnsiTA(z); AnsiPuts( tmp );
    }
  AnsiTA( cNORMAL );

  for ( z = 1; z <= AnsiMaxX(); z++ )
    AnsiOut( z, 1, "*", z );
  for ( z = 1; z <= AnsiMaxX(); z++ )
    AnsiOut( z, AnsiMaxY()-1, "*", z );
  int c = AnsiGetch();
  if (c) c = c; // :) test


  AnsiDone();
}
#endif

 // eof ansiterm.cpp
