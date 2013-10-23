/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: unicon.h,v 1.4 2003/01/21 19:56:35 cade Exp $
 *
 */

#ifndef _UNICON_H_
#define _UNICON_H_

#include "target.h"

#ifdef _TARGET_UNKNOWN_
  #error "I don't know what is the target platform"
#endif

#ifdef _TARGET_UNIX_
  #if defined(_TARGET_LINUX_)
  #include <curses.h>
  #elif defined(_TARGET_NETBSD_)
  #include <ncurses.h>
  #else
  #include <curses.h>
  #endif
  #include <stdlib.h>
#endif

/****************************************************************************
**
** COLOR defines
**
****************************************************************************/

  #define CONCOLOR(f,b) (b*16+f)
  #define COLORFG(t)    (t % 16)
  #define COLORBG(t)    (t / 16)

  /***** std-colors/normal ******/

  #define cNORMAL    7
  #define cBOLD      8
  #define cREVERSED  CONCOLOR(cBLACK,cWHITE)

  /***** low-colors/normal ******/

  #define cBLACK     0
  #define cBLUE      1
  #define cGREEN     2
  #define cCYAN      3
  #define cRED       4
  #define cMAGENTA   5
  #define cBROWN     6
  #define cYELLOW    6
  #define cLGRAY     7
  
  /***** hi-colors/bright *******/
  
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

/****************************************************************************
**
** KEY defines
**
****************************************************************************/

/******* common ************************************************************/

  #define KEY_CTRL_A    1
  #define KEY_CTRL_B    2
  #define KEY_CTRL_C    3
  #define KEY_CTRL_D    4
  #define KEY_CTRL_E    5
  #define KEY_CTRL_F    6
  #define KEY_CTRL_G    7
  #define KEY_CTRL_H    8
  #define KEY_CTRL_I    9
  #define KEY_CTRL_J   10
  #define KEY_CTRL_K   11
  #define KEY_CTRL_L   12
  #define KEY_CTRL_M   13
  #define KEY_CTRL_N   14
  #define KEY_CTRL_O   15
  #define KEY_CTRL_P   16
  #define KEY_CTRL_Q   17
  #define KEY_CTRL_R   18
  #define KEY_CTRL_S   19
  #define KEY_CTRL_T   20
  #define KEY_CTRL_U   21
  #define KEY_CTRL_V   22
  #define KEY_CTRL_W   23
  #define KEY_CTRL_X   24
  #define KEY_CTRL_Y   25
  #define KEY_CTRL_Z   26

#ifdef KEY_ENTER
#undef KEY_ENTER
#endif
#define KEY_ENTER	13

/******* DJGPP/DOS *********************************************************/

#ifdef _TARGET_GO32_
  #define KEY_PREFIX      1000
  #define KEY_BACKSPACE   8
  #define KEY_LEFT      (KEY_PREFIX + 75)
  #define KEY_RIGHT     (KEY_PREFIX + 77)
  #define KEY_UP        (KEY_PREFIX + 72)
  #define KEY_DOWN      (KEY_PREFIX + 80)
  #define KEY_HOME      (KEY_PREFIX + 71)
  #define KEY_END       (KEY_PREFIX + 79)
  #define KEY_PPAGE     (KEY_PREFIX + 73)
  #define KEY_NPAGE     (KEY_PREFIX + 81)
  #define KEY_IC        (KEY_PREFIX + 82)
  #define KEY_DC        (KEY_PREFIX + 83)

  #define KEY_F0        (KEY_PREFIX + 58)
  #define KEY_F(n)      (KEY_PREFIX + (58+(n)))

  #define KEY_F1        (KEY_PREFIX + 59)
  #define KEY_F2        (KEY_PREFIX + 60)
  #define KEY_F3        (KEY_PREFIX + 61)
  #define KEY_F4        (KEY_PREFIX + 62)
  #define KEY_F5        (KEY_PREFIX + 63)
  #define KEY_F6        (KEY_PREFIX + 64)
  #define KEY_F7        (KEY_PREFIX + 65)
  #define KEY_F8        (KEY_PREFIX + 66)
  #define KEY_F9        (KEY_PREFIX + 67)
  #define KEY_F10       (KEY_PREFIX + 68)

  #define KEY_SH_F1     (KEY_PREFIX +  84)
  #define KEY_SH_F2     (KEY_PREFIX +  85)
  #define KEY_SH_F3     (KEY_PREFIX +  86)
  #define KEY_SH_F4     (KEY_PREFIX +  87)
  #define KEY_SH_F5     (KEY_PREFIX +  88)
  #define KEY_SH_F6     (KEY_PREFIX +  89)
  #define KEY_SH_F7     (KEY_PREFIX +  90)
  #define KEY_SH_F8     (KEY_PREFIX +  91)
  #define KEY_SH_F9     (KEY_PREFIX +  92)
  #define KEY_SH_F10    (KEY_PREFIX +  93)

  #define KEY_CTRL_F1   (KEY_PREFIX +  94)
  #define KEY_CTRL_F2   (KEY_PREFIX +  95)
  #define KEY_CTRL_F3   (KEY_PREFIX +  96)
  #define KEY_CTRL_F4   (KEY_PREFIX +  97)
  #define KEY_CTRL_F5   (KEY_PREFIX +  98)
  #define KEY_CTRL_F6   (KEY_PREFIX +  99)
  #define KEY_CTRL_F7   (KEY_PREFIX + 100)
  #define KEY_CTRL_F8   (KEY_PREFIX + 101)
  #define KEY_CTRL_F9   (KEY_PREFIX + 102)
  #define KEY_CTRL_F10  (KEY_PREFIX + 103)

  #define KEY_ALT_F1    (KEY_PREFIX + 104)
  #define KEY_ALT_F2    (KEY_PREFIX + 105)
  #define KEY_ALT_F3    (KEY_PREFIX + 106)
  #define KEY_ALT_F4    (KEY_PREFIX + 107)
  #define KEY_ALT_F5    (KEY_PREFIX + 108)
  #define KEY_ALT_F6    (KEY_PREFIX + 109)
  #define KEY_ALT_F7    (KEY_PREFIX + 110)
  #define KEY_ALT_F8    (KEY_PREFIX + 111)
  #define KEY_ALT_F9    (KEY_PREFIX + 112)
  #define KEY_ALT_F10   (KEY_PREFIX + 113)

  #define KEY_ALT_1     (KEY_PREFIX + 120)
  #define KEY_ALT_2     (KEY_PREFIX + 121)
  #define KEY_ALT_3     (KEY_PREFIX + 122)
  #define KEY_ALT_4     (KEY_PREFIX + 123)
  #define KEY_ALT_5     (KEY_PREFIX + 124)
  #define KEY_ALT_6     (KEY_PREFIX + 125)
  #define KEY_ALT_7     (KEY_PREFIX + 126)
  #define KEY_ALT_8     (KEY_PREFIX + 127)
  #define KEY_ALT_9     (KEY_PREFIX + 128)
  #define KEY_ALT_0     (KEY_PREFIX + 129)
  #define KEY_ALT_MINUS (KEY_PREFIX + 130)
  #define KEY_ALT_EQ    (KEY_PREFIX + 131)

  #define KEY_ALT_Q     (KEY_PREFIX + 16)
  #define KEY_ALT_W     (KEY_PREFIX + 17)
  #define KEY_ALT_E     (KEY_PREFIX + 18)
  #define KEY_ALT_R     (KEY_PREFIX + 19)
  #define KEY_ALT_T     (KEY_PREFIX + 20)
  #define KEY_ALT_Y     (KEY_PREFIX + 21)
  #define KEY_ALT_U     (KEY_PREFIX + 22)
  #define KEY_ALT_I     (KEY_PREFIX + 23)
  #define KEY_ALT_O     (KEY_PREFIX + 24)
  #define KEY_ALT_P     (KEY_PREFIX + 25)

  #define KEY_ALT_A     (KEY_PREFIX + 30)
  #define KEY_ALT_S     (KEY_PREFIX + 31)
  #define KEY_ALT_D     (KEY_PREFIX + 32)
  #define KEY_ALT_F     (KEY_PREFIX + 33)
  #define KEY_ALT_G     (KEY_PREFIX + 34)
  #define KEY_ALT_H     (KEY_PREFIX + 35)
  #define KEY_ALT_J     (KEY_PREFIX + 36)
  #define KEY_ALT_K     (KEY_PREFIX + 37)
  #define KEY_ALT_L     (KEY_PREFIX + 38)

  #define KEY_ALT_Z     (KEY_PREFIX + 44)
  #define KEY_ALT_X     (KEY_PREFIX + 45)
  #define KEY_ALT_C     (KEY_PREFIX + 46)
  #define KEY_ALT_V     (KEY_PREFIX + 47)
  #define KEY_ALT_B     (KEY_PREFIX + 48)
  #define KEY_ALT_N     (KEY_PREFIX + 49)
  #define KEY_ALT_M     (KEY_PREFIX + 50)

#endif

/******* UNIX/NCURSES ******************************************************/

#ifdef _TARGET_UNIX_

  #define KEY_F1        (KEY_F(0) + 1)
  #define KEY_F2        (KEY_F(0) + 2)
  #define KEY_F3        (KEY_F(0) + 3)
  #define KEY_F4        (KEY_F(0) + 4)
  #define KEY_F5        (KEY_F(0) + 5)
  #define KEY_F6        (KEY_F(0) + 6)
  #define KEY_F7        (KEY_F(0) + 7)
  #define KEY_F8        (KEY_F(0) + 8)
  #define KEY_F9        (KEY_F(0) + 9)
  #define KEY_F10       (KEY_F(0) + 10)

  #define KEY_SH_F1     (KEY_F(0) + 11)
  #define KEY_SH_F2     (KEY_F(0) + 12)
  #define KEY_SH_F3     (KEY_F(0) + 13)
  #define KEY_SH_F4     (KEY_F(0) + 14)
  #define KEY_SH_F5     (KEY_F(0) + 15)
  #define KEY_SH_F6     (KEY_F(0) + 16)
  #define KEY_SH_F7     (KEY_F(0) + 17)
  #define KEY_SH_F8     (KEY_F(0) + 18)
  #define KEY_SH_F9     (KEY_F(0) + 19)
  #define KEY_SH_F10    (KEY_F(0) + 20)

  #define KEY_CTRL_F1   (-1)
  #define KEY_CTRL_F2   (-1)
  #define KEY_CTRL_F3   (-1)
  #define KEY_CTRL_F4   (-1)
  #define KEY_CTRL_F5   (-1)
  #define KEY_CTRL_F6   (-1)
  #define KEY_CTRL_F7   (-1)
  #define KEY_CTRL_F8   (-1)
  #define KEY_CTRL_F9   (-1)
  #define KEY_CTRL_F10  (-1)

  #define KEY_ALT_F1    (-1)
  #define KEY_ALT_F2    (-1)
  #define KEY_ALT_F3    (-1)
  #define KEY_ALT_F4    (-1)
  #define KEY_ALT_F5    (-1)
  #define KEY_ALT_F6    (-1)
  #define KEY_ALT_F7    (-1)
  #define KEY_ALT_F8    (-1)
  #define KEY_ALT_F9    (-1)
  #define KEY_ALT_F10   (-1)

  #define KEY_PREFIX    1000
  #define KEY_ALT_1     (KEY_PREFIX + '1')
  #define KEY_ALT_2     (KEY_PREFIX + '2')
  #define KEY_ALT_3     (KEY_PREFIX + '3')
  #define KEY_ALT_4     (KEY_PREFIX + '4')
  #define KEY_ALT_5     (KEY_PREFIX + '5')
  #define KEY_ALT_6     (KEY_PREFIX + '6')
  #define KEY_ALT_7     (KEY_PREFIX + '7')
  #define KEY_ALT_8     (KEY_PREFIX + '8')
  #define KEY_ALT_9     (KEY_PREFIX + '9')
  #define KEY_ALT_0     (KEY_PREFIX + '0')
  #define KEY_ALT_MINUS (KEY_PREFIX + '-')
  #define KEY_ALT_EQ    (KEY_PREFIX + '=')

  #define KEY_ALT_Q     (KEY_PREFIX + 'q')
  #define KEY_ALT_W     (KEY_PREFIX + 'w')
  #define KEY_ALT_E     (KEY_PREFIX + 'e')
  #define KEY_ALT_R     (KEY_PREFIX + 'r')
  #define KEY_ALT_T     (KEY_PREFIX + 't')
  #define KEY_ALT_Y     (KEY_PREFIX + 'y')
  #define KEY_ALT_U     (KEY_PREFIX + 'u')
  #define KEY_ALT_I     (KEY_PREFIX + 'i')
  #define KEY_ALT_O     (KEY_PREFIX + 'o')
  #define KEY_ALT_P     (KEY_PREFIX + 'p')

  #define KEY_ALT_A     (KEY_PREFIX + 'a')
  #define KEY_ALT_S     (KEY_PREFIX + 's')
  #define KEY_ALT_D     (KEY_PREFIX + 'd')
  #define KEY_ALT_F     (KEY_PREFIX + 'f')
  #define KEY_ALT_G     (KEY_PREFIX + 'g')
  #define KEY_ALT_H     (KEY_PREFIX + 'h')
  #define KEY_ALT_J     (KEY_PREFIX + 'j')
  #define KEY_ALT_K     (KEY_PREFIX + 'k')
  #define KEY_ALT_L     (KEY_PREFIX + 'l')

  #define KEY_ALT_Z     (KEY_PREFIX + 'z')
  #define KEY_ALT_X     (KEY_PREFIX + 'x')
  #define KEY_ALT_C     (KEY_PREFIX + 'c')
  #define KEY_ALT_V     (KEY_PREFIX + 'v')
  #define KEY_ALT_B     (KEY_PREFIX + 'b')
  #define KEY_ALT_N     (KEY_PREFIX + 'n')
  #define KEY_ALT_M     (KEY_PREFIX + 'm')

#endif

/******* common (part 2) ***************************************************/

  #define KEY_INSERT    KEY_IC
  #define KEY_INS       KEY_IC
  #define KEY_DELETE    KEY_DC
  #define KEY_DEL       KEY_DC

/****************************************************************************
**
** Functions
**
****************************************************************************/
  
  int con_init();  // should be called before any other con_xxx()
  void con_done(); // should be called at the end of the console io actions 

  void con_suspend(); // suspends console (before system() for example)
  void con_restore(); // restores console after suspend

  void con_ce( int attr = -1 ); // clear to end-of-line
  void con_cs( int attr = -1 ); // clear screen

  // following functions print string `s' at position `x,y' (col,row) with
  // color (attribute) `attr'
  void con_out( int x, int y, const char *s );
  void con_out( int x, int y, const char *s, int attr );
  void con_puts( const char *s );
  void con_puts( const char *s, int attr );

  void con_chide(); // cursor hide
  void con_cshow(); // cursor show

  int con_max_x(); // max screen x (column)
  int con_max_y(); // max screen y (row)
  int con_x();     // current screen x (column)
  int con_y();     // current screen y (row)

  void con_fg( int color ); // set foreground color
  void con_bg( int color ); // set background color
  void con_ta( int attr );  // set new attribute ( CONCOLOR(fg,bg) )

  void con_xy( int x, int y ); // move cursor to position x,y

  int con_kbhit(); // return != 0 if key is waiting in "keyboard" buffer 
  int con_getch(); // get single char from the "keyboard"
  void con_beep(); // make a "beep" sound

#endif /* _UNICON_H_ */
/****************************************************************************
** EOF
****************************************************************************/


