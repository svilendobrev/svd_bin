/*
 *
 *  VSTRING Library supporting structures and functions
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *  Distributed under the GPL license, see end of this file for full text!
 *
 *  $Id: vstrlib.cpp,v 1.28 2005/04/27 23:08:52 cade Exp $
 *
 */

#ifdef WIN32
#include "stdafx.h"
#endif

#include <ctype.h>

#include "vstrlib.h"

/****************************************************************************
**
** VString aditional functions
**
****************************************************************************/

  char* time2str( const time_t tim )
  {
    time_t t = tim;
    return ctime( &t );
  };

  time_t str2time( const char* timstr )
  {
    if (strlen( timstr ) < 24) return 0;
    char ts[32];
    struct tm m; memset( &m, 0, sizeof(m) );

    strcpy( ts, timstr );
    str_up( ts );
    //  0    5   10    5   20   4
    // "Wed Jun 30 21:49:08 1993\n"
    ts[24] = 0; m.tm_year = atoi( ts + 20 ) - 1900;
    ts[19] = 0; m.tm_sec  = atoi( ts + 17 );
    ts[16] = 0; m.tm_min  = atoi( ts + 14 );
    ts[13] = 0; m.tm_hour = atoi( ts + 11 );
    ts[10] = 0; m.tm_mday = atoi( ts +  8 );
    ts[ 7] = 0; m.tm_mon  = str_find( "JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC", ts+4 ) / 3;
    m.tm_yday = 0;
    m.tm_wday = 0;
    m.tm_isdst = -1;
    time_t tim = mktime( &m );
    return tim;
  };

  int str_find_regexp( const char* target, const char* pattern, int startpos )
  {
    VRegexp re;
    if ( ! re.comp( pattern ) ) return -1;
    if ( startpos < 0 ) return -1;
    int z = 0;
    while( startpos-- )
      {
      if ( target[z] == 0 ) return -1;
      z++;
      }
    if ( re.m( target + z ) )
      return z + re.sub_sp( 0 );
    else
      return -1;
  };

  int str_rfind_regexp( const char* target, const char* pattern )
  {
    VRegexp re;
    if ( ! re.comp( pattern ) ) return -1;
    int z = str_len( target );
    while(4)
      {
      z--;
      if ( re.m( target + z ) )
        return z + re.sub_sp( 0 );
      if ( z == 0 ) break;
      }
    return -1;
  };

/*****************************************************************************
**
** Hex string to pattern conversion
**
** Converts hex-string to binary pattern (data)
** example: `56 6C 61 64 69' -> ...
** returns pattern length
**
*****************************************************************************/

  int __hex_code( int ch )
  {
    ch = toupper( ch );
    if( ch >= '0' && ch <= '9' ) return ch - '0';
    if( ch >= 'A' && ch <= 'F' ) return ch - 'A' + 10;
    return -1;
  }

  int hex_string_to_pattern( const char *str, char* pattern )
  {
     const char *pc = pattern;
     while( *str )
     {
       while( *str == ' ' || *str == '\t' ) str++;
       int hex  = __hex_code( *str++ );
       if( hex == -1 )  return 0;
       int hex2 = __hex_code( *str++ );
       if( hex2 == -1 )  return 0;
       hex <<= 4;
       hex += hex2;
       *pattern = hex;
       pattern ++;
     }
     return pattern - pc;
  };

/*****************************************************************************
**
** Knuth-Morris-Pratt search
**
*****************************************************************************/

void __kmp_preprocess( const char* p, int ps, int* next )
{
 int i = 0;
 int j = next[0] = -1;
 while (i < ps)
   {
   while ((j > -1) && (p[i] != p[j])) j=next[j];
   i++;
   j++;
   next[i] = p[i] == p[j] ? next[j] : j;
   }
}

#define MAX_KMP_PATTERN_SIZE 1024

int mem_kmp_search( const char *p, int ps, const char *d, int ds )
{
   int i;
   int j;
   int next[MAX_KMP_PATTERN_SIZE];
   if ( ps > MAX_KMP_PATTERN_SIZE ) return -1;

   __kmp_preprocess( p, ps, next );

   i = j = 0;
   while (j < ds)
     {
     while (i > -1 && p[i] != d[j]) i = next[i];
     i++;
     j++;
     if (i >= ps) return j - i;
     }
   return -1;
}

/*****************************************************************************
**
** Quick Search (simplified Boyer-Moore)
**
** Note: currently only 256-symbol alphabet supported (ASCII)
**
** The difference from Boyer-Moore is that good-suffix shift is not used.
** Actually this is quick search with Horspool hint which is that rightmost
** char is examined first.
**
*****************************************************************************/

#define QS_ASIZE 256

void __qs_preprocess( const char* p, int ps, int* badc )
{
   int i;
   for (i = 0; i < QS_ASIZE; i++) badc[i] = ps + 1;
   for (i = 0; i < ps; i++) badc[(unsigned char)p[i]] = ps - i;
}

int mem_quick_search( const char *p, int ps, const char *d, int ds )
{
   int  badc[QS_ASIZE];
   __qs_preprocess( p, ps, badc);

   int j = 0;
   while (j <= ds - ps)
   {
      int i;
      for ( i = ps - 1; i >= 0 && p[i] == d[i + j]; --i );
      if ( i < 0 ) return j;
      j += badc[(unsigned char)d[j + ps]];
   }
   return -1;
}

/* no-case version */

void __qs_preprocess_nc( const char* p, int ps, int* badc )
{
   int i;
   for (i = 0; i < QS_ASIZE; i++) badc[i] = ps + 1;
   for (i = 0; i < ps; i++) badc[toupper((unsigned char)p[i])] = ps - i;
}

int mem_quick_search_nc( const char *p, int ps, const char *d, int ds )
{
   int  badc[QS_ASIZE];
   __qs_preprocess_nc( p, ps, badc);

   int j = 0;
   while (j <= ds - ps)
   {
      int i;
      for ( i = ps - 1; i >= 0 && toupper(p[i]) == toupper(d[i + j]); --i );
      if ( i < 0 ) return j;
      j += badc[toupper((unsigned char)d[j + ps])];
   }
   return -1;
}

/*****************************************************************************
**
** Sum search
**
** This exact form is made myself. It is not anything new or exceptional :)
** It is Karp-Rabin idea of searching `similar' pattern and if found check
** the actual one. The hash function here is simple sum of bytes in the range
** of pattern size.
**
** Mostly useless since Quick search performs better in almost all cases.
** I wrote it for benchmarking purpose.
**
*****************************************************************************/

int mem_sum_search( const char *p, int ps, const char *d, int ds )
{
   int psum = 0;

   int i;
   for( i = 0; i < ps; i++ ) psum += p[i];

   int j = 0;
   int sum = 0;
   while( j <= ds - ps )
     {
     if ( sum == psum && memcmp( p, d + j, ps ) == 0 ) return j;
     sum -= d[j];
     j++;
     sum += d[j+ps];
     }
   return -1;
};

/*****************************************************************************
**
** mem_*_search benchmarks:
**
** For simple benchmark I used ~700MB file and tried to find 10- and 70-chars
** patterns. Results in seconds for both cases (similar to 1-2 seconds) were:
**
** Quick  26
** KMP    42
** Sum    39
**
** Even though KMP returns right result I prefer Quick search for default!
** (last one was joke:))
**
** Case insensitive search is 2 times slower due to the simple implementation.
**
*****************************************************************************/

/*****************************************************************************
**
** file search frontend
**
*****************************************************************************/

long file_pattern_search( const char *p, int ps, FILE* f, const char* opt,
                          int (*mem_search)( const char *p, int ps,
                                             const char *d, int ds ) )
{
   #define BUFSIZE  (1024*1024)
   char* buff = new char[BUFSIZE];

   int nocase = str_find( opt, 'i' ) > -1;
   char* np = new char[ps+1];
   ASSERT(np);
   memcpy( np, p, ps );
   np[ps] = 0;

   if ( ! mem_search )
     mem_search = mem_quick_search;
   if ( nocase )
     mem_search = mem_quick_search_nc;

   off_t pos = -1;
   while(4)
     {
     int bs = fread( buff, 1, BUFSIZE, f );
     int cpos = mem_search( np, ps, buff, bs );
     if ( cpos > -1 )
       {
       pos = ftello(f) - bs + cpos;
       break;
       }
     else
       {
       fseeko( f, -ps, SEEK_CUR );
       }
     if ( bs < BUFSIZE ) break;
     }
   delete np;
   delete buff;
   return pos;
};

long file_pattern_search( const char *p, int ps, const char* fn, const char* opt,
                          int (*mem_search)( const char *p, int ps,
                                             const char *d, int ds ) )
{
  FILE *f = fopen( fn, "r" );
  if ( ! f ) return -1;
  int res = file_pattern_search( p, ps, f, opt, mem_search );
  fclose( f );
  return res;
};

/*****************************************************************************
**
** Grep -- regular expression search
**
*****************************************************************************/

/* FGrep -- regular expression search (I know `G' here stands for <nothing>:)) */

long file_grep( const char *re_string, const char* file_name, int nocase, off_t spos )
{
  FILE *f = fopen( file_name, "rb" );
  if (!f) return -1;
  long pos = file_grep( re_string, f, nocase, spos );
  fclose(f);
  return pos;
}

int file_grep_max_line = MAX_GREP_LINE;
int file_grep_lines_read = 0;
long file_grep( const char *re_string, FILE* f, int nocase, off_t spos )
{
  if ( strlen(re_string) >= (size_t)file_grep_max_line ) return -2; // just in case, and for now...

  char newpat[MAX_PATTERN+1];
  strcpy( newpat, re_string );
  if ( nocase ) str_up( newpat );

  VRegexp re;
  if ( ! re.comp( newpat ) ) return -2;
  char *line = (char*)malloc( file_grep_max_line+1 );

  off_t opos = ftello( f );
  ASSERT( spos >= -1 );
  if (spos != -1) fseeko( f, spos, SEEK_SET );
  off_t cpos = ftello( f );

  file_grep_lines_read = 0;
  int found = 0;
  while( fgets( line, file_grep_max_line, f ) )
    {
    if ( nocase ) str_up( line );
    if ( re.m( line ) )
      {
      found = 1;
      break;
      }
    cpos = ftello( f );
    file_grep_lines_read++;
    if (feof(f)) break;
    }

  fseeko( f, opos, SEEK_SET );
  if (found)
    cpos += ( re.sub_sp( 0 ) );

  free(line);
  file_grep_max_line = MAX_GREP_LINE;
  return found ? cpos : -1;
}

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

long file_string_search( const char *p, const char* fn, const char* opt )
{
  FILE *f = fopen( fn, "rb" );
  if (!f) return -1;
  long pos = file_string_search( p, f, opt );
  fclose(f);
  return pos;
}

long file_string_search( const char *p, FILE *f, const char* opt )
{
  int ps = strlen(p);
  ASSERT( ps < MAX_PATTERN );

  int nocase = str_find( opt, 'i' ) > -1;

  long pos = -1;

  if( str_find( opt, 'r' ) > -1 )
    {
    pos = file_grep( p, f, 0, -1 );
    } else
  if( str_find( opt, 'h' ) > -1 )
    {
  	char new_p[MAX_PATTERN+1];
  	int pl = hex_string_to_pattern( p, new_p );
  	if (pl > 0)
  	  pos = file_pattern_search( new_p, pl, f, nocase ? "i" : "" );
    }
  else
    {
    pos = file_pattern_search( p, strlen(p), f, nocase ? "i" : "" );
    }

  return pos;
};

int mem_string_search( const char *p, const char* d, const char* opt )
{
  int ps = strlen(p);
  ASSERT( ps < MAX_PATTERN );

  int nocase = str_find( opt, 'i' ) > -1;

  long pos = -1;

  if( str_find( opt, 'r' ) > -1 )
    {
    VRegexp re;
    if ( ! re.comp( p ) ) return -1;
    if ( ! re.m( d ) ) return -1;
    pos = re.sub_sp( 0 );
    } else
  if( str_find( opt, 'h' ) > -1 )
    {
  	char new_p[MAX_PATTERN+1];
  	int pl = hex_string_to_pattern( p, new_p );
  	if (pl > 0)
  	  if ( nocase )
        pos = mem_quick_search_nc( new_p, pl, d, strlen(d) );
      else
        pos = mem_quick_search( new_p, pl, d, strlen(d) );
    }
  else
    {
    if ( nocase )
      pos = mem_quick_search_nc( p, ps, d, strlen(d) );
    else
      pos = mem_quick_search( p, ps, d, strlen(d) );
    }

  return pos;
};

/***************************************************************************
**
** VREGEXP
**
****************************************************************************/

  VRegexp::VRegexp()
  {
    re = NULL;
    pe = NULL;
    rc = 0;
    lp = NULL;

    pt = NULL;
    pl = 0;
  };

  VRegexp::VRegexp( const char* rs, const char* opt )
  {
    re = NULL;
    pe = NULL;
    rc = 0;
    lp = NULL;

    pt = NULL;
    pl = 0;

    comp( rs, opt );
  };

  VRegexp::~VRegexp()
  {
    if ( re ) pcre_free( re );
    if ( pt ) delete pt;
  };

  int VRegexp::get_options( const char* opt )
  {
    opt_mode = MODE_REGEXP;
    opt_nocase = 0;
    if ( ! opt    ) return 0;
    if ( ! opt[0] ) return 0;
    int options = 0;
    int sl = strlen( opt );
    int z;
    for( z = 0; z < sl; z++ )
      {
      switch( opt[z] )
        {
        case 'i': options |= PCRE_CASELESS; opt_nocase = 1; break;
        case 'm': options |= PCRE_MULTILINE; break;
        case 's': options |= PCRE_DOTALL; break;
        case 'x': options |= PCRE_EXTENDED; break;
        case 'f': opt_mode = MODE_FIND; break;
        case 'h': opt_mode = MODE_HEX; break;
        case 'r': opt_mode = MODE_REGEXP; break;
        default: errstr = "invalid option, allowed are: imsxfhr"; return -1;
        }
      }
    return options;
  };

  int VRegexp::comp( const char* pattern, const char *opt )
  {
    if ( re ) pcre_free( re );
    if ( pt ) delete pt;
    re = NULL;
    pt = NULL;
    pl = 0;

    int options = get_options( opt );
    if( options == -1 ) return 0;

    if ( opt_mode == MODE_REGEXP )
      {
      const char *error;
      int erroffset;
      re = pcre_compile( pattern, options, &error, &erroffset, NULL );

      if ( re )
        {
        errstr = "";
        return 1;
        }
      else
        {
        errstr = error;
        return 0;
        }
      }
    else
      {
      pl = strlen( pattern );
      pt = new char[pl+1];
      if ( opt_mode == MODE_HEX )
        pl = hex_string_to_pattern( pattern, pt );
      else
        strcpy( pt, pattern );
      pt[pl] = 0;
      return pl;
      }
  };

  int VRegexp::study()
  {
    return 1;
  };

  int VRegexp::ok()
  {
    if ( opt_mode == MODE_REGEXP )
      return re != NULL;
    else
      return pt != NULL && pl > 0;
  }

  int VRegexp::m( const char* line )
  {
    if ( ! ok() )
      {
      errstr = "no pattern compiled";
      return 0;
      }
    if ( ! line )
      {
      errstr = "no data to search into";
      return 0;
      }
    errstr = "";
    lp = line;
    if ( opt_mode == MODE_REGEXP )
      {
      rc = pcre_exec( re, pe, lp, strlen( lp ), 0, 0, sp, VREGEXP_MAX_SUBS*3 );
      ASSERT( rc >= -1 && rc != 0 );
      if ( rc > VREGEXP_MAX_SUBS ) rc = VREGEXP_MAX_SUBS;
      if ( rc < 1 ) rc = 0; // fail-safe, should throw exception above in debug mode
      return rc;
      }
    else
      {
      if ( opt_nocase )
        pos = mem_quick_search_nc( pt, pl, line, strlen(lp) );
      else
        pos = mem_quick_search( pt, pl, line, strlen(lp) );
      return pos >= 0;
      }
  };

  int VRegexp::m(  const char* line, const char* pattern, const char *opt )
  {
    comp( pattern, opt );
    return m( line );
  };

  VString VRegexp::sub( int n )
  {
    VString substr;
    if ( ! ok() ) return substr;
    if ( ! lp ) return substr;
    if ( opt_mode == MODE_REGEXP )
      {
      if ( n < 0 || n >= rc ) return substr;

      int s = sp[n*2];
      int e = sp[n*2+1];
      int l = e - s;
      substr.setn( lp + s, l );
      }
    else
      {
      if ( n != 0 ) return substr;
      substr.setn( lp + pos, pl );
      }
    return substr;
  };

  int VRegexp::sub_sp( int n )
  {
    if ( opt_mode == MODE_REGEXP )
      {
      if ( n < 0 || n >= rc ) return -1;
      return sp[n*2];
      }
    else
      {
      if ( n != 0 ) return -1;
      return pos;
      }
  };

  int VRegexp::sub_ep( int n )
  {
    if ( opt_mode == MODE_REGEXP )
      {
      if ( n < 0 || n >= rc ) return -1;
      return sp[n*2+1];
      }
    else
      {
      if ( n != 0 ) return -1;
      return pos+pl;
      }
  };

/***************************************************************************
**
** VCHARSET
**
****************************************************************************/

  VCharSet::VCharSet()
    {
    _data = NULL;
    _size = 0;
    };

  VCharSet::~VCharSet()
    {
    _data = NULL;
    _size = 0;
    };

  void VCharSet::resize( int new_size )
  {
    if ( new_size < 1 )
      {
      if ( _data ) delete [] _data;
      _data = NULL;
      _size = 0;
      return;
      }
    // calc required mem size in unsigned chars (bytes?)
    new_size = new_size / sizeof(unsigned char) + (new_size % sizeof(unsigned char) != 0);
    // pad mem size in blocks of VCHARSET_BLOCK_SIZE
    new_size = new_size / VCHARSET_BLOCK_SIZE + (new_size % VCHARSET_BLOCK_SIZE != 0);
    // calc size back to unsigned chars (bytes?)
    new_size *= VCHARSET_BLOCK_SIZE;
    unsigned char *new_data = new unsigned char[ new_size ];
    memset( new_data, 0, new_size );
    if ( _data )
      {
      memcpy( new_data, _data, _size < new_size ? _size : new_size );
      delete [] _data;
      }
    _data = new_data;
    _size = new_size;
  };


  void VCharSet::push( int n, int val )
  {
    if ( n < 0 ) return;
    if ( n >= _size * (int)sizeof(unsigned char) ) resize( n + 1 );
    if ( val )
      _data[ n / sizeof(unsigned char) ] |= 1 << (n % sizeof(unsigned char));
    else
      _data[ n / sizeof(unsigned char) ] &= ~(1 << (n % sizeof(unsigned char)));
  };

  void VCharSet::undef( int n )
  {
    push( n, 0 );
  };

  void VCharSet::undef()
  {
    resize( 0 );
  }

  int VCharSet::in( int n )
  {
    if ( n < 0 || n >= _size * (int)sizeof(unsigned char) ) return 0;
    return ( _data[ n / sizeof(unsigned char) ] & ( 1 << ( n % sizeof(unsigned char) ) ) ) != 0;
  };


/*
  int VCharSet::get( int pn )
    {
      if ( pn < 0 || pn >= size ) return 0;
      return (data[pn / 8] & (1 << (pn % 8))) != 0;
    };

  void VCharSet::set_range1( int start, int end ) // set range
  {
    char s = ( start < end ) ? start : end;
    char e = ( start > end ) ? start : end;
    for( int z = s; z <= e; z++) set1( z );
  };

  void VCharSet::set_range0( int start, int end ) // set range
  {
    char s = ( start < end ) ? start : end;
    char e = ( start > end ) ? start : end;
    for( int z = s; z <= e; z++) set0( z );
  };

  void VCharSet::set_str1( const char* str )
  {
    int sl = strlen( str );
    for( int z = 0; z < sl; z++ )
      set1( str[z] );
  };

  void VCharSet::set_str0( const char* str )
  {
    int sl = strlen( str );
    for( int z = 0; z < sl; z++ )
      set0( str[z] );
  };

  int VCharSet::in( const char *str )
  {
    int sl = strlen( str );
    for( int z = 0; z < sl; z++ )
      if ( !in( str[z] ) ) return 0;
    return 1;
  };

  int VCharSet::resize( int p_size )
    {
      ASSERT( p_size > 0 );
      int new_size = p_size;
      int new_datasize = p_size / 8 + (p_size % 8 != 0);
      char *new_data = (char*)malloc( new_datasize );
      if (new_data == NULL) return CE_MEM;
      memset( new_data, 0, new_datasize );
      if (data)
        {
        memcpy( new_data, data, datasize < new_datasize ? datasize : new_datasize );
        free( data );
        data = NULL;
        }
      data = new_data;
      size = new_size;
      datasize = new_datasize;
      return CE_OK;
    }

  VCharSet& VCharSet::operator  = ( const VCharSet &b1 )
  {
    resize( b1.size );
    memcpy( data, b1.data, datasize );
    return *this;
  };

  VCharSet& VCharSet::operator &= ( const VCharSet &b1 )
  {
    int z;
    for(z = 0; z < (datasize < b1.datasize ? datasize : b1.datasize ); z++)
      data[z] &= b1.data[z];
    return *this;
  };

  VCharSet& VCharSet::operator |= ( const VCharSet &b1 )
  {
    int z;
    for(z = 0; z < (datasize < b1.datasize ? datasize : b1.datasize ); z++)
      data[z] |= b1.data[z];
    return *this;
  };

  VCharSet VCharSet::operator ~ ()
  {
    VCharSet b;
    b = *this;
    int z;
    for(z = 0; z < b.datasize; z++)
      b.data[z] = ~b.data[z];
    return b;
  };

  VCharSet operator & ( const VCharSet &b1, const VCharSet &b2 )
  {
    VCharSet b;
    b = b1;
    b &= b2;
    return b;
  };

  VCharSet operator | ( const VCharSet &b1, const VCharSet &b2 )
  {
    VCharSet b;
    b = b1;
    b |= b2;
    return b;
  };
*/

/***************************************************************************
**
** UTILITIES
**
****************************************************************************/

  // split `source' with `regexp_str' regexp
  VArray str_split( const char* regexp_str, const char* source, int maxcount )
  {
    VArray arr;
    VRegexp re;
    int z = re.comp( regexp_str );
    ASSERT( z );
    if ( ! z ) return arr;

    const char* ps = source;

    while( ps && ps[0] && re.m( ps ) )
      {
      if ( maxcount != -1 )
        {
        maxcount--;
        if ( maxcount == 0 ) break;
        }
      VString s;
      s.setn( ps, re.sub_sp( 0 ) );
      arr.push( s );
      ps += re.sub_ep( 0 );
      }
    if ( ps && ps[0] )
      arr.push( ps );
    return arr;
  };

  // split `source' with exact string `delimiter_str'
  VArray str_split_simple( const char* delimiter_str, const char* source, int maxcount )
  {
    VArray arr;
    const char* ps = source;
    const char* fs;

    int rl = strlen( delimiter_str );

    VString s;
    while( (fs = strstr( ps, delimiter_str )) )
      {
      if ( maxcount != -1 )
        {
        maxcount--;
        if ( maxcount == 0 ) break;
        }
      int l = fs - ps;
      s.setn( ps, l );
      arr.push( s );
      ps = (const char *)(ps + l + rl);
      }
    if ( ps && ps[0] )
      arr.push( ps );
    return arr;
  };

  // join array data to single string with `glue' string
  // returns the result string or store to optional `dest'
  VString str_join( VArray array, const char* glue )
  {
    VString str;
    for( int z = 0; z < array.count()-1; z++ )
      {
      str += array.get( z );
      str += glue;
      }
    str += array.get( array.count()-1 );
    return str;
  };

/***************************************************************************
**
** EOF
**
****************************************************************************/
