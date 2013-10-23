/*
 *
 *  VSTRING Library
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *  Distributed under the GPL license, you should receive copy of GPL!
 *
 *  VSTRING library provides vast set of string manipulation features
 *  including dynamic string object that can be freely exchanged with
 *  standard char* type, so there is no need to change function calls
 *  nor the implementation when you change from char* to VString (and
 *  vice versa). The main difference from other similar libs is that
 *  the dynamic VString class has no visible methods (except operators)
 *  so you will use it as a plain char* but it will expand/shrink as
 *  needed.
 *
 *  Thank you for the attention!
 *  If you find bug or you have note about vstring lib, please feel
 *  free to contact me at:
 *
 *  Vladi Belperchinov-Shabanski "Cade"
 *  <cade@biscom.net>
 *  <cade@datamax.bg>
 *  http://soul.datamax.bg/~cade
 *
 *  NOTE: vstring was initially (and loosely) based on
 *        `cxstring' lib (c) Ivo Baylov 1998.
 *  NOTE: vstring is distributed standalone as well as a part from vslib.
 *
 *  This file (vstring.h and vstring.cpp) implements plain string-only
 *  manipulations. For further functionality see vstrlib.h and vstrlib.cpp.
 *
 *  $Id: vstring.h,v 1.22 2003/04/28 17:17:13 cade Exp $
 *
 */

#ifndef _VSTRING_H_
#define _VSTRING_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <assert.h>
#ifndef ASSERT
#define ASSERT assert
#endif

/***************************************************************************
**
** GLOBALS
**
****************************************************************************/

#define VARRAY_BLOCK_SIZE 2048

class VTrie;   /* forward */
class VArray;  /* forward */
class VRegexp; /* forward */

#define VHash   VTrie;   /* using casual names... */
#define VRegExp VRegexp; /* using casual names... */

/***************************************************************************
**
** VREF
**
****************************************************************************/

class VRef
{
  int _ref;

public:

  VRef() { _ref = 1; }  // creator get first reference
  virtual ~VRef() { ASSERT( _ref == 0 ); }

  void ref() { _ref++; }
  void unref() { ASSERT( _ref > 0 ); _ref--; if ( _ref == 0 ) delete this; }

  int refs() { return _ref; }
};

/****************************************************************************
**
** VSTRING BOX
**
****************************************************************************/

class VStringBox: public VRef
{
public:

  int   sl;   // string buffer length
  int   size; // internal buffer size
  char* s;    // internal buffer

  int   compact;

  VStringBox() { s = NULL; sl = size = compact = 0; resize_buf( 0 ); };
  ~VStringBox() { undef(); if ( s ) free( s ); };

  VStringBox* clone();

  void resize_buf( int new_size );
  void undef() { resize_buf( 0 ); sl = 0; };
};


/****************************************************************************
**
** VSTRING
**
****************************************************************************/

#define STR_BLOCK_SIZE    256

class VString
{
  VStringBox* box;
  char retch; // used to return char& for off-range char index

  void detach();

public:

  VString( const VString& str )
    {
    box = str.box;
    box->ref();
    };

  VString()                      {  box = new VStringBox(); };
  VString( const char*    ps  )  {  box = new VStringBox(); set( ps);  };
  VString( const int      n   )  {  box = new VStringBox(); i(n);     };
  VString( const long     n   )  {  box = new VStringBox(); l(n);     };
  VString( const double   n   )  {  box = new VStringBox(); f(n);     };
  ~VString() { box->unref(); };

  void compact( int a_compact ) // set this != 0 for compact (memory preserving) behaviour
       { box->compact = a_compact; }; //FIXME: detach() first?

  void resize( int new_size )
       { detach(); box->resize_buf( new_size ); };

  void undef()
       { box->unref(); box = new VStringBox(); };

  const VString& operator  = ( const VString& str )
    {
    box->unref();
    box = str.box;
    box->ref();
    return *this;
    };

  const VString& operator  = ( const char*   ps   ) { set(ps);return *this; };
  const VString& operator  = ( const int     n    ) { i(n);   return *this; };
  const VString& operator  = ( const long    n    ) { l(n);   return *this; };
  const VString& operator  = ( const double  n    ) { f(n);   return *this; };

  const VString& operator += ( const VString& str )
        { cat( str.box->s ); return *this; };
  const VString& operator += ( const char*  ps    )
        { cat( ps ); return *this; };
  const VString& operator += ( const int    n     )
        { VString tmp = n; cat(tmp); return *this; };
  const VString& operator += ( const long   n     )
        { VString tmp = n; cat(tmp); return *this; };
  const VString& operator += ( const double n     )
        { VString tmp = n; cat(tmp); return *this; };

  const VString& operator *= ( const int    n     )
        { return str_mul( *this, n ); };

  friend VString operator + ( const VString& str1, const VString& str2 )
         { VString res = str1; res += str2; return res; };
  friend VString operator + ( const VString& str1, const char* ps )
         { VString res = str1; res += ps; return res; };
  friend VString operator + ( const char* ps, const VString& str2 )
         { VString res = ps; res += str2; return res; };

  friend VString operator + ( const VString& str1, const int    n )
         { VString res = str1; res +=    n; return res; };
  friend VString operator + ( const int    n, const VString& str2 )
         { VString res =    n; res += str2; return res; };
  friend VString operator + ( const VString& str1, const long   n )
         { VString res = str1; res +=    n; return res; };
  friend VString operator + ( const long   n, const VString& str2 )
         { VString res =    n; res += str2; return res; };
  friend VString operator + ( const VString& str1, const double n )
         { VString res = str1; res +=    n; return res; };
  friend VString operator + ( const double n, const VString& str2 )
         { VString res =    n; res += str2; return res; };

  friend int operator == ( const VString& s1, const VString& s2 ) { return strcmp( s1, s2 ) == 0; };
  friend int operator == ( const char*    s1, const VString& s2 ) { return strcmp( s1, s2 ) == 0; };
  friend int operator == ( const VString& s1, const char*    s2 ) { return strcmp( s1, s2 ) == 0; };

  friend int operator != ( const VString& s1, const VString& s2 ) { return strcmp( s1, s2 ) != 0; };
  friend int operator != ( const char*    s1, const VString& s2 ) { return strcmp( s1, s2 ) != 0; };
  friend int operator != ( const VString& s1, const char*    s2 ) { return strcmp( s1, s2 ) != 0; };

  friend int operator >  ( const VString& s1, const VString& s2 ) { return strcmp( s1, s2 ) >  0; };
  friend int operator >  ( const char*    s1, const VString& s2 ) { return strcmp( s1, s2 ) >  0; };
  friend int operator >  ( const VString& s1, const char*    s2 ) { return strcmp( s1, s2 ) >  0; };

  friend int operator >= ( const VString& s1, const VString& s2 ) { return strcmp( s1, s2 ) >= 0; };
  friend int operator >= ( const char*    s1, const VString& s2 ) { return strcmp( s1, s2 ) >= 0; };
  friend int operator >= ( const VString& s1, const char*    s2 ) { return strcmp( s1, s2 ) >= 0; };

  friend int operator <  ( const VString& s1, const VString& s2 ) { return strcmp( s1, s2 ) <  0; };
  friend int operator <  ( const char*    s1, const VString& s2 ) { return strcmp( s1, s2 ) <  0; };
  friend int operator <  ( const VString& s1, const char*    s2 ) { return strcmp( s1, s2 ) <  0; };

  friend int operator <= ( const VString& s1, const VString& s2 ) { return strcmp( s1, s2 ) <= 0; };
  friend int operator <= ( const char*    s1, const VString& s2 ) { return strcmp( s1, s2 ) <= 0; };
  friend int operator <= ( const VString& s1, const char*    s2 ) { return strcmp( s1, s2 ) <= 0; };

  operator const char* ( ) const { return (const char*)box->s; }
  const char* data() { return box->s; }

  char& operator [] ( int n )
      {
      if ( n < 0 ) n = box->sl + n;
      if ( n < 0 || n >= box->sl )
        {
        retch = 0;
        return retch;
        }
      detach();
      return box->s[n];
      }

  void fixlen()
       { box->sl = strlen(box->s);
         ASSERT( box->sl < box->size ); }
  void fix()
       { box->sl = strlen(box->s);
         box->resize_buf(box->sl);
         ASSERT( box->sl < box->size ); }

  void   i( const int n );
  void   l( const long n );
  void   f( const double d );
  void   fi( const double d ); // sets double as int (w/o frac)

  int    i() { return atoi( box->s ); }
  long   l() { return atol( box->s ); }
  double f() { return atof( box->s ); }
  double fi() { return atof( box->s ); }

  void   set( const char* ps );
  void   cat( const char* ps );
  void   setn( const char* ps, int len );
  void   catn( const char* ps, int len );

  /* for debugging only */
  int check() { int len = strlen(box->s); return ((len == box->sl)&&(len<box->size)); }

  /****************************************************************************
  ** VString Friend Functions (for class VString)
  ****************************************************************************/

  inline friend int str_len( VString& target ) { return target.box->sl; };
  inline friend VString& str_set( VString& target, const char* ps ) { target.set( ps ); return target; };

  friend VString& str_mul( VString& target, int n ); // multiplies the VString n times, i.e. `1'*5 = `11111'
  friend VString& str_del    ( VString& target, int pos, int len ); // deletes `len' chars starting from `pos'
  friend VString& str_ins    ( VString& target, int pos, const char* s ); // inserts `s' in position `pos'
  friend VString& str_ins_ch ( VString& target, int pos, char ch ); // inserts `ch' in position `pos'
  friend VString& str_replace( VString& target, const char* out, const char* in ); // replace `out' w. `in'

  friend VString& str_copy  ( VString& target, const char* source, int pos = 0, int len = -1 ); // returns `len' chars from `pos'
  friend VString& str_left  ( VString& target, const char* source, int len ); // returns `len' chars from the left
  friend VString& str_right ( VString& target, const char* source, int len ); // returns `len' chars from the right
  friend VString& str_sleft ( VString& target, int len ); // SelfLeft -- just as 'Left' but works on `this'
  friend VString& str_sright( VString& target, int len ); // SelfRight -- just as 'Right' but works on `this'

  friend VString& str_trim_left ( VString& target, int len ); // trims `len' chars from the beginning (left)
  friend VString& str_trim_right( VString& target, int len ); // trim `len' chars from the end (right)

  friend VString& str_cut_left ( VString& target, const char* charlist ); // remove all chars `charlist' from the beginning (i.e. from the left)
  friend VString& str_cut_right( VString& target, const char* charlist ); // remove all chars `charlist' from the end (i.e. from the right)
  friend VString& str_cut      ( VString& target, const char* charlist ); // does `CutR(charlist);CutL(charlist);'
  friend VString& str_cut_spc  ( VString& target ); // does `Cut(" ");'

  friend VString& str_pad  ( VString& target, int len, char ch = ' ' );
  friend VString& str_comma( VString& target, char delim = ',' );

  // next 3 functions are safe! so if you get/set out f the VString range!
  friend void str_set_ch( VString& target, int pos, const char ch ); // sets `ch' char at position `pos'
  friend char str_get_ch( VString& target, int pos ); // return char at position `pos', -1 for the last char etc...
  friend void str_add_ch( VString& target, const char ch ); // adds `ch' at the end

  friend char*  str_word( VString& target, const char* delimiters, char* result );
  friend char*  str_rword( VString& target, const char* delimiters, char* result );
  // check VArray::split() instead of word() funtions...

  //FIXME: TODO: str_sprintf() should return VString!
  // this `sprintf'-like function works as follows:
  // 1. set `this.VString' length to `init_size'
  // 2. call `sprintf' with `format' and `...'
  // NOTE: You have to supply enough `init_size'! sorry...
  friend int sprintf( int init_size, VString& target, const char *format, ... );
  // this is equal to `printf( 1024, format, ... )', i.e. `init_size=1024'
  friend int sprintf( VString& target, const char *format, ... );


  friend VString& str_tr ( VString& target, const char *from, const char *to );
  friend VString& str_up ( VString& target );
  friend VString& str_low( VString& target );
  friend VString& str_flip_case( VString& target );

  friend VString& str_reverse  ( VString& target ); // reverse the VString: `abcde' becomes `edcba'
  friend VString& str_squeeze( VString& target, const char* sq_chars ); // squeeze repeating chars to one only

}; /* end of VString class */

/****************************************************************************
**
** VString Functions (for class VString)
**
****************************************************************************/

/****************************************************************************
**
** VString Functions (for char*)
**
****************************************************************************/

  inline int str_len( const char* ps ) { return strlen( ps ); };
  inline char* str_set( char* target, const char* ps ) { target[0] = 0; if (ps) strcpy( target, ps ); strcpy( target, ps ); return target; };

  char* str_mul( char* target, int n ); // multiplies the VString n times, i.e. `1'*5 = `11111'

  char* str_del    ( char* target, int pos, int len ); // deletes `len' chars starting from `pos'
  char* str_ins    ( char* target, int pos, const char* s ); // inserts `s' in position `pos'
  char* str_ins_ch ( char* target, int pos, char ch ); // inserts `ch' in position `pos'
  char* str_replace( char* target, const char* out, const char* in ); // replace `out' w. `in'

  int   str_overlap( const char* target, const char* source, int len = -1 ); // check if source and target overlap, returns 1 if they do

  char* str_copy  ( char* target, const char* source, int pos = 0, int len = -1 ); // returns `len' chars from `pos'
  char* str_left  ( char* target, const char* source, int len ); // returns `len' chars from the left
  char* str_right ( char* target, const char* source, int len ); // returns `len' chars from the right
  char* str_sleft ( char* target, int len ); // just as 'left' but works on `target'
  char* str_sright( char* target, int len ); // just as 'right' but works on `target'

  char* str_trim_left ( char* target, int len ); // trims `len' chars from the beginning (left)
  char* str_trim_right( char* target, int len ); // trim `len' chars from the end (right)

  // next 3 functions are safe! so if you get/set out f the VString range!
  // (note: that `char*' funcs are slower because of initial strlen() check
  void str_set_ch( char* target, int pos, const char ch ); // sets `ch' char at position `pos'
  char str_get_ch( char* target, int pos ); // return char at position `pos', -1 for the last char etc...
  void str_add_ch( char* target, const char ch ); // adds `ch' at the end

  // return first `word', i.e. from pos 0 to first found delimiter char
  // after that deletes this `word' from the VString
  char* str_word ( char* target, const char* delimiters, char* result );
  // ...same but `last' word reverse/rear
  char* str_rword( char* target, const char* delimiters, char* result );

  char* str_cut_left ( char* target, const char* charlist ); // remove all chars `charlist' from the beginning (i.e. from the left)
  char* str_cut_right( char* target, const char* charlist ); // remove all chars `charlist' from the end (i.e. from the right)
  char* str_cut      ( char* target, const char* charlist ); // does `CutR(charlist);CutL(charlist);'
  char* str_cut_spc  ( char* target ); // does `Cut(" ");'

  // expand align in a field, filled w. `ch', if len > 0 then right, else left
  char* str_pad( char* target, int len, char ch = ' ' );

  // insert `commas' for 1000's delimiter or use another delimiter
  // VString supposed to be a integer or real w/o `e' format
  char* str_comma( char* target, char delim = ',' );

  // translate chars from `from' to `to'
  // length of `from' MUST be equal to length of `to'
  char* str_tr( char* target, const char *from, const char *to );

  char* str_up ( char* target );
  char* str_low( char* target );
  char* str_flip_case( char* target );

  char* str_reverse( char* target ); // reverse the VString: `abcde' becomes `edcba'

  char* str_squeeze( char* target, const char* sq_chars ); // squeeze repeating chars to one only

/****************************************************************************
**
** VString Functions (for const char*)
**
****************************************************************************/

  VString str_up ( const char* src );
  VString str_low( const char* src );
  VString str_flip_case( const char* src );

/****************************************************************************
**
** VString Functions -- common (VString class will pass transparently)
**
****************************************************************************/

  int str_find ( const char* target, int c, int startpos = 0 ); // returns first zero-based position of char, or -1 if not found
  int str_rfind( const char* target, int c ); // returns last zero-based position of char, or -1 if not found
  int str_find ( const char* target, const char* s, int startpos = 0 ); // returns first zero-based position of VString, or -1 if not found
  int str_rfind( const char* target, const char* s ); // returns last zero-based position of VString, or -1 if not found

  int str_count( const char* target, const char* charlist, int startpos = 0 ); // returns match count of all chars from `charlist'
  int str_str_count( const char* target, const char* s, int startpos = 0 ); // returns match count of `s' VString into target

  int str_is_int   ( const char* target ); // check if VString is correct int value
  int str_is_double( const char* target ); // check if VString is correct double (w/o `e' format :( )

/***************************************************************************
**
** VARRAYBOX
**
****************************************************************************/

class VArrayBox : public VRef
{
public:

  VString** _data;
  int       _size;
  int       _count;

  VArrayBox() { _data = NULL; _size = 0; _count = 0; };
  ~VArrayBox() { undef(); };

  VArrayBox* clone();

  void resize( int new_size );
  void undef() { resize( 0 ); };
};

/***************************************************************************
**
** VARRAY
**
****************************************************************************/

class VArray
{
  VArrayBox *box;

  int       _fe; // foreach element index

  VString   _ret_str; // return-container

  void detach();
  void q_sort( int lo, int hi, int (*q_strcmp)(const char *, const char *) );

  public:

  int compact;

  VArray();
  VArray( const VArray& arr );
  VArray( const VTrie& tr );
  ~VArray();

  int count() { return box->_count; } // return element count

  void ins( int n, const char* s ); // insert at position `n'
  void del( int n ); // delete at position `n'
  void set( int n, const char* s ); // set/replace at position `n'
  const char* get( int n ); // get at position `n'

  void undef() // clear the array (frees all elements)
      { box->unref(); box = new VArrayBox(); _ret_str = ""; }

  int push( const char* s ); // add to the end of the array
  const char* pop(); // get and remove the last element

  int unshift( const char* s ); // add to the beginning of the array
  const char* shift(); // get and remove the first element

  int merge( VTrie *tr ); // return new elements count (same as += )
  int merge( VArray *arr ); // return new elements count (same as += )

  void print(); // print array data to stdout (console)

  int fload( const char* fname ); // return 0 for ok
  int fsave( const char* fname ); // return 0 for ok
  int fload( FILE* f ); // return 0 for ok
  int fsave( FILE* f ); // return 0 for ok

  void sort( int rev = 0, int (*q_strcmp)(const char *, const char *) = NULL ); // sort (optional reverse order)
  void reverse(); // reverse elements order
  void shuffle(); // randomize element order with Fisher-Yates shuffle

  VString& operator []( int n )
    {
      if ( n < 0 ) { _ret_str = ""; return _ret_str; }
      if ( n >= box->_count )
        set( n, "" );
      else
        detach(); // I don't know if user will change returned VString?!
      return *box->_data[n];
    }

  const VArray& operator = ( const VArray& arr )
    {
    box->unref();
    box = arr.box;
    box->ref();
    return *this;
    };

  const VArray& operator = ( const VTrie& tr )
    { undef(); merge( (VTrie*)&tr ); return *this; };
  const VArray& operator = ( const VString& str )
    { undef(); push( str ); return *this; };
  const VArray& operator += ( const VArray& arr )
    { merge( (VArray*)&arr ); return *this; };
  const VArray& operator += ( const VTrie& tr )
    { merge( (VTrie*)&tr ); return *this; };
  const VArray& operator += ( const VString& str )
    { push( str ); return *this; };

  /* utilities */

  /* implement `foreach'-like interface */
  void reset() // reset position to beginning
    { _fe = -1; };
  const char* next() // get next item or NULL for the end
    { _fe++; return _fe < box->_count ? box->_data[_fe]->data() : NULL; };
  const char* current() // get latest item got from next() -- current one
    { return _fe < box->_count ? box->_data[_fe]->data() : NULL; };
  int current_index() // current index
    { return _fe < box->_count ? _fe : -1; };

  int max_len(); // return the length of the longest string in the array
  int min_len(); // return the length of the shortest string in the array
};

/***************************************************************************
**
** VTRIENODE
**
****************************************************************************/

class VTrieNode
{
public:

  VTrieNode();
  ~VTrieNode();

  VTrieNode *next;
  VTrieNode *down;
  char      c;
  VString   *data;

  void detach() { next = down = NULL; }
  void del_node( const char *key, int branch = 0 );
  VTrieNode* find_node( const char* key, int create = 0 );

  VTrieNode *clone();
  void print();
};

/***************************************************************************
**
** VTRIEBOX
**
****************************************************************************/

class VTrieBox : public VRef
{
public:

  VTrieNode *root;

  VTrieBox()  { root = new VTrieNode(); }
  ~VTrieBox() { ASSERT( root ); delete root; }

  VTrieBox* clone();
  void undef() { ASSERT( root ); delete root; root = new VTrieNode(); };
};

/***************************************************************************
**
** VTRIE
**
****************************************************************************/

class VTrie
{
  VTrieBox *box;

  void detach();
  void trace_node( VTrieNode *node, VArray* keys, VArray *vals );

  VString temp_key;

  public:

  int compact;

  VTrie();
  VTrie( const VArray& arr );
  VTrie( const VTrie& tr );
  ~VTrie();

  void set( const char* key, const char* data ); // set data, same as []
  void del( const char* key ); // remove data associated with `key'
  const char* get( const char* key ); // get data by `key'

  int exists( const char* key ) // return != 0 if key exist (with data)
      { return box->root->find_node( key ) != NULL; }

  void undef() // delete all key+data pairs
    { box->unref(); box = new VTrieBox(); }

  void keys_and_values( VArray *keys, VArray *values );

  VArray keys(); // store keys to `arr', return keys count
  VArray values(); // store values to `arr',  return values count

  void reverse(); // reverse keys <-> values

  void merge( VTrie *tr ); // return new keys count (same as +=)
  void merge( VArray *arr ); // return new keys count (same as +=)

  //void print_nodes() { print_node( root ); }; // for debug only
  void print(); // print trie data to stdout (console)

  int fload( const char* fname ); // return 0 for ok
  int fsave( const char* fname ); // return 0 for ok
  int fload( FILE* f ); // return 0 for ok
  int fsave( FILE* f ); // return 0 for ok

  VString& operator []( const char* key )
    {
    detach(); // I don't know if user will change returned VString?!
    VTrieNode *node = box->root->find_node( key, 1 );
    ASSERT( node );
    if ( ! node->data )
      node->data = new VString();
    return *(node->data);
    }

  const VTrie& operator = ( const VTrie& tr )
    {
    box->unref();
    box = tr.box;
    box->ref();
    return *this;
    };

  const VTrie& operator = ( const VArray& arr )
    { undef(); merge( (VArray*)&arr ); return *this; };
  const VTrie& operator += ( const VArray& arr )
    { merge( (VArray*)&arr ); return *this; };
  const VTrie& operator += ( const VTrie& tr )
    { merge( (VTrie*)&tr ); return *this; };
};

/****************************************************************************
**
** VString Utility functions
**
****************************************************************************/

/* str_chop() removes last char from a VString (perl-like) */
inline char* str_chop( char* target ) { return str_trim_right( target, 1 ); };
inline VString& str_chop( VString& target ) { return str_trim_right( target, 1 ); };

/* reduces VString to the given width using dots:
   `this is long line' -> `this...ine'
   `s' can be NULL, then target will be reduced */
VString str_dot_reduce( const char* s, int width );

/****************************************************************************
**
** VString file names utilities -- functions and classes
** NOTE: does not use any external (outside this library) function calls!
**
****************************************************************************/

// adds trailing '/' if not exist
char* str_fix_path( char* s, int slashtype = '/' );
const char* str_fix_path( VString& s, int slashtype = '/' );

VString str_file_ext( const char *ps );       /* `ext'            */
VString str_file_name( const char *ps );     /* `filename'       */
VString str_file_name_ext( const char *ps ); /* `filename.ext'   */
VString str_file_path( const char *ps );     /* `/path/'         */

/* removes "/../"s, `path' can be NULL, then dest is fixed */
VString str_reduce_path( const char* path );

/****************************************************************************
**
** VString Conversions
**
****************************************************************************/

long hex2long( const char* s ); // hex to long

#endif /* _VSTRING_H_ */

/***************************************************************************
**
** EOF
**
****************************************************************************/


