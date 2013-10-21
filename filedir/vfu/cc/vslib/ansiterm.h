/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',LICENSE' OR COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: ansiterm.h,v 1.3 2003/01/21 19:56:35 cade Exp $
 *
 */

#ifndef _ANSITERM_H_
#define _ANSITERM_H_

///////////////////////////////////////////////////////////////////////////
//
// COLOR defines
//
  #ifndef CONCOLOR // to avoid duplicates with UNICON
  #define CONCOLOR(f,b) (b*16+f)
  #define COLORFG(t)    (t % 16)
  #define COLORBG(t)    (t / 16)
  #endif // CONCOLOR

  #ifndef cNORMAL // to avoid duplicates with UNICON
  #define cNORMAL    7
  #define cBOLD      8

  #define cBLACK     0
  #define cBLUE      1
  #define cGREEN     2
  #define cCYAN      3
  #define cRED       4
  #define cMAGENTA   5
  #define cBROWN     6
  #define cYELLOW    6
  #define cLGRAY     7
  #define chBLACK    7
  #define cWHITE     7
  #define cDGRAY     8
  #define chBLUE     9
  #define chGREEN   10
  #define chCYAN    11
  #define chRED     12
  #define chMAGENTA 13
  #define chYELLOW  14
  #define chWHITE   15
  #endif // cNORMAL

  int AnsiInit( int pANSI = -1 ); // 0=off, 1=on, -1=auto (TERM env.var)
  void AnsiDone();

  void AnsiSuspend(); // suspends console (before system() for example)
  void AnsiRestore(); // restores console after suspend

  void AnsiCE( int attr = -1 ); // clear to end-of-line
  void AnsiCS( int attr = -1 ); // clear screen

  void AnsiOut( int x, int y, const char *s );
  void AnsiOut( int x, int y, const char *s, int attr );
  void AnsiPuts( const char *s );
  void AnsiPuts( const char *s, int attr );

  void AnsiCHide(); // cursor hide
  void AnsiCShow(); // cursor show

  int AnsiMaxX();
  int AnsiMaxY();
  int AnsiX();
  int AnsiY();

  void AnsiFG( int color );
  void AnsiBG( int color );
  void AnsiTA( int attr );

  void AnsiXY( int x, int y ); // go to x,y

  int AnsiKbHit();
  int AnsiGetch();
  void AnsiBeep();



#endif //_ANSITERM_H_

 // eof ansiterm.h
