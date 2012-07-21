#include <stdio.h>
#include <stdlib.h>
#define PR_STR(x)  fprintf(f,"%s\n",x)      //"%0x : "

#ifdef ENVARG   //unixes?
# define ENVasARG   , char** env_in
# define ENVARR     env_in
#else
# define ENVasARG
# ifdef __ZTC__
#  ifdef M_UNIX
#   define ENVARR _environ
#  else
#   define ENVSTR _envptr
#  endif
# else
#  define ENVARR  environ
# endif
#endif

void main(int ac, char**av  ENVasARG ) {
#ifdef ENVARR
 const char ** env = ENVARR;
#else
 const char * env = ENVSTR;
#endif

#ifdef TOFILE
  FILE*f = fopen("sayall.dmp","w"); if (!f) f = stdout;
#else
# define f stdout
#endif
    if (env)
#ifdef ENVARR
        while (*env) P_PTR_STR(*env), env++;
#else
        { int l; while(l=strlen(env)) PR_STR(env), env+=l+1; }
#endif
        PR_STR("--args:");
        while (ac--) PR_STR(*av++);
#ifdef TOFILE
  if (f!=stdout) fclose(f);
#endif
}
