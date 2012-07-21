
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <io.h>

#include "svd.h"


#define LtextEND  0x0E
#define LparaOFS  0x12
#define LftnOFS   0x14
#define LbozaOFS  0x16
#define LdivOFS   0x18
#define Lsum1OFS  0x1A
#define LsumOFS   0x1C

#define LallOFS   0x6A
#define LpageOFS  0x76
#define Lboza1OFS 0x78
#define LhdrOFS   0x7C

#define OTHERSIZE 0x1000

char header[128], charbuf[128], parabuf[128], blank[128], Fill128[128];

cp infn = "x.doc", outfn = "y.doc",
   tmpfn= "txt.tmp", ptrfn = "ptr.tmp", inatr="rb", outatr="wb", fdon;
cp outnchar = "&char.h&",  outnpara = "&para.h&",
   outnpage = "&page.h&",  outndiv  = "&div.h&",
   outnftn  = "&ftn.h&",   outnhdr  = "&hdr.h&";

fl inf, outf, tmpf, ptrf,
   inchar,  inpara,  indiv,  inftn,  inpage,  inhdr,
   outchar, outpara, outdiv, outftn, outpage, outhdr;

uint charofs, paraofs, divofs, pageofs, ftnofs, bozaofs,
     hdrofs, sumofs, allofs, boza1ofs, diff, allsize;

#define L_charDESCR 2
#define L_paraDESCR 2
#define L_divDESCR 6
#define L_ftnDESCR 0        // - only 2 ptrs available -> ftnvalidescr = 2*
int L_pageDESCR,  L_hdrDESCR; // these 2 are read from header

int charvalidescr, paravalidescr, divalidescr=0,
    hdrvalidescr=0, ftnvalidescr=0, pagevalidescr=0;
int nchardescr=0, nparadescr=0, ndivdescr=0, nftndescr=0, npagedescr=0, nhdrdescr=0;
int ncharblock=0, nparablock=0, charvalidblock, paravalidblock;

long *charbp, *parabp;
cp divbp, pagebp, hdrbp, ftnbp,  divbf, pagebf, hdrbf, ftnbf;

bool nochar=0, nopara=0;
bool avail_div, avail_hdr, avail_ftn, avail_page, first_time, avail_sum;
// defaut: no divs, pages, hdrs, ftns;  there are paras, chars


long textsize, textend;
long txtptr, H, HHH;  // offset & number of current hyphen, number of all hyphens


void loadblock(cp where, fl from) { fread(where,128,1,from); }
void wblock(cp where, fl to) { fwrite(where,128,1,to); }

#ifdef maybe

void lother(bf,ff) cp *bf; fl ff; {
       if (!(*bf = malloc(OTHERSIZE))) err(NOMEM);
       fread(*bf,1,OTHERSIZE-1,ff);
     }

void sother(bf,ff,valid,L,add4) cp bf; fl ff; int valid,L; bool add4; { int l1,l2;
       l1 = 4 + (valid+add4) + valid*L;
       l2 = ((l1 >> 7) +1) <<7;
       if (valid) { fwrite(bf,1,l1,ff); fwrite(Fill128,1,l2-l1,ff); }
     }

dpfh(n,valid,L,bp) int *n,valid,L; cp *bp; {
    if (valid)   while (*n < valid  &&  *(long *)*bp < txtptr) {
                    *(long *)*bp += H;
                    *bp += L+4;  (*n)++;
                  }
  }

#endif

extern bool hyphword();         //hyphenating algorithm
#define MAXWORD 250
#define MAXIN 0x7800
#define BUFFSIZEK 0x1F
chr HYPHEN=0;
bool WORD5=0;
chr TABLE[256];
cp inbuf,outbuf,inbfp,outbfq, bf;
cp HelpHim = "The syntax is::\nhyph Infile [Outfile] /w /-nnn\n/w - MSWord .DOCs Only\n/-nnn - uses chr(nnn) as a HYPHEN\nIf Outfile omitted, Infile.HYH is accepted as output\n"; //Uses WhatToDo.HPH for ASCII tables\n

chr x;
int i,p,r,MX;   // count words that are too long
uint q;
int lsize, inofs, insize;
long leftsize, oksize, words=0, wordsH=0, filesize;

void free_all_buffs() { free(inbuf); free(outbuf); }

void load(where, how) cp where; int how; { fread(where,1,how,inf); }
void save() { fwrite(outbuf,1,q,outf); }  // q - howmuch to save, i.e. valid outbuf size

/****************************************/

void prehyph() { long t2 = txtptr+128;

 if (!nochar) {

       if (!ncharblock) {            // if 1st time - load 1st block
nextcharblock: if (ncharblock) wblock( charbuf, outchar);   // write current block
               if (ncharblock < charvalidblock) {
                  loadblock(charbuf,inchar);                // load next block
                  ncharblock++;
                  charvalidescr = charbuf[127];
                  nchardescr = 0;
                  charbp = (long *)charbuf;
                  if ( *charbp < t2) *charbp += H;
                  charbp += 1;
                } else { nochar = 1; goto paragraphs; }  // no more char descriptors
            }
       while ( *charbp < t2) {
          *charbp += H;
          (cp)charbp += L_charDESCR+4;
          nchardescr++;
          if (nchardescr >= charvalidescr) goto nextcharblock;
        }
     }

paragraphs:

 if (!nopara) {

       if (!nparablock) {
nextparablock: if (nparablock) wblock(parabuf,outpara);  // write current block
               if (nparablock < paravalidblock) {
                  loadblock(parabuf,inpara);               // load next block
                  nparablock++;
                  paravalidescr = parabuf[127];
                  nparadescr = 0;
                  parabp = (long *)parabuf;
                  if ( *parabp < t2) *parabp += H;
                  parabp += 1;
                } else { nopara = 1; goto others; }  // no more para descriptors
            }
       while ( *parabp < t2) {
          *parabp += H;
          (cp)parabp += L_paraDESCR+4;
          nparadescr++;
          if (nparadescr >= paravalidescr) goto nextparablock;
        }
     }

others:  ;
#ifdef maybe
   dpfh(&ndivdescr,  divalidescr,   L_divDESCR,  &divbp);
   dpfh(&nftndescr,  ftnvalidescr,  L_ftnDESCR,  &ftnbp);
   dpfh(&nhdrdescr,  hdrvalidescr,  0, &hdrbp);  //L_hdrDESCR,
   dpfh(&npagedescr, pagevalidescr, 0, &pagebp); //L_pageDESCR,
#endif

}

void wcopy(fname) cp fname; { fl infile; long rsize=0;
   infile = fopen(fname, inatr);
   while (!feof(infile)) {
      if (!(q=fread(outbuf,1,MAXIN,infile))) err(outERR);
      save(); rsize+= (long)q;
    }
   q = ((((rsize-1) >> 7) +1) << 7) - rsize;
   if (q) fwrite(Fill128,1,q,outf);
   fclose(infile);
 }
