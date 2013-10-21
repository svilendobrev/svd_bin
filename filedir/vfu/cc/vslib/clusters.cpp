/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: clusters.cpp,v 1.5 2003/01/21 19:56:35 cade Exp $
 *
 */

#include <stdlib.h>
#include <string.h>
#include "clusters.h"

#define RETURN(n) { return status = n; }

/****************************************************************************
**
** FREE-LIST cluster
**
****************************************************************************/

#define FL_EF(n) (((int32*)(data+(n)*es))[0]) // element `free' field
#define FL_ED(n) ((char*)(data+(n)*es+sizeof(int32))) // element `data' field

#define E_BUSY (-2)
#define E_NULL (-1)
#define E_FREE ( 0)


FLCluster::FLCluster()
{
  base = 0;
  null = -1;

  data = NULL;
  size = 0;
  used = 0;
  ff   = E_NULL;
}

void FLCluster::done()
{
  ASSERT( data );
  if (data) ::free( data );
}

FLCluster::~FLCluster()
{
  done();
}

int FLCluster::create( int32 pcnt, int32 pgrow, int32 pes )
{
  ASSERT( pes > 0 );
  ASSERT( pcnt > -1 );
  ASSERT( pgrow > -1 );
  ASSERT( !(pcnt == 0 && pgrow == 0 ) );

  es = pes + sizeof(int32);
  ds = pes;
  size = 0;
  used = 0;
  growby = pgrow;
  ff   = E_NULL;
  data = NULL;
  return Realloc( pcnt );
}

int32 FLCluster::add( void* pe ) // insert element
{
  ASSERT( pe );
//  if (ff == E_NULL) return -1;
  if (ff == E_NULL)
    {
    int32 res = Realloc( size + growby );
    if (res != CE_OK) return null;
    }

  int32 ret = ff;
  ff = FL_EF(ret);

  ASSERT( FL_EF(ret) != E_BUSY );
  FL_EF(ret) = E_BUSY;

  memcpy( FL_ED(ret), pe, ds );

  return ret + base;
}

int FLCluster::get( int32 pn, void* pe ) // get element
{
  pn -= base;

  ASSERT( pn >= 0 && pn < size );
  ASSERT( pe );
  ASSERT( FL_EF(pn) == E_BUSY );

  memcpy( pe, FL_ED(pn), ds );

  return CE_OK;
}

char* FLCluster::get( int32 pn ) // get element pointer or NULL if error
{
  pn -= base;

  ASSERT( pn >= 0 && pn < size );
  ASSERT( FL_EF(pn) == E_BUSY );

  return (char*)(FL_ED(pn));
}

int FLCluster::del( int32 pn ) // get element
{
  pn -= base;

  ASSERT( pn >= 0 && pn < size );
  ASSERT( FL_EF(pn) == E_BUSY );

  FL_EF(pn) = ff;
  ff = pn;

  return CE_OK;
}

int FLCluster::is_used( int32 pn ) // 1 if pn element is used
{
  return ( FL_EF(pn - base) == E_BUSY );
}

int FLCluster::Realloc( int32 pn ) // expand/shrink data list
{
  pn -= base;

  ASSERT( pn >= size );
  if ( pn == size ) return CE_OK;

  char *newdata = (char*)realloc( data, pn*es );
  if (!newdata) return CE_MEM;
  data = newdata;
  memset( data + size*es, 0, (pn - size)*es );

  int32 z;
  int32 base = size > 0;
  for(z = size+base; z < pn; z++) FL_EF(z) = z - 1;
  FL_EF(size) = ff;
  ff = pn - 1;
  size = pn;

  return CE_OK;
}

void FLCluster::dump()
{
  int32 z;
  printf("size: %d, ff: %d, used: %d\n", size, ff, used);
  for(z = 0; z < size; z++)
    {
    printf("%2d: nextfree: %2d\n", z, FL_EF(z));
    }
}

/****************************************************************************
**
** BASE Cluster prototype
**
****************************************************************************/

  int BaseCluster::create( int p_size, int p_bsize, int p_es )
  {
    cnt = 0;
    es = p_es;
    // size = p_size; this should be set by Realloc
    size = 0;
    bsize = p_bsize;
    RETURN(Realloc( p_size ));
  };

  void BaseCluster::done()
  {
    freeall();
    cnt = 0;
    es = 0;
    bsize = 0;
    if (data) ::free(data);
    data = NULL;
  };

  void BaseCluster::del( int pn )
  {
    ASSERT( pn >= 0 && pn < cnt );
    if (pn < cnt - 1)
      memmove( data + ( pn )*es, data + ( pn + 1 )*es, ( cnt - pn )*es );
    cnt--;
  };

  void BaseCluster::delall()
  {
    int z = cnt;
    while(z)
      del((z--) - 1);
  };

  void BaseCluster::free( int pn )
  {
    ASSERT( pn >= 0 && pn < cnt );
    destroy_element( (void*)(data + (pn)*es) );
    del( pn );
  };

  void BaseCluster::freeall()
  {
    int z = cnt;
    while(z)
      free((z--) - 1);
  }

  int BaseCluster::Realloc( int pn )
  {
    if ( pn == size ) RETURN(CE_OK);
    char* newdata = (char*)malloc( pn*es );
    if (newdata == NULL) RETURN(CE_MEM);
    #ifdef DEBUG
    memset( newdata, '+', pn*es );
    #endif
    if (newdata && data) memcpy( newdata, data, (( pn < size ) ? pn : size)*es );
    if (data) ::free(data);
    data = newdata;
    size = pn;
    RETURN(CE_OK);
  }

/****************************************************************************
**
** DATA cluster
**
****************************************************************************/
    
  int DCluster::add( void* pe )
  {
    RETURN(ins( cnt, pe ));
  };

  int DCluster::ins( int pn, void* pe )
  {
    int res = 0;
    if ( cnt == size )
      if ( (res = Realloc( size + bsize )) != 0 ) RETURN(res);
    if (pn < cnt)
      memmove( data + (pn+1)*es, data + (pn)*es, (cnt - pn)*es );
    memcpy( data + (pn*es), pe, es );
    cnt++;
    RETURN(CE_OK);
  };

  void DCluster::put( int pn, void* pe )
  {
    ASSERT( pn >= 0 && pn < cnt );
    memcpy( data + pn*es, pe, es );
  };

  void DCluster::get( int pn, void* pe )
  {
    ASSERT( pn >= 0 && pn < cnt );
    memcpy( pe, data + pn*es, es );
  };

/****************************************************************************
**
** POINTER cluster
**
****************************************************************************/

    int PCluster::add( void* pe )
    {
      RETURN(ins( cnt, pe ));
    };

    int PCluster::ins( int pn, void* pe )
    {
      int res = 0;
      if ( cnt == size )
        if ( (res = Realloc( size + bsize )) != 0 ) RETURN(res);
      if (pn < cnt)
        memmove( data + (pn+1)*es, data + (pn)*es, (cnt - pn)*es );
     ((void**)data)[pn] = pe;
      cnt++;
      RETURN(CE_OK);
    };

    void PCluster::put( int pn, void* pe )
    {
      ASSERT( pn >= 0 && pn < cnt );
     ((void**)data)[pn] = pe;
    };

    void* PCluster::get( int pn )
    {
      ASSERT( pn >= 0 && pn < cnt );
      return ((void**)data)[pn];
    };

/****************************************************************************
**
** BIT-SET cluster
**
****************************************************************************/
    
    BSet::BSet() 
      { 
      data = NULL; 
      size = 0; 
      datasize = 0; 
      resize( 256 );
      };

    BSet::BSet( const char* str ) 
      { 
      data = NULL; 
      size = 0; 
      datasize = 0; 
      resize( 256 );
      set_str1( str );
      };
      
    BSet::~BSet() 
      { 
      if( data ) free( data );
      };

    void BSet::set1( int pn )
      {
        if ( pn < 0 ) return;
        if ( pn >= size ) resize( pn + 1 );
        data[pn / 8] |= 1 << (pn % 8);
      };

    void BSet::set0( int pn )
      {
        if ( pn < 0 ) return;
        if ( pn >= size ) resize( pn + 1 );
        data[pn / 8] &= ~(1 << (pn % 8));
      };

    int BSet::get( int pn )
      {
        if ( pn < 0 || pn >= size ) return 0;
        return (data[pn / 8] & (1 << (pn % 8))) != 0;
      };

    void BSet::set_range1( int start, int end ) // set range
    {
      char s = ( start < end ) ? start : end;
      char e = ( start > end ) ? start : end;
      for( int z = s; z <= e; z++) set1( z );
    };

    void BSet::set_range0( int start, int end ) // set range
    {
      char s = ( start < end ) ? start : end;
      char e = ( start > end ) ? start : end;
      for( int z = s; z <= e; z++) set0( z );
    };

    void BSet::set_str1( const char* str )
    {
      int sl = strlen( str );
      for( int z = 0; z < sl; z++ )
        set1( str[z] );
    };

    void BSet::set_str0( const char* str )
    {
      int sl = strlen( str );
      for( int z = 0; z < sl; z++ )
        set0( str[z] );
    };

    int BSet::in( const char *str )
    {
      int sl = strlen( str );
      for( int z = 0; z < sl; z++ )
        if ( !in( str[z] ) ) return 0;
      return 1;  
    };

    int BSet::resize( int p_size )
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

    BSet& BSet::operator  = ( const BSet &b1 )
    {
      resize( b1.size );
      memcpy( data, b1.data, datasize );
      return *this;
    };

    BSet& BSet::operator &= ( const BSet &b1 )
    {
      int z;
      for(z = 0; z < (datasize < b1.datasize ? datasize : b1.datasize ); z++)
        data[z] &= b1.data[z];
      return *this;
    };

    BSet& BSet::operator |= ( const BSet &b1 )
    {
      int z;
      for(z = 0; z < (datasize < b1.datasize ? datasize : b1.datasize ); z++)
        data[z] |= b1.data[z];
      return *this;
    };

    BSet BSet::operator ~ ()
    {
      BSet b;
      b = *this;
      int z;
      for(z = 0; z < b.datasize; z++)
        b.data[z] = ~b.data[z];
      return b;
    };

    BSet operator & ( const BSet &b1, const BSet &b2 )
    {
      BSet b;
      b = b1;
      b &= b2;
      return b;
    };

    BSet operator | ( const BSet &b1, const BSet &b2 )
    {
      BSet b;
      b = b1;
      b |= b2;
      return b;
    };
    
// eof
