%{
  /* @(#)trace_doc.l : automatic RTMX trace Version: 1.2 - 12:02:29 97/06/05
   *  Description:
   *     Requires that the subject file is a Frame document containing the
   *     paragraph and character types of the name:
   *
   *         Trace-<doc_id>[-<extra>]
   *
   *     where:
   *        <doc_id> is the id of a document being traced to.
   *                 EG., in SRS, there might be a para type: Trace-REQB.
   *        <extra>  is any addition text in the type, just in case you
   *                 want one para type in a table and another in the text.
   *
   *     Multiple references can be included on a given line, as long as they
   *     are separated by white space.
   *
   *  State diagram:
   *
   *          At start, or any state
   *
   *              | Start of "Heading[0-9]" paragraph         | <TabID
   *              | / if curr_ref not null print curr_ref     |
   *              |                                           |
   *             \ /       Start of new                      \ /
   *        -------------- para       --------          ---------------
   *        | STARTDOCID |----------->| IDLE |          | GETTABID    |
   *        |            |            --------          ---------------
   *        --------------                                    |
   *              | Start of paragraph                        |Found Table
   *              | number.                                   | ID.
   *              |                                           |
   *             \ /                                          |
   *        -------------                                     |
   *        | GETDOCID  |                                     |
   *        -------------                                     |
   *              | Got paragraph                             |
   *              | number.                                   |
   *              |                                           |
   *              |                                           |
   *             \ /                                         \ /
   *       -------------------------------------------------------------
   *       | STARTREQB                                                 |
   *       |                                                           |
   *       -------------------------------------------------------------
   *         |     | LTrace        / \         / \     <ATbl  |     / \
   *         |     |                |           |             |      |
   *         |    \ /               |           |            \ /     |
   *         |   ------------      /             \     ------------  |
   *         |   | FIXEDREQ |------               -----| FREQTAB  |  |
   *         |   |          |                          ------------  |
   *         |   |          |        --------------                  |
   *         |   |          |------->| TABINREQ   |                  |
   *         |   |          |        |            |                  |
   *         |   |          |<-------|            |                  |
   *         |   ------------        --------------                  |
   *         |     |  / \                                            |
   *         |      \ /                                              |
   *         |       -                                               |
   *         |                                                       |
   *         | Find a paragraph type with name "Trace-*"             |
   *         | or Find a character type with name "Trace-*"          |
   *         |                                                       |
   *        \ /                                                      |
   *   -----------                                                   |
   *   | PARSING |                                                   |
   *   |         |                                                   |
   *   |         |                                                   |
   *   -----------                                                   |
   *         | Found start of reference document name                |
   *         |       / curr_ref = null                               |
   *        \ /                                                      |
   *     ---------------- <Para or end of font trace                 |
   *     |              |       / print curr_ref                     /
   *     |   GETREQID   |--------------------------------------------
   *     |              |
   *     |              | <Font when not in font trace
   *     |              |          ----------------
   *     |              |--------->| FONTDBLCK    |
   *     |              |          |              |--------> ERROR
   *     |              |          |              | <FTag LTrace or Trace-
   *     |              |<---------|              |
   *     |              | End of   ----------------
   *     |              |  that font (basically, it was ignored)
   *     |              |
   *     |              |
   *     |              |------ <Char (found hard return, tab etc)
   *     |              |      \    / print curr_ref
   *     |              |       |
   *     |              |      /
   *     |              |<----
   *     |              |
   *     ----------------
   *      / \          | Found string containing section numbers
   *       |           | for the reference document
   *       |           |
   * add to| Found     |
   * curr  | last ref  |
   * ref   | for       |
   *       | string   \ /
   *     -----------------
   *     |   REQSTRING   |
   *     -----------------
   *            /\   | Found ref / process ref
   *             \   /
   *               -
   *
   */
#include <stdio.h>
#include <string.h>
int verbose;
#define  printf  if (verbose) printf
#define eprintf  printf
char *process_ref(char *format,char *doc2ref, char *intext, char *docID,
                  char *doc1ref, char *doc2ID);
void printline(FILE *dest, char *string0, char *string1, char *string2,
               char *string3, char *string4);
  char format1[] = "Table";
  char format2[] = "Section";
  char *format = NULL;
  char *ptr2Star = NULL;
  char *ptr2End = NULL;
  char *docIDString = NULL;
  char *doc1String = NULL;
  char *doc2IDString = NULL;
  char *doc2refString = NULL;
  FILE *dest;
  int   fonttrace=0;
        /* sd: now more than one String one after another allowed; will be concatenated */
  char morestring=0;
#define NEWSTRING(str,val)      if (str) free(str); str=val
#define DELSTRING(str)          NEWSTRING(str,NULL)
#define SETSTRING(str,val)      \
 if (morestring && str) { char * q = malloc( strlen(val)+strlen(str)+2);        \
                        strcpy(q,str); strcat(q,val); free(str); str = q;       \
  } else { NEWSTRING(str, strdup(val) ); }

  /* States:
   IDLE          waiting for a new section in this document
   GETTABID      Found the start of a table at the beginning of the document - get it's ID
   STARTDOCID    looking for the Current Paragraph num for this document
   GETDOCID      loading Current Paragraph number for this document
   STARTREQB     looking for a reference document
   PARSING       found a reference document -> getting its name
   GETREQID      getting the string containing the reference document's section numbers
   REQSTRING     getting the next section number from the reference document string.
   GETTABREF     Got the start of a table reference while looking for a
                 reference document reference. Get the ID.
   TABINREQ      Looking for a Table ID from a GETTABREF.
   FIXEDREQ      Found LTrace - look for the Requirement ID.
   GETFREQ       Found the fixed requirement ID.
   FREQTAB       Found a table reference while looking for the fixed
                   requirement ID. Looking for the Table ID.
   FONTDBLCK     An unwanted font change has been located.  Ignore it if
                   it is not LTrace or Trace. Otherwise, exit with error.
                   We can't nest tags.
  */
%}

%s IDLE
%s STARTDOCID
%s GETDOCID
%s GETTABID
%s STARTREQB
%s GETTABREF
%s PARSING
%s GETREQID
%s REQSTRING
%s TABINREQ
%s FIXEDREQ
%s FR_IDLE
%s FR_TAG
%s GETFREQ
%s FREQTAB
%s FONTDBLCK

%%

"<PgfTag `Heading"[0-9]         { printf("found head\n"); BEGIN STARTDOCID;
                                  doc2refString=process_ref(format, doc2refString, NULL, docIDString,doc1String,doc2IDString);
                                  format = &format2[0]; doc1String = NULL; }
<STARTDOCID>"<Para "            { printf("idle\n");BEGIN IDLE; }
<STARTDOCID>"<PgfNumString `"   { BEGIN GETDOCID; }
<GETDOCID>""[0-9]*[.0-9]*       { SETSTRING(docIDString,yytext); printf("docid(%s)\n",docIDString);
                                  BEGIN STARTREQB; }
"<TblID "                       { printf("gettabid\n"); BEGIN GETTABID;
                                  format = &format1[0]; doc1String=NULL; }
<GETTABID>""[0-9]+              { SETSTRING(docIDString,yytext);
                                  printf("loading tabid(%s)\n",docIDString);
                                  BEGIN STARTREQB; }
<STARTREQB>"<PgfTag `Trace-"    { printf("begin para parse\n"); BEGIN PARSING; fonttrace=0;}
<STARTREQB>"<FTag `Trace-"      { printf("begin font parse\n"); BEGIN PARSING; fonttrace=1;}
<STARTREQB>"<PgfTag `LTrace"    { printf("begin FREQ para\n"); fonttrace=0; BEGIN FIXEDREQ; DELSTRING(doc1String); morestring=1; }
<STARTREQB>"<FTag `LTrace"      { printf("begin FREQ font\n"); fonttrace=1; BEGIN FIXEDREQ; DELSTRING(doc1String); morestring=1; }
<STARTREQB>"<ATbl"              { printf("Found a Table ref\n");
                                  doc2refString=process_ref(format, doc2refString,NULL, docIDString, doc1String, doc2IDString);
                                  BEGIN GETTABREF; }
 /* if u have <font inside the <para ltrace etc, this below is required to recover after it;
    also there may be a single string divided into two with font inside
    for now, only fixedreq need it; the getreq part does not need this, but be aware! */
<FIXEDREQ>"<Para "              { printf("idle para\n"); BEGIN FR_IDLE; /* STARTREQB; */ }
<FIXEDREQ>"<Font "              { if (fonttrace==0) { printf("idle font\n"); BEGIN FR_IDLE; }
                                   else { printf("eo freq font\n"); morestring=0; BEGIN STARTREQB; } }
<FR_IDLE>">"                    { printf("eo idle font/para/whatever\n"); BEGIN FIXEDREQ; }
<FR_IDLE>"<"                    { printf("fr idle sometag\n"); BEGIN FR_TAG; }
<FR_TAG>">"                     { printf("eo fr idle sometag\n"); BEGIN FR_IDLE; }

<FIXEDREQ>"<Char "              { printf("found HR\n"); }

<FIXEDREQ>"<String `"           { printf("begin FixedReq\n"); BEGIN GETFREQ; }
<FIXEDREQ>"<ATbl"               { printf("Found a Table ref\n"); BEGIN FREQTAB; }
<FIXEDREQ>"> # end of Para"     { printf("eo freq para\n"); morestring=0; BEGIN STARTREQB; }
<FIXEDREQ>"> # end of Font"     { if (fonttrace==0) { printf("eo freq font\n"); morestring=0; BEGIN STARTREQB; } }

<FREQTAB>""[0-9]+               { printf("  ref is (%s)\n",yytext);
                                  SETSTRING(doc2IDString,"Table")
                                  doc2refString =process_ref(format, doc2refString,yytext, docIDString,doc1String,  doc2IDString);
                                  BEGIN FIXEDREQ; }
<GETFREQ>""[ ]*[A-Za-z_\-;:/.0-9]+[ ]*  { printf("Found FixedReq(%s)\n", yytext); SETSTRING(doc1String,yytext); }
<GETFREQ>"'>"[ \n]*"<String `"  { printf("end of string, new one\n"); morestring=1; }
<GETFREQ>"'>"                   { printf("end of string\n"); /*morestring=0;*/ BEGIN FIXEDREQ; /*STARTREQB*/; }

<GETTABREF>""[0-9]+             { printf("  ref is (%s)\n",yytext);
                                  SETSTRING(doc2IDString,"Table");
                                  doc2refString =process_ref(format, doc2refString,yytext, docIDString,doc1String,  doc2IDString);
                                  BEGIN STARTREQB; }
<PARSING>""[0-9_\:A-Za-z]+      { SETSTRING(doc2IDString,yytext); printf("Found ReqTrace, refid(%s)\n",doc2IDString);
                                  BEGIN GETREQID; }
<GETREQID>"<Para "              { printf("new para\n"); BEGIN STARTREQB;
                                  doc2refString=process_ref(format, doc2refString,NULL, docIDString, doc1String, doc2IDString); }
<GETREQID>"<Font "              { printf("new font\n");
                                  if (fonttrace) { printf("finished font trace\n");
                                    BEGIN STARTREQB;
                                    doc2refString=process_ref(format, doc2refString,NULL, docIDString, doc1String, doc2IDString);
                                  }
                                }

<FONTDBLCK>"<FTag `Trace-"      { eprintf("ERROR, Cannot have Font Reference in Para Reference\n"); exit(1);}
<FONTDBLCK>"<FTag `LTrace-"     { eprintf("ERROR, Cannot have Font Reference in Para Reference\n"); exit(1);}

<FONTDBLCK>"> # end of Font"    { printf("go back to GETREQID\n"); BEGIN GETREQID; }
<GETREQID>"<Char "              { printf("found HR\n");
                                  doc2refString=process_ref(format, doc2refString,NULL, docIDString,doc1String,  doc2IDString); }
<GETREQID>"<String `"           { printf("begin reqstring\n"); morestring=0; BEGIN REQSTRING; }
<GETREQID>"<ATbl"               { printf("Found a Table ref\n");
                                  doc2refString=process_ref(format, doc2refString,NULL, docIDString, doc1String, doc2IDString);
                                  BEGIN TABINREQ; }

<TABINREQ>""[0-9]+              { printf("  ref is (%s)\n",yytext);
                                  doc2refString =process_ref(format, doc2refString,yytext, docIDString,doc1String, "Table");
                                  doc2refString =process_ref(format, doc2refString,NULL, docIDString,doc1String, "Table");
                                  BEGIN GETREQID; }

<REQSTRING>""[ ]*[A-Za-z_\-;:/.0-9]+[ ]*        { printf("Found ReqTrace(%s)\n", yytext);
                                                doc2refString =process_ref(format, doc2refString,yytext, docIDString,doc1String,  doc2IDString); }
<REQSTRING>" '>"                { printf("Found space string()\n");
                                  doc2refString =process_ref(format, doc2refString," ", docIDString,doc1String,  doc2IDString);
                                  BEGIN GETREQID; }
<REQSTRING>"'>"[ \n]*"<String `"        { printf("end of string, new one\n"); morestring=1; }
<REQSTRING>"'>"                 { printf("end of string\n"); morestring=0; BEGIN GETREQID; }

.|\n    /*IGNORE*/      /*{ printf("--ignore %s\n", yytext); } */
%%
extern char *yytext;

int main(int argc, char **argv)
{
  if (argc>1 && argv[1][0]=='-' && argv[1][1]=='v') verbose++;
/*  if((dest = fopen("rtmx_trace.tab", "a")) == NULL) {
    printf("\nSorry! Can't open rtmx target\n");
    return -1;
  }
*/
  dest = stderr;
  yyin = stdin;
  yylex();
  doc2refString=process_ref(format, doc2refString,NULL, docIDString,doc1String,  doc2IDString);
  fprintf(dest,"\n");
  fclose(dest);
  return 0;
}

/**************************************************************************
  format:  "Section" or "Table"
  doc2ref: current reference for the document referenced by <doc2ID>
  intext:  additional text to be added to doc2ref
  docID:   the section number of this document
  doc1ref: current reference for this document
  doc2ID:  the name of the document being referenced.

  This procedure produces a table with the following five line formats:
  1) A reference within a table with no local references
     Table <TabID> -  <doc2ID> <doc2ref>
  2) A reference within a table which has a local reference
     Table <TabID> <LocalReq> <doc2ID> <doc2ref>
  3) A reference within a section
     Section <section> <LocalReq> <doc2ID> <doc2ref>
  4) A table within a section
     Section <section> - TABLE <TabID>
  5) A table within a section prefixed by a Local requirement
     Section <section> <LocalReq> TABLE <TabID>
**************************************************************************/
char *process_ref(char *format, char *doc2ref, char *intext, char *docID,
                  char *doc1ref, char *doc2ID)
{
int index;
char *starttext;
char *newtext;
char *currtext;
int ready;

   eprintf("process(%x,%x,%x,%x,%x)\n",doc2ref,intext,docID,doc1ref,doc2ID);
   ready = 0;
   currtext = doc2ref;
   starttext = intext;

   /* if there is new text coming in, with spaces at front, process that*/
   if (starttext != NULL) {
     printf("Checking1 start(%s)\n",starttext);
     if (*starttext == ' ' || *starttext == '\t')
       printf("(%s) has spaces at front ",starttext);

     while(*starttext == ' ' || *starttext == '\t')
       starttext++;
   }

   /* if the new text had speces and there is current text, print the */
   /* current text */
   if ((starttext != intext) && (currtext != NULL)) {/* spaces were found */
       printline(dest,format,docID,doc1ref,doc2ID,currtext);
       free(currtext);
       currtext=NULL;
   }

   /* if there is new text coming in, get rid of any spaces at end */
   printf("Checking start text(%x)\n",starttext);
   if (starttext != NULL && strlen(starttext) > 0) {
     printf("before_dup \n");
     newtext = strdup(starttext);
     index = strcspn(newtext,"  ");
     printf("got(%s){%d} ",intext,index);
     if (index > 0) {
       if (index < strlen(newtext)) {
         ready = 1;
         newtext[index] = '\0';
         printf("had spaces ");
       }
       printf(" now(%s) ",newtext);
     } else {
       free(newtext);
       printf("just spaces ");
     }

     /* if there is already text waiting, add to this */
     if (currtext != NULL ) {
       printf("adding to(%s) ",currtext);
       index += strlen(currtext);
       currtext = (char *)realloc(currtext,index+1);
       strcat(currtext,newtext);
       printf("gives(%s)+(%s)=(%s){%d} ",currtext,newtext,currtext,index);
     } else {
       currtext = newtext;
     }
   } else {
     ready = 1;
        printf("just print what's there\n");
   }

   /* if input had spaces or there was no input and stuff was waiting to
      print, print it out  otherwise wait for next line */

   if (currtext != NULL && ready) {
        printf("printing(%s)\n",currtext);
     printline(dest,format,docID,doc1ref,doc2ID,currtext);
     free(currtext);
     currtext=NULL;
   }
   if (currtext) { printf("finally returning(%s)\n",currtext); }
   else { printf("nothing being returned\n"); }

   return(currtext);
}

void printline(FILE *dest, char *string0, char *string1, char *string2,
               char *string3,  char *string4)
{
/* sd: print Everything, separated by formfeed */
#define S(x) (x?x:"-")
 fprintf( dest, "%s\f%s\f%s\f%s\f%s\n", S(string0), S(string1), S(string2), S(string3),
S(string4) );
#if 0
  if (string0) {
    fprintf(dest,"%-10s",string0);
  } else {
      fprintf(dest,"%-10s","-");
  }
  if (string1) {
    fprintf(dest,"%-20s",string1);
  } else {
      fprintf(dest,"%-20s","-");
  }
  if (string2) {
    fprintf(dest,"%-20s",string2);
  } else {
      fprintf(dest,"%-20s","-");
  }
  if (string3) {
    fprintf(dest,"%-20s",string3);
  } else {
      fprintf(dest,"%-20s","-");
  }
  if (string4) {
    fprintf(dest,"%-20s\n",string4);
  } else {
      fprintf(dest,"%-20s\n","-");
  }
#endif
}
