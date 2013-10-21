/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',LICENSE' OR COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: eval.h,v 1.3 2003/01/21 19:56:35 cade Exp $
 *
 */
 

#ifndef _EVAL_H_
#define _EVAL_H_

//
// this evaluates math expression with recursive parser etc.
// (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1996-1998
//

extern int EvalResult;
double Eval( const char* pExp );

#endif //_EVAL_H_
