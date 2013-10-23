/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: unicon.cpp,v 1.4 2003/01/21 19:56:35 cade Exp $
 *
 */

#include "unicon.h"
#include "locale.h"

/****************************************************************************
**
** DJGPP/DOS Part
**
****************************************************************************/

#ifdef _TARGET_GO32_

#include <pc.h>
#include <dos.h>
#include <conio.h>
#include "vstring.h"

  int original_ta;

  text_info ti;
  int __fg;
  int __bg;
  int __ta;

  int con_init()
  {
    gppconio_init();
    gettextinfo( &ti );
    original_ta = ti.attribute;
    return 0;
  };

  void con_done()
  {
    textattr( original_ta );
    return;
  };

  void con_suspend() { return; };
  void con_restore() { return; };

  void con_ce( int attr )
  {
    if (attr != -1)
      {
      int ta = __ta;
      textattr( attr );
      clreol();
      textattr( ta );
      }
    else
      clreol();
  };

  void con_cs( int attr )
  {
    if (attr != -1)
      {
      int ta = __ta;
      textattr( attr );
      clrscr();
      gotoxy(1,1);
      textattr( ta );
      }
    else
      {
      clrscr();
      gotoxy(1,1);
      }
  };

  void con_puts( const char *s )
  {
    #ifdef _TARGET_GO32_
    VString str = s;
    str_replace( str, "\n", "\r\n" );
    cputs( str );
    #else
    cputs( s );
    #endif
  };

  int con_max_x() { return ti.screenwidth; };
  int con_max_y() { return ti.screenheight; };
  int con_x() { return wherex(); };
  int con_y() { return wherey(); };
  void con_fg( int color ) { __fg = color; __ta = CONCOLOR(__fg,__bg); textattr( __ta ); };
  void con_bg( int color ) { __bg = color; __ta = CONCOLOR(__fg,__bg); textattr( __ta ); };
  void con_ta( int attr ) { __ta = attr; __bg = COLORBG(attr); __fg = COLORFG(attr); textattr( attr ); };
  void con_xy( int x, int y ) { gotoxy( x, y ); };

  void con_chide() { _setcursortype( _NOCURSOR ); };
  void con_cshow() { _setcursortype( _NORMALCURSOR ); };

  int con_kbhit() { return kbhit(); };
  int con_getch()
  {
    char ch = getch();
    if ( ch == 0 )
      return KEY_PREFIX + getch();
    else
      return ch;
  };

  void con_beep()
  {
    sound(800);
    delay(1); // 1/10 second
    sound(0);
  };

#endif /* _TARGET_GO32_ */

/****************************************************************************
**
** UNIX Part
**
****************************************************************************/

#ifdef _TARGET_UNIX_

/****************************************************************************
** This part is loosely based on `linconio':
** ---------------------------------------------------------------------
** File: conio.h     Date: 03/09/1997       Version: 1.02
** CONIO.H an implementation of the conio.h for Linux based on ncurses.
** This is copyright (c) 1996,97 by Fractor / Mental EXPlosion.
** If you want to copy it you must do this following the terms of the
** GNU Library Public License
** Please read the file "README" before using this library.
****************************************************************************/

  int __fg;
  int __bg;
  int __ta;
  WINDOW *conio_scr;

  #define CON_PAIR(f,b) (((b)*8)+(f)+1)

  /* Some internals... */
  int colortab(int a) /* convert UNIX/Curses Color code to DOS-standard */
  {
     switch(a) {
        case cBLACK   : return COLOR_BLACK;
        case cBLUE    : return COLOR_BLUE;
        case cGREEN   : return COLOR_GREEN;
        case cCYAN    : return COLOR_CYAN;
        case cRED     : return COLOR_RED;
        case cMAGENTA : return COLOR_MAGENTA;
        case cYELLOW  : return COLOR_YELLOW;
        case cWHITE   : return COLOR_WHITE;
     }
     return 0;
  }

  int con_init()
  {
    setlocale(LC_ALL,"");
    initscr();
    start_color();
    qiflush();
    cbreak();
    if ( !getenv("UNICON_NO_RAW") )
      {
      /* To allow curses app to handle properly ctrl+z, ctrl+c, etc.
         I should not call raw() here, anyway it is known that this
         will cause misinterpretation of some keys (arrows) after
         resuming (SUSP -- ctrl+z)...
         So, unless UNICON_NO_RAW exported and set to any value raw()
         is called as usual.
      */
      raw();
      }
    noecho();
    nonl(); // `return' translation off
    if (!has_colors())
       fprintf(stderr,"Attention: A color terminal may be required to run this application !\n");
    conio_scr=newwin(0,0,0,0);
    keypad(conio_scr,TRUE); // allow function keys (keypad)
    meta(conio_scr,TRUE); // switch to 8 bit terminal return values
    // intrflush(conio_scr,FALSE); //
    idlok(conio_scr,TRUE);      // hardware line ins/del (required?)
    idcok(conio_scr,TRUE);      // hardware char ins/del (required?)
    scrollok(conio_scr,TRUE);   // scroll screen if required (cursor at bottom)
    /* Color initialization */
    for ( __bg=0; __bg<8; __bg++ )
       for ( __fg=0; __fg<8; __fg++ )
          init_pair( CON_PAIR(__fg,__bg), colortab(__fg), colortab(__bg));
    con_ta(7);
    return 0;
  };

  void con_done()
  {
    delwin(conio_scr);
    endwin();
  };

  void con_suspend()
  {
    con_done();
  };

  void con_restore()
  {
    con_init();
  };

  void con_ta( int attr )
  {
    __ta = attr;
    wattrset(conio_scr,0); /* (???) My curses-version needs this ... */
    __fg = COLORFG(attr);
    __bg = COLORBG(attr);
    wattrset(conio_scr,COLOR_PAIR(CON_PAIR( __fg%8, __bg%8 )) | ( __bg > 7 )*(A_BLINK) | ( __fg > 7 )*(A_BOLD) );
    wbkgdset( conio_scr, COLOR_PAIR(CON_PAIR( __fg%8, __bg%8 )) );
  };

  void con_ce( int attr )
  {
    if (attr != -1)
      {
      int ta = __ta;
      con_ta( attr );
      wclrtoeol(conio_scr);
      wrefresh(conio_scr);
      con_ta( ta );
      }
    else
      {
      wclrtoeol(conio_scr);
      wrefresh(conio_scr);
      }
  };

  void con_cs( int attr )
  {
    if (attr != -1)
      {
      int ta = __ta;
      con_ta( attr );
      wclear(conio_scr);
      wmove(conio_scr,0,0);
      wrefresh(conio_scr);
      con_ta( ta );
      }
    else
      {
      wclear(conio_scr);
      wmove(conio_scr,0,0);
      wrefresh(conio_scr);
      }
  };

  void con_puts( const char *s )
  {
    waddstr(conio_scr,s);
    wrefresh(conio_scr);
  };

  int con_max_x()
  {
    int x;
    int y;
    getmaxyx(conio_scr,y,x);
    return(x);
  };

  int con_max_y()
  {
    int x;
    int y;
    getmaxyx(conio_scr,y,x);
    return(y);
  };

  int con_x()
  {
    int y;
    int x;
    getyx(conio_scr,y,x);
    return(x+1);
  };

  int con_y()
  {
    int y;
    int x;
    getyx(conio_scr,y,x);
    return(y+1);
  };

  void con_fg( int color )
  {
    __fg=color;
    con_ta( CONCOLOR( __fg, __bg ) );
  };

  void con_bg( int color )
  {
    __bg=color;
    con_ta( CONCOLOR( __fg, __bg ) );
  };


  void con_xy( int x, int y )
  {
    wmove(conio_scr,y-1,x-1);
    wrefresh(conio_scr);
  };

  void con_chide()
  {
    con_xy( 1, 1 );
    leaveok(conio_scr,TRUE);
    curs_set( 0 );
  };

  void con_cshow()
  {
    leaveok(conio_scr,FALSE);
    curs_set( 1 );
  };

  int con_kbhit()
  {
    int i;
    nodelay(conio_scr,TRUE);
    i=wgetch(conio_scr);
    nodelay(conio_scr,FALSE);
    if (i==-1)
      i=0;
    else
      ungetch(i);
    return(i);
  };

  int con_getch()
  {
    int i;
    i=wgetch(conio_scr);
    if (i==-1) i=0;
    if (i == 27)
      if (con_kbhit())
        i = KEY_PREFIX + wgetch(conio_scr);
    #ifndef _NO_ALT_ESCAPE_SAME_
    if (i == KEY_PREFIX + 27) i = 27;
    #endif
    return(i);
  };

  void con_beep()
  {
    printf( "\007" );
    fflush( stdout );
  };

#endif /* _TARGET_UNIX_ */

/****************************************************************************
**
** COMMON Part
**
****************************************************************************/

  void con_out( int x, int y, const char *s )
  {
    con_out( x, y, s, __ta );
  };

  void con_out( int x, int y, const char *s, int attr )
  {
    int ta = __ta;
    con_ta( attr );
    con_xy( x, y );
    con_puts( s );
    con_ta( ta );
  };

  void con_puts( const char *s, int attr )
  {
    int ta = __ta;
    con_ta( attr );
    con_puts( s );
    con_ta( ta );
  }

/****************************************************************************
** EOF
****************************************************************************/

