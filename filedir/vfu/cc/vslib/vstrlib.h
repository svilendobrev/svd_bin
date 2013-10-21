/*
 *
 *  VSTRING Library supporting structures and functions
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *  Distributed under the GPL license, you should receive copy of GPL!
 *
 *  VSTRLIB library provides string data structures which mimic Perl's.
 *  There are several classes:
 *
 *  VArray -- array of VString elements
 *  VTrie -- associative array (hash) of VString elements
 *  VRegexp -- regular expression helper class
 *
 *  $Id: vstrlib.h,v 1.20 2004/04/04 23:18:20 cade Exp $
 *
 */

#ifndef _VSTRLIB_H_
#define _VSTRLIB_H_

#include <assert.h>
#ifndef ASSERT
#define ASSERT assert
#endif

#include <stdlib.h>
#include <time.h>
#include <pcre.h>

#include "vstring.h"

/***************************************************************************
**
** GLOBALS
**
****************************************************************************/

#define VCHARSET_BLOCK_SIZE 32

/* max pattern length for file_find_*() and ... */
#define MAX_PATTERN		2048

/* max file_grep() text line input length... :| */
#define MAX_GREP_LINE		4096


/****************************************************************************
**
** VString aditional functions
**
****************************************************************************/

char*  time2str( const time_t tim );
time_t str2time( const char* timstr );

int str_find_regexp( const char* target, const char* pattern, int startpos = 0 );
// warning: str_rfind_regexp() is slow! it can execute pattern matching to `n'
// times where n is the target string length...
int str_rfind_regexp( const char* target, const char* pattern );

/*****************************************************************************
**
** Hex string to pattern conversion
**
** Converts hex-string to binary pattern (data)
** example: `56 6C 61 64 69' -> ...
** returns pattern length
**
*****************************************************************************/

int hex_string_to_pattern( const char *str, char* pattern );

/*****************************************************************************
**
** Next mem* search functions are used to find pattern into memory block
** p is pattern, ps is pattern size, d is data searched and ds is its size
** return found pttern position or -1 for not found
**
*****************************************************************************/

int mem_kmp_search( const char *p, int ps, const char *d, int ds );
int mem_quick_search( const char *p, int ps, const char *d, int ds );
int mem_sum_search( const char *p, int ps, const char *d, int ds );

/* no-case versions */

int mem_quick_search_nc( const char *p, int ps, const char *d, int ds );

/*****************************************************************************
**
** Function which return position of pattern into a file
** this uses mem* functions above or defaults to mem_quick_search
**
*****************************************************************************/

long file_pattern_search( const char *p, int ps, FILE* f, const char* opt = "",
                          int (*mem_search)( const char *p, int ps,
                                             const char *d, int ds ) = NULL );

long file_pattern_search( const char *p, int ps, const char* fn, const char* opt = "",
                          int (*mem_search)( const char *p, int ps,
                                             const char *d, int ds ) = NULL );

/*****************************************************************************
**
** This function reads lines from a text file and runs regexp on it.
** file_grep_max_line defines the max line length read (1024)
** file_grep_lines_read reports how many lines are read in during the
**                      last file_grep() call
** re_string is regexp string, not arbitrary (binary) pattern
** spos defines what file start offset should be accepted
**
*****************************************************************************/

extern int file_grep_max_line;
extern int file_grep_lines_read;
long file_grep( const char *re_string, const char* file_name, int nocase, off_t spos = -1 );
long file_grep( const char *re_string, FILE* f, int nocase, off_t spos = -1 );

/*****************************************************************************
**
** Search interface functions
**
** options are:
**
** i    -- ignore case
** r    -- regular expression (grep)
** h    -- hex pattern search
**
*****************************************************************************/

long file_string_search( const char *p, const char* fn, const char* opt );
long file_string_search( const char *p, FILE *f, const char* opt );

int mem_string_search( const char *p, const char* d, const char* opt );

/***************************************************************************
**
** VREGEXP
**
****************************************************************************/
/*
** options are:
**               i -- case insensitive
**               m -- multiline matches
**               s -- single line (`.' matches and NEWLINE's)
**               x -- extended (ifnores whitespace and comments)
**
**               f -- plain find (substring) using quick search
**               h -- hex search, input pattern is converted from hex string
**
** for more docs see perlre(1) and pcre library docs
**
**
** WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING!
** extracting of the captured substring is only possible while subject input
** line which is used as matching target is intact! which means that if you
** change this line between match and substring extraction this will lead to
** segmentation fault!
**
*/

/* number of subpatterns which can be catched by VRegexp::m() */
#define VREGEXP_MAX_SUBS    32

class VRegexp
{
  /* search modes */
  enum SearchMode { MODE_REGEXP = 0, MODE_FIND, MODE_HEX };

  /* common data */
  SearchMode opt_mode;
  int opt_nocase; // 1 if caseless search needed

  /* regexp data */
  pcre*       re;
  pcre_extra *pe;
  int         sp[VREGEXP_MAX_SUBS*3]; // sub pointers
  int         rc;
  const char *lp; // last line matched ptr

  /* no-regexp/hex search pattern */
  char*       pt; // pattern
  int         pl; // pattern length
  int         pos; // last match found pos

  /* common data */
  VString errstr;

  int get_options( const char* opt );

  public:

  VRegexp();
  VRegexp( const char* pattern, const char *opt = NULL ); // compiles new regexp
  ~VRegexp();

  int comp( const char* pattern, const char *opt = NULL ); // compile re, return > 0 for success
  int study(); // optimizing regexp for (big-size) multiple matches
  int ok(); // return 1 if regexp is compiled ok, 0 if not

  int m( const char* line ); // execute re against line, return 1 for match
  int m( const char* line, const char* pattern, const char *opt = NULL ); // same as exec, but compiles first

  VString sub( int n ); // return n-th substring match
  int sub_sp( int n ); // return n-th substring start position
  int sub_ep( int n ); // return n-th substring end position

  VString operator []( int n ) // same as sub()
    { return sub( n ); }

  const char* error_str() { return errstr.data(); };
};

/***************************************************************************
**
** VCHARSET
**
****************************************************************************/

class VCharSet
  {
    unsigned char *_data;
    int            _size;  // size (in bytes)

    void resize( int new_size );

    public:

    VCharSet();
    ~VCharSet();

    void push( int n, int val = 1 );
    void undef( int n );
    void undef();

    int  in( int n );
/*

    push

    int  get ( int pn );

    void set_range1( int start, int end );
    void set_range0( int start, int end );

    void set_str1( const char* str );
    void set_str0( const char* str );

    int in( const char *str ); // return 1 if all str's chars are in the set
    int in( int pn )
        { if ( pn < 0 || pn >= size ) return 0; else return get( pn ); };

    void reverse() { for(int z = 0; z < datasize; z++) data[z] = ~data[z]; };
    void set( int pn, int val ) { if ( val ) set1( pn ); else set0( pn ); };
    void set_all1() { if ( data ) memset( data, 0xff, datasize ); };
    void set_all0() { if ( data ) memset( data, 0x00, datasize ); };

    const int operator [] ( int pn )
       { ASSERT( pn >= 0 && pn < size  ); return get( pn ); };

    int resize( int p_size );

    VCharSet& operator  = ( const VCharSet &b1 );
    VCharSet& operator &= ( const VCharSet &b1 );
    VCharSet& operator |= ( const VCharSet &b1 );
    VCharSet  operator  ~ ();

    friend VCharSet operator & ( const VCharSet &b1, const VCharSet &b2 );
    friend VCharSet operator | ( const VCharSet &b1, const VCharSet &b2 );
*/
  };

/***************************************************************************
**
** UTILITIES
**
****************************************************************************/

  // split `source' with `regexp_str' regexp
  VArray str_split( const char* regexp_str, const char* source, int maxcount = -1 );
  // split `source' with exact string `delimiter_str'
  VArray str_split_simple( const char* delimiter_str, const char* source, int maxcount = -1 );
  // join array data to single string with `glue' string
  // returns the result string or store to optional `dest'
  VString str_join( VArray array, const char* glue = "" );


/***************************************************************************
**
** MISC FUNCTIONS
**
****************************************************************************/



#endif /* _VSTRLIB_H_ */

/***************************************************************************
**
** EOF
**
****************************************************************************/

