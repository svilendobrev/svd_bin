/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: vsuti.h,v 1.9 2004/04/04 23:18:20 cade Exp $
 *
 */

#ifndef _VSUTI_H_
#define _VSUTI_H_

#include <sys/stat.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dirent.h>

#include "target.h"

#ifdef _TARGET_UNIX_
#include <pwd.h>
#include <sys/types.h>
#include <sys/param.h>
#endif

#include <assert.h>
#ifndef ASSERT
#define ASSERT assert
#endif

#include "vstring.h"

/*###########################################################################*/
/* MISC defines */

/* max filename length */
#ifndef MAX_PATH
#define MAX_PATH	3*512
#endif

/*###########################################################################*/
/* CRC functions */

typedef unsigned long int crc32_t;

#define CRC32NULL (0xffffffff)

/* should start with `0xffffffff' for `crc' and result is crc = ~crc; */
crc32_t update_crc32( const unsigned char octet, const crc32_t crc );

crc32_t mem_crc32( const void* buff, int size );
crc32_t str_crc32( const char *s );
crc32_t file_crc32( FILE *f, long buffsize = 256*1024  );
crc32_t file_crc32( const char *fname, long buffsize = 256*1024  );

/*###########################################################################*/

typedef unsigned long int adler32_t;

adler32_t adler32(adler32_t adler, const char *buf, unsigned int len);

adler32_t mem_adler32( const void* buff, int size );
adler32_t str_adler32( const char *s );
adler32_t file_adler32( FILE *f, long buffsize = 256*1024  );
adler32_t file_adler32( const char *fname, long buffsize = 256*1024  );

/*###########################################################################*/
/* FILE functions */

off_t file_size( const char *fname );
off_t file_size( FILE *f );

int file_load( FILE *f, void *buff, int size = -1 );
int file_save( FILE *f, void *buff, int size = -1 );
int file_load( const char* fname, void *buff, int size = -1 );
int file_save( const char* fname, void *buff, int size = -1 );

int file_load_crc32( const char* fname, void *buff, int size );
int file_save_crc32( const char* fname, void *buff, int size );

int file_is_link( const char* fname );
int file_is_dir( const char* fname );
int file_is_dir( struct stat st );
int file_exists( const char* fname );

/*****************************************************************************
**
** tilde_expand() expands ~/path and ~name/path to real pathname.
** it uses $HOME environment variable for ~ substitution.
**
*****************************************************************************/

VString tilde_expand( const char* a_path );

/*****************************************************************************
**
** make_path() create new directory including non-existing path entries.
** It can create /a/b/c/d/e/ without existing of `/a/' for example.
** return 0 for success
**
*****************************************************************************/

int make_path( const char *s,
        long mode = S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH );

/*****************************************************************************
**
** expand_path() resolves symlinks etc.
**
*****************************************************************************/

char* expand_path( const char *src, char *dest );
VString expand_path( const char* src );

/*****************************************************************************
**
** dosstat() is fast stat() designed for DOS FAT filesystems under DJGPP.
**
*****************************************************************************/

#ifdef _TARGET_GO32_
#include <dirent.h>
#include <dir.h>
int dosstat( DIR *dir, struct stat *stbuf );
#endif

/*****************************************************************************
**
** ftwalk() traverses directory tree and calls func() for every entri it
** encounters. It supports DOS FAT filesystems under DJGPP.
**
*****************************************************************************/

#define FTWALK_F        1 /* file (regular) */
#define FTWALK_D        2 /* dir */
#define FTWALK_DX       3 /* call on exit directory */
#define FTWALK_NS       4 /* stat() failed */

/* func() should return 0 for ok, -1 */
int ftwalk( const char *origin_dir,
            int (*func)( const char* origin,    /* origin path */
                         const char* fname,     /* full file name */
                         const struct stat* st, /* stat struture or NULL */
                         int is_link,           /* 1 if link */
                         int flag ),
            int level = -1 );

/*****************************************************************************
**
** get_rc_directory() return application rc directory (and possibly create it)
** returned dir is $HOME/.dir_prefix or $HOME/$RC_PREFIX/dir_prefix depending
** on $RC_PREFIX existence.
**
*****************************************************************************/

VString get_rc_directory( const char* dir_prefix );

/*****************************************************************************
**
** EOF
**
*****************************************************************************/
#endif /* _VUTILS_H_ */


