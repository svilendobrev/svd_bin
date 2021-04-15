/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',LICENSE' OR COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: conmenu.cpp,v 1.10 2005/06/06 06:20:20 cade Exp $
 *
 */

#include <ctype.h>

#include <unicon.h>
#include <vstring.h>
#include <scroll.h>
#include "conmenu.h"

ConMenuInfo con_default_menu_info;

int con_toggle_box( int x, int y, const char *title, ToggleEntry* toggles, ConMenuInfo *menu_info  )
{
  ScrollPos scroll;
  int z;

  int w = -1;
  int h = -1;

  int maxlen = 0;
  int count  = 0;
  while( toggles[count].key != -1 )
    {
    int sl = strlen( toggles[count].name );
    if (sl > maxlen) maxlen = sl;
    count++;
    }
  maxlen += 6+3; // 6 for state string and 3 for " key " string in the front

  if (w == -1) w = maxlen;
  if (h == -1) h = count;

  z = strlen(title);
  if (w < z) w = z;
  if (h > count) h = count;
  if (h == 0) h = 1;

  // FIXME: those should be fixed!!!
  if (x + w > con_max_x()) w = con_max_x() - x - 1;
  if (y + h > con_max_y()-4) h = con_max_y() - y - 5;

  VString str;
  VString str1;
  VString hots = "";
  for(z = 0; z < count; z++)
    if (strncmp("--", toggles[z].name, 2))
      str_add_ch( hots, toggles[z].key );
    else
      str_add_ch( hots,' ' );
  con_xy(x,y);
  int ch = 0;

  str = "";
  str = title;
  str_pad( str,-w, menu_info->bo ? '-' : ' ' );
  if (str_len(str) > w) str_sleft(str,w);
  if (menu_info->bo)
    str = ".-" + str + "-.";
  else
    str = "  " + str + "  ";
  con_out(x,y,str,menu_info->ti);
  y++;

  scroll.wrap = 1;
  scroll.set_min_max( 0, count-1 );
  scroll.set_pagesize( h );
  scroll.go( 0 );

  while(1)
    {
    for( z = 0; z < scroll.pagesize(); z++ )
      {
      if (scroll.page() + z >= count)
        {
        str = " ~";
        str_pad( str, -(w+2), ' ');
        }
      else
        {
        int sep = (strncmp("--", toggles[scroll.page()+z].name, 2) == 0);
        if (sep)
          {
          str = "";
          str += toggles[scroll.page()+z].name;
          str_pad( str, -w, '-');
          str += "--";
          }
        else
          {
          str = " "; str_add_ch( str, toggles[scroll.page()+z].key ); str += " ";
          str += toggles[scroll.page()+z].name;
          str_pad( str, -(w-6), ' ');
          str1 = toggles[scroll.page()+z].states[*(toggles[scroll.page()+z].data)];
          str_pad( str1, 6, ' '); str1 += " ";
          str += " " + str1;
          }
        }
      if (menu_info->bo)
        str = "|" + str + "|";
      else
        str = " " + str + " ";
//      if (str.len() > w) StrSLeft(str,w);
//      str = " " + str + " ";
      con_out( x, y+z, str, ( scroll.page()+z != scroll.pos() ) ? menu_info->cn : menu_info->ch );
      }
    if (menu_info->bo)
      {
      str = "";
      str_pad( str, w+2, '-' );
      str = "`" + str + "'";
      con_out( x, y+scroll.pagesize(), str, menu_info->cn );
      }
    ch = con_getch();
    menu_info->ec = ch;

    if ( ch == KEY_UP    ) scroll.up();
    if ( ch == KEY_DOWN  ) scroll.down();
    if ( ch == KEY_NPAGE ) scroll.npage();
    if ( ch == KEY_PPAGE ) scroll.ppage();
    if ( ch == KEY_HOME  ) scroll.home();
    if ( ch == KEY_END   ) scroll.end();

    if ( ch < 0 || ch > 255 ) continue;
    if ( ch == 27 ) return 0;
    if ( ch == 13 /* && strncmp("--", toggles[scroll.pos].name, 2) */ ) return 1;
    if (menu_info->key_translator) ch = menu_info->key_translator( ch) ;
    z = ( ch == ' ' ) ? scroll.pos() : str_find( hots, ch );
    if (z > -1 && strncmp("--", toggles[z].name, 2) )
      {
      int state = *(toggles[z].data) + 1;
      if (toggles[z].states[state] == NULL) state = 0;
      *(toggles[z].data) = state;
      }
    }
  return -1;
}

int con_menu_box( int x, int y, const char *title, VArray *va, int hotkeys, ConMenuInfo *menu_info  )
{
  ScrollPos scroll;
  int z;

  int w = -1;
  int h = -1;

  if (w == -1) w = va->max_len();
  if (h == -1) h = va->count();

  z = strlen(title);
  if (w < z) w = z;
  if (h > va->count()) h = va->count();
  if (h == 0) h = 1;

  // FIXME: those should be fixed!!!
  if (x + w > con_max_x()) w = con_max_x() - x - 4;
  if (y + h > con_max_y()-4) h = con_max_y() - y - 4;

  VString str;
  VString hots = "";
  if ( hotkeys > -1 )
    {
    for(z = 0; z < va->count(); z++)
      if (strncmp("--", va->get(z), 2))
        str_add_ch( hots, char(((const char*)(va->get(z)))[hotkeys]) );
      else
        str_add_ch( hots,' ' );
    str_up(hots);
    }
  con_xy(x,y);
  int ch = 0;

  str = " ";
  str += title;
  str += " ";
  str_pad( str,-(w), menu_info->bo ? '-' : ' ' );
  if (str_len(str) > w) str_sleft(str,w);
  if (menu_info->bo)
    str = ".-" + str + "-.";
  else
    str = "  " + str + "  ";
  con_out(x,y,str,menu_info->ti);
  y++;

  scroll.wrap = 1;
  scroll.set_min_max( 0, va->count()-1 );
  scroll.set_pagesize( h );
  scroll.go( 0 );

  while(1)
    {
    for( z = 0; z < scroll.pagesize(); z++ )
      {
      str = (scroll.page()+z >= va->count())? "~" : va->get(scroll.page()+z);

      if ( menu_info->hide_magic[0] )
        {
        int i = str_rfind( str, menu_info->hide_magic );
        if ( i != -1)
          str_sleft( str, i );
        }

      str_pad( str,-w , (strncmp("--", str, 2) == 0)?'-':' ');
      if (str_len(str) > w)
        str = str_dot_reduce( str, w );
      if (menu_info->bo)
        str = "| " + str + " |";
      else
        str = "  " + str + "  ";
      con_out( x, y+z, str, ( scroll.page()+z != scroll.pos() ) ? menu_info->cn : menu_info->ch );
      }
    if (menu_info->bo)
      {
      str = "";
      str_pad( str, w+2, '-' );
      str = "`" + str + "'";
      con_out( x, y+scroll.pagesize(), str, menu_info->cn );
      }
    ch = con_getch();
    menu_info->ec = ch;

    if ( ch == KEY_UP    ) scroll.up();
    if ( ch == KEY_DOWN  ) scroll.down();
    if ( ch == KEY_NPAGE ) scroll.npage();
    if ( ch == KEY_PPAGE ) scroll.ppage();
    if ( ch == KEY_HOME  ) scroll.home();
    if ( ch == KEY_END   ) scroll.end();

    if ( ch < 0 || ch > 255 ) continue;
    if ( ch == 27 )
      {
      menu_info->ac = 0;
      return -1;
      }
    if ( ch == 13 )
      {
      if (strncmp("--", va->get(scroll.pos()), 2) != 0) // ako e "--" e separator
        {
        menu_info->ec = hots[scroll.pos()];
        menu_info->ac = -1;
        return scroll.pos();
        }
      }
    if ( menu_info->ac > -1 && ch == menu_info->ac )
      {
      if (strncmp("--", va->get(scroll.pos()), 2) != 0) // ako e "--" e separator
        {
        menu_info->ec = hots[scroll.pos()];
        menu_info->ac = -2;
        return scroll.pos();
        }
      }
    if (menu_info->key_translator) ch = menu_info->key_translator( ch) ;
    z = str_find( hots, toupper(ch) );
    if (z > -1)
      {
      menu_info->ec = hots[z];
      menu_info->ac = -1;
      return z;
      }
    }
  menu_info->ac = -1;
  return -1;
};

int con_full_box( int x, int y, const char *title, VArray *va, ConMenuInfo *menu_info )
{
  ScrollPos scroll;
  scroll.wrap = 0;
  scroll.set_min_max( 0, va->count()-1 );
  scroll.set_pagesize( con_max_y() - 3 ); /* one title and two status */
  scroll.go( 0 );

  char pos_str[32];

  con_xy( 1, 1 );
  con_puts( title, menu_info->ti );
  con_ce( menu_info->ti );
  while(4)
    {
    VString str;
    int z;
    for( z = 0; z < scroll.pagesize(); z++ )
      {
      if ( scroll.page() + z < va->count() )
        str = va->get( scroll.page() + z );
      else
        str = "~";
      str = str_dot_reduce( str, con_max_x()-1 );
      con_xy( 1, z + 2 );
      int c = ( scroll.page() + z == scroll.pos() ) ? menu_info->ch : menu_info->cn;
      con_puts( str, c );
      con_ce( c );
      }
    sprintf( pos_str, " %5d of %5d", scroll.pos()+1, scroll.max()+1 );
    con_out( con_max_x() - 15, 1, pos_str, menu_info->ti );
    int ch;
    switch( (ch = con_getch()) )
      {
      case 27 : menu_info->ec = 27; return -1; break;
      case 13 : menu_info->ec = 13; return scroll.pos(); break;
      case KEY_UP    : scroll.up(); break;
      case KEY_DOWN  : scroll.down(); break;
      case KEY_NPAGE : scroll.npage(); break;
      case KEY_PPAGE : scroll.ppage(); break;
      case KEY_HOME  : scroll.home(); break;
      case KEY_END   : scroll.end(); break;
      default:
        if ( tolower(ch) == tolower(menu_info->ac) )
          {
          menu_info->ec = menu_info->ac;
          return -2;
          }
          break;
      }
    }
}

