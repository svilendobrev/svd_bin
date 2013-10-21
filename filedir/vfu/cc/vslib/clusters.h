/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',LICENSE' OR COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: clusters.h,v 1.5 2003/01/21 19:56:35 cade Exp $
 *
 */
/*
 *
 *  This is general purpose array classes.
 *  `CLUSTERS' name replaces boring `Arrays' name :)
 *  It really doesn't make much difference however...
 *
*/

#ifndef _CLUSTERS_H_
#define _CLUSTERS_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <assert.h>

#ifndef ASSERT
#define ASSERT assert
#endif

#ifndef int32
#define int32 int
#endif

// cluster errors
#define CE_OK    0   // ok -- no error
#define CE_MEM   1   // low memory
#define CE_OVR   128 // overflow
#define CE_ERR   255 // error

/****************************************************************************
**
** FREE-LIST cluster
**
****************************************************************************/
  
  class FLCluster
  {
    int32 es;      // element size
    int32 ds;      // data size
    int32 size;    // elements allocated
    int32 used;    // elements used == count
    int32 ff;      // first free element
    int32 growby;  // `grow by' elements
    char *data;    // actual data

    public:

    int base;
    int null;

    FLCluster();
    ~FLCluster();

    int create( int32 pcnt, int32 pgrow, int32 pes ); // pes=element size, initial count & `grow by'
    void done();

    int32 add( void* pe ); // insert element, return handle or -1
    int del( int32 pn ); // delete element (memset(`+') & mark it `free'), ret E_OK or error
    int get( int32 pn, void* pe ); // get element, return E_OK or error
    char* get( int32 pn ); // get element pointer or NULL if error

    int is_used( int32 pn ); // 1 if pn element is used

    void dump(); // only for debugging

    protected:
    int Realloc( int32 pn ); // expand/shrink data list, return CE_OK, or error

  };

/****************************************************************************
**
** BASE Cluster prototype
**
****************************************************************************/

class BaseCluster
  {
    protected:

    int es;
    int size;
    int cnt;
    int bsize;
    char *data;

    int status;

    void (*destructor_func)( void* );

    public:

    BaseCluster() { data = NULL; es = 0; size = 0; cnt = 0; bsize = 0; destructor_func = NULL; };
    virtual ~BaseCluster() { if (data) done(); };

    int create( int p_size, int p_bsize, int p_es );
    void done();

    void del( int pn );
    void delall();
    void free( int pn );
    void freeall();

    int count() { return cnt; };

    void shrink() { Realloc( cnt ); };

    void set_destructor( void (*dfunc)(void*) ) { destructor_func = dfunc; };

    protected:

    virtual void destroy_element( void* pe )
      { if ( destructor_func != NULL ) destructor_func( pe ); };
    int Realloc( int pn );

  };

/****************************************************************************
**
** DATA cluster
**
****************************************************************************/

class DCluster : public BaseCluster
  {
    public:
    int add( void* pe );
    int ins( int pn, void* pe );
    void put( int pn, void* pe );
    void get( int pn, void* pe );

    const void* operator [] ( int pn ) { ASSERT( pn >= 0 && pn < cnt  ); return data + (pn*es); };
  };

/****************************************************************************
**
** TEMPLATE DATA cluster
**
****************************************************************************/

template< class T >
class TDCluster : public DCluster
  {
    public:

    const T* operator [] ( int pn ) const { ASSERT( pn >= 0 && pn < cnt  ); return (T*)(data + (pn*es)); };
    T operator [] ( int pn ) { ASSERT( pn >= 0 && pn < cnt  ); return (*((T*)(data + (pn*es)))); };
  };

/****************************************************************************
**
** POINTER cluster
**
****************************************************************************/

class PCluster : public BaseCluster
  {
    public:
    int create( int p_size, int p_bsize )
      { return BaseCluster::create( p_size, p_bsize, sizeof(void*) ); };

    int add( void* pe );
    int ins( int pn, void* pe );
    void put( int pn, void* pe );
    void* get( int pn );

    void* operator [] ( int pn ) { ASSERT( pn >= 0 && pn < cnt  ); return ((void**)data)[pn]; };

    protected:
    virtual void destroy_element( void* pe )
      { if ( destructor_func != NULL ) destructor_func( ((void**)pe)[0] ); };
  };

/****************************************************************************
**
** TEMPLATE POINTER cluster
**
****************************************************************************/

template< class T >
class TPCluster : public PCluster
  {
    public:
    int create( int p_size, int p_bsize )
      { return BaseCluster::create( p_size, p_bsize, sizeof(void*) ); };

    T* get( int pn ) {};
    T* operator [] ( int pn ) { ASSERT( pn >= 0 && pn < cnt  ); return ((T**)data)[pn]; };

    protected:
    virtual void destroy_element( void* pe ) 
      { delete ((T**)pe)[0]; };
  };

/****************************************************************************
**
** TEMPLATE cluster
**
****************************************************************************/

template< class T >
class TCluster
  {
    int cnt;
    int size;
    int bsize;
    T   *data;

    public:

    TCluster() { data = NULL; cnt = 0; size = 0; bsize = 0; };
    ~TCluster() { if (data) done(); };

    void create( int p_size, int p_bsize ) { bsize = p_bsize; Realloc( p_size ); };
    void done() { if (data) delete [] data; data = NULL; cnt = 0; size = 0; bsize = 0; };

    long count() const { return cnt; }
    void Realloc( int pn )
      {
        if( pn == 0 )
          {
          if( data ) delete [] data;
          size = 0;
          cnt = 0;
          data = NULL;
          return;
          }

        T *newdata = new T[pn];

        int less =  pn < cnt ? pn : cnt;
        int z;
        for( z = 0; z < less; z++ )  newdata[z] = data[z];
        if( data )  delete [] data;

        cnt = less;
        size = pn;
        data   = newdata;
      };
    void add( T &e )
      {
      if ( cnt == size ) Realloc( size + bsize );
      data[cnt] = e;
      cnt++;
      };
    T& operator [] ( int pn )
      { ASSERT( pn >= 0 && pn < cnt  ); return data[pn]; };
    const T& operator [] ( int pn ) const
      { ASSERT( pn >= 0 && pn < cnt  ); return data[pn]; };
};

/****************************************************************************
**
** BIT-SET set
**
****************************************************************************/

class BSet
  {
    public:

    int size;  // size (in bits)
    int datasize; // size (in bytes)
    char *data;

    BSet();
    BSet( const char* str );
    ~BSet();

    void set1( int pn );
    void set0( int pn );
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

    BSet& operator  = ( const BSet &b1 );
    BSet& operator &= ( const BSet &b1 );
    BSet& operator |= ( const BSet &b1 );
    BSet  operator  ~ ();

    friend BSet operator & ( const BSet &b1, const BSet &b2 );
    friend BSet operator | ( const BSet &b1, const BSet &b2 );
  };

#endif //_CLUSTERS_H_
