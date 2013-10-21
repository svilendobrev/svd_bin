/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" 1996-2003
 * http://soul.datamax.bg/~cade  <cade@biscom.net>  <cade@datamax.bg>
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: vfumenu.h,v 1.5 2003/01/26 21:48:42 cade Exp $
 *
 */

#ifndef _VFUMENU_H_
#define _VFUMENU_H_

#include <vslib.h>
#include "vfuuti.h"

#define menu_box_info con_default_menu_info

int vfu_toggle_box( int x, int y, const char *title, ToggleEntry* toggles );
int vfu_menu_box( int x, int y, const char *title, VArray *va = &mb );
int vfu_menu_box( const char* title, const char* menustr, int row = -1 );


#endif /* _VFUMENU_H_ */

/* eof vfumenu.h */
