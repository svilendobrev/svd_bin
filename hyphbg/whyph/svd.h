
#define MAXW 255  // max input line length & max ASCII

enum { OK=0, ERR };

typedef int bool;
typedef unsigned char chr;
typedef char * cp;
typedef char far *cf;
typedef unsigned int uint;
typedef unsigned long int ulint;
#ifdef _MSC_VER
typedef char huge * chuge;
#else
typedef char far * chuge;
#endif

#ifndef min
#define min(xa,xb) (((xa)<(xb)) ? (xa) : (xb))
#endif

enum { NOINERR=1, NODOERR, inOPENERR, outOPENERR, doOPENERR,
       inERR, outERR, doERR, NOMEM, NOMET, SORRY };

#if defined(__STDIO_H) || defined(_STDIO_DEFINED) || defined(_STDIO_H_INCLUDED)
typedef FILE *fl;

#ifndef MAINEXE
#define err(fn) { perror(fn); return ERR; }
#define HELPHIM { puts(HelpHim); return ERR; }

void nl() { char n = 0; puts(&n); }
void pn(n) int n; { printf("%6d",n); }
void pl(n) long n; { printf("%10ld",n); }

#else


fl inf, outf;
cp cantopen = "Can't open             ";
cp inatr = "rb", outatr = "wb";
extern cp infn, outfn, fdon;
extern cp HelpHim;

void free_all_buffs();

/*
void px(w,n) cp w; int n; { int i;
   for (i=0; i<n; i++) putc(w[i], stdout); putc(10,stdout); }
*/

#define ps(ssssss) puts(ssssss)
void nl() { char n = 0; puts(&n); }
void pn(n) int n; { printf("%6d",n); }
void pl(n) long n; { printf("%10ld",n); }

void err(x,nn) int x,nn; {
cp ms= cantopen, z=0;
  switch (x) {
     case 0: goto gohome;
     case NOINERR: ms = HelpHim; break;
     case inOPENERR:  strcpy(ms+11,infn);  break;
     case outOPENERR: strcpy(ms+11,outfn); break;
     case doOPENERR:  strcpy(ms+11,fdon);  break;
     case inERR:  ms = "inFile error, offset"; z++; nn=ftell(inf); break;
     case outERR: ms = "outFile error, offset"; z++; nn=ftell(outf); break;
     case doERR: ms = "What-To-Do-File error, line"; z++; break;
     case NOMEM: ms = "Not enough memory. Min 200K required"; break;
     default: ms = "UNKNOWN ERROR !";
    } /* endswitch */
   printf("\n\rError: %s",ms);
   if (z) printf(": %d",nn);
   printf("\n\r");
gohome:
   free_all_buffs();
   fcloseall();
   exit(0);
 }
#define err(_x) err(_x,0)

#endif

#endif
