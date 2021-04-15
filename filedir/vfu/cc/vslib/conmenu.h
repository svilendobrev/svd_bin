/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',LICENSE' OR COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: conmenu.h,v 1.4 2003/01/21 19:56:35 cade Exp $
 *
 */

#ifndef _CONMENU_H_
#define _CONMENU_H_

#include <vstrlib.h>

struct  ToggleEntry
{
  int  key;
  char name[64];
  int  *data;
  const char **states;
};

struct ConMenuInfo
{
  ConMenuInfo() { defaults(); }
  void defaults() { cn = 112; ch = 47; ti = 95; bo = ec = ac = 0; }

  int cn; // normal color
  int ch; // highlight color
  int ti; // title color

  int bo; // should view borders?

  int ec; // exit char (used by con_menu_box)
  int ac; // alternative confirm (used by menu box)

  int st; // scroll type -- 1 dynamic and 0 normal/static
  char hide_magic[32];

  int (*key_translator)( int);
};

extern ConMenuInfo con_default_menu_info;

int con_toggle_box( int x, int y, const char *title, ToggleEntry* toggles, ConMenuInfo *menu_info );
int con_menu_box( int x, int y, const char *title, VArray *va, int hotkeys, ConMenuInfo *menu_info );

/* show full screen varray list (w/o last two lines of the screen) */
int con_full_box( int x, int y, const char *title, VArray *va, ConMenuInfo *menu_info );

#endif //_CONMENU_H_
