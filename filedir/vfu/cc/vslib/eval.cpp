/*
 *
 * (c) Vladi Belperchinov-Shabanski "Cade" <cade@biscom.net> 1998-2003
 *
 * SEE `README',`LICENSE' OR `COPYING' FILE FOR LICENSE AND OTHER DETAILS!
 *
 * $Id: eval.cpp,v 1.5 2003/01/21 19:56:35 cade Exp $
 *
 */

#include <math.h>
#include <vstring.h>
#include "eval.h"

/*

  This is *very* old code and I'm not sure if it works at all
  after the last rewrite :)

*/

int EvalResult;
double Eval( const char* a_exp )
{
  VString exp = a_exp;
  str_cut_spc( exp );
  
  int ps    = 0; // pos of the +/-/:/* signs
  int prior = 0; // priority flag
  int par   = 0; // brackets flag
  int z     = 0; // pos counter
  while ( z < str_len( exp ) )
   {
   switch ( exp[z] ) {
     case '(': par++; break;
     case ')': par--; break;
     case '+': if ((par == 0) && (prior < 20)) { prior = 20; ps = z; } break;
     case '-': if ((par == 0) && (prior < 20)) { prior = 20; ps = z; } break;
     case '*': if ((par == 0) && (prior < 10)) { prior = 10; ps = z; } break;
     case '/': if ((par == 0) && (prior < 10)) { prior = 10; ps = z; } break;
     case '%': if ((par == 0) && (prior < 10)) { prior = 10; ps = z; } break;
     }
   z++;
   }
  if (ps != 0) 
   {
   VString p1;
   VString p2;
   str_copy( p1, exp, 0, ps );
   str_copy( p1, exp, ps );
   
   double res = 0.0;
   switch (exp[ps]) {
     case '+': res = (Eval(p1)+Eval(p2)); break;
     case '-': res = (Eval(p1)-Eval(p2)); break;
     case '*': res = (Eval(p1)*Eval(p2)); break;
     case '/': res = (Eval(p1)/Eval(p2)); break;
     case '%': res = (fmod(Eval(p1),Eval(p2))); break;
     }
   return res;
   }
  else
   { // well ... constant/function/brackets
   int bp = str_find( exp, '(' );
   if ( bp >= 0 )
     if ( bp > 0 )
       { // function
       VString fname;
       str_copy( fname, exp, 0, bp );
       
       VString p1;
       str_copy( p1, exp, bp+1,  str_rfind( exp, ')' ) - bp - 1 );
       
       double res = 0.0;
       if (strcasecmp(fname, "sin") == 0)  {res  = sin(Eval(p1));} else
       if (strcasecmp(fname, "cos") == 0)  {res  = cos(Eval(p1));} else
       if (strcasecmp(fname, "tan") == 0)  {res  = sin(Eval(p1))/cos(Eval(p1));} else
       if (strcasecmp(fname, "atan") == 0) {res  = atan(Eval(p1));} else
       if (strcasecmp(fname, "asin") == 0) {res  = asin(Eval(p1));} else
       if (strcasecmp(fname, "acos") == 0) {res  = acos(Eval(p1));} else
       // degree/radians/grads conversions...
       if (strcasecmp(fname, "r2d") == 0) {res  = Eval(p1)*180/M_PI;} else
       if (strcasecmp(fname, "d2r") == 0) {res  = Eval(p1)*M_PI/180;} else
       if (strcasecmp(fname, "r2g") == 0) {res  = Eval(p1)*200/M_PI;} else
       if (strcasecmp(fname, "g2r") == 0) {res  = Eval(p1)*M_PI/200;} else
       if (strcasecmp(fname, "d2g") == 0) {res  = Eval(p1)*400/360;} else
       if (strcasecmp(fname, "g2d") == 0) {res  = Eval(p1)*360/400;} else
  
       if (strcasecmp(fname, "random") == 0) {res  = random() % long(Eval(p1));} else
       if (strcasecmp(fname, "abs") == 0)    {res  = fabs(Eval(p1));} else
       if (strcasecmp(fname, "int") == 0)    {res  = floor(Eval(p1)+0.5);} else
       if (strcasecmp(fname, "sqrt") == 0)   {res  = sqrt(Eval(p1));} else
       if (strcasecmp(fname, "exp") == 0)    {res  = ::exp(Eval(p1));} else
       if (strcasecmp(fname, "ln") == 0)     {res  = log(Eval(p1));} else
       if (strcasecmp(fname, "lg") == 0)     {res  = log10(Eval(p1));} else
  //       if (strcasecmp(fname, "") == 0) {} else
       EvalResult = 10;
       if (EvalResult == 10)
         return 0;
       else
         return res;
       }
     else
       { // brackets
       VString p1;
       str_copy( p1, exp, 1, str_len( exp ) - 2 );
       double res = Eval( p1 );
       return res;
       }
   else
     { // constant
     if ( strcasecmp( exp, "pi" ) == 0 ) { return M_PI; } else
     if ( strcasecmp( exp, "e" )  == 0 ) { return M_E;  } else
     return atof ( exp );
     }
   }
  //return 0;
}
