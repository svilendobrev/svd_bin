/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: target.h,v 1.6 2004/12/29 02:44:21 cade Exp $
 *
 */

#ifndef _TARGET_H_
#define _TARGET_H_

#define _TARGET_UNKNOWN_

/****************************************** define target OS ***************/

#ifdef _TARGET_UNKNOWN_
  #if defined(DJGPP) || defined(_TARGET_DJGPP_)
  #define _TARGET_GO32_
  #define _TARGET_DJGPP_
  #define _TARGET_DOS_
  #define _TARGET_DESCRIPTION_	"DOS/DJGPP"
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifdef _TARGET_UNKNOWN_
  #if defined(__linux__) || defined(__Linux__) || defined(_TARGET_LINUX_)
  #define _TARGET_LINUX_
  #define _TARGET_UNIX_
  #define _TARGET_DESCRIPTION_	"UNIX/LINUX"
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifdef _TARGET_UNKNOWN_
  #if defined(__NetBSD__) || defined(_TARGET_NETBSD_)
  #define _TARGET_NETBSD_
  #define _TARGET_UNIX_
  #define _TARGET_DESCRIPTION_	"UNIX/NETBSD"
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifdef _TARGET_UNKNOWN_
  #if defined(WIN32) || defined(_TARGET_WIN32_)
  #define _TARGET_WIN32_
  #define _TARGET_UNIX_
  #define _TARGET_DESCRIPTION_	"DOS/WIN32" // sorry :)
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifdef _TARGET_UNKNOWN_
  #if defined(MACOSX) || defined(__APPLE__)
  #define _TARGET_MACOSX_
  #define _TARGET_UNIX_
  #define _TARGET_DESCRIPTION_	"UNIX/MACOSX"
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifdef _TARGET_UNKNOWN_
  #if defined(__GNU__) || defined(_TARGET_GNU_)
  #define _TARGET_GNU_
  #define _TARGET_UNIX_
  #define _TARGET_DESCRIPTION_	"GNU"
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifdef _TARGET_UNKNOWN_
  #if ((defined(__unix__) || defined(unix)) && !defined(USG)) || defined(_TARGET_UNIX_)
  #define _TARGET_UNIX_
  #define _TARGET_DESCRIPTION_	"UNIX"
  #undef  _TARGET_UNKNOWN_
  #endif
#endif

#ifndef _TARGET_DESCRIPTION_
  #define _TARGET_DESCRIPTION_	"UNKNOWN/UNKNOWN"
#endif

/****************************************** go error unless known :/ *******/

#ifdef _TARGET_UNKNOWN_
  #error "Unknown target please define one manually!"
  #error "Supported are _TARGET_LINUX_, _TARGET_DJGPP_, _TARGET_NETBSD_, _TARGET_GNU_, _TARGET_UNIX_"
  #error "Read README or COMPILE file(s) for details"
#endif

/******************************************************************* eof ***/
#endif //_TARGET_H_


