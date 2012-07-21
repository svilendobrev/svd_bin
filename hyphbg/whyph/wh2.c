#define MAINEXE xyz
//#define maybe
#include "wl.c"

main(argc, argv, envp) int argc; char *argv[]; char *envp; {
   puts("SvD Text & MSWord files Hyphenator - bg v2xA");

   if (argc==1) err(NOINERR);
    else infn = argv[1];

   if (!(tmpf=fopen(infn,inatr))) err(inOPENERR);
   loadblock(header,tmpf);   fclose(tmpf);
   WORD5  =  ( 0xBE31 == *(uint *)header) ? 1 : 0;

/************************************************/

   p=0;
   for (i=1; i<argc;i++) {
      bf = argv[i];
      if ('/'==*bf || '-'==*bf) {
         switch (*(bf+1)) {
            case 'w':
            case 'W': if (!WORD5) puts("Warning! Non-MSWord file");
                      WORD5=1; continue;
            case '-': sscanf(bf+2,"%d",&HYPHEN); continue;   // get int value
          }  // endswitch
       } else switch (p) {
                 case 0: infn=bf;  p++; continue;
                 case 1: outfn=bf; p++; continue;
               }
       printf("Skipped invalid argument %s\n",bf);
     }

   if (!p) err(NOINERR);


   if (p==1) {
      i=strlen(infn); outfn=blank; strcpy(outfn,infn);
      if(!(fdon=strrchr(outfn,'.'))) fdon=outfn+i;
      strcpy(fdon,".HYH");
    }

   if (!(inf =fopen(infn,inatr))) err(inOPENERR);
   filesize = filelength(fileno(inf));

   if (WORD5) {
      puts("MS Word format accepted.");
      ptrf = fopen(ptrfn, outatr);
      loadblock(header,inf);
      textend  = *(long *)(header+LtextEND);
      textsize = textend-128L;
#ifndef maybe
      puts("Only character and paragraph info saved.");
#endif
   } else textsize = filesize;

// pl(textsize);

   if (!(outf=fopen((WORD5) ? tmpfn : outfn, outatr))) err(outOPENERR);

   if (!(inbuf = malloc((uint)BUFFSIZEK<<10)) || !(outbuf= malloc((uint)BUFFSIZEK<<11))) err(NOMEM);

   for (i=0; i<=255; i++) TABLE[i]=0;
   for (i=128; i<=159; i++) TABLE[i]= i-127;       // Default settings
   TABLE[(chr)'€']+=128; TABLE[(chr)'…']+=128; TABLE[(chr)'ˆ']+=128; TABLE[(chr)'Ž']+=128;
   TABLE[(chr)'“']+=128; TABLE[(chr)'š']+=128; TABLE[(chr)'ž']+=128; TABLE[(chr)'Ÿ']+=128;
   for (i=160; i<=191; i++) TABLE[i]= TABLE[i-32];

   if (!HYPHEN) HYPHEN = '-';
   printf("\nHYPHEN is ASCII %d\n",HYPHEN);

inofs = 0; oksize = 0L; leftsize = textsize;

while (lsize = ((long)min(leftsize,(long)MAXIN))) {

   load(inbuf+inofs,lsize);
   insize = lsize+inofs;
   p=q=0; inbfp=inbuf; outbfq=outbuf;

   while (p<insize)
      if (!TABLE[(chr)(x=(chr)*inbfp)]) { *outbfq++ = x; p++; q++; inbfp++;}
       else { r = min(insize - p, MAXWORD);
         for (i=0; i<r && TABLE[(chr)inbfp[i]]; i++);
         if (i==MAXWORD) MX++;
           else {
               if (p+i> insize) {   save(); // here was =
                  memcpy(inbuf, inbfp, inofs= insize-p);
                  goto loadnext; }
              }
       txtptr = oksize+p;
         r= hyphword(outbfq,inbfp,i)+i;
         p+= i; inbfp+= i; q+= r; outbfq+= r;  HHH+= r-i;
       }
   save(); inofs=0;
loadnext:
   leftsize-= (long)lsize;         // size left to EOF
   oksize+= (long)lsize;           // passed size

 } // EO while


/*****************************************************************************/
/*****************************************************************************/


   if (!WORD5) goto exit;
   fclose(outf);  fclose(ptrf);
   tmpf = fopen(tmpfn, inatr);
   ptrf = fopen(ptrfn, inatr);

   inchar = fopen(infn, inatr);
   inpara = fopen(infn, inatr);

   outf    = fopen(outfn,    outatr);
   outchar = fopen(outnchar, outatr);
   outpara = fopen(outnpara, outatr);

   charofs = ((long)(textend-1L)>>7)+1;
   paraofs = *(uint *)(header+LparaOFS);
   ftnofs  = *(uint *)(header+LftnOFS);

   sumofs  = *(uint *)(header+LsumOFS);

#ifdef maybe
   bozaofs = *(uint *)(header+LbozaOFS);
   divofs  = *(uint *)(header+LdivOFS);

   allofs  = *(uint *)(header+LallOFS);
   pageofs = *(uint *)(header+LpageOFS);
   boza1ofs = *(uint *)(header+Lboza1OFS);
   hdrofs  = *(uint *)(header+LhdrOFS);

   if (!pageofs) pageofs = bozaofs;
   if (!hdrofs)  hdrofs  = divofs;
#endif

   allsize = ((long)(filesize-1L)>>7)+1;

   charvalidblock = paraofs - charofs;
   paravalidblock = ftnofs  - paraofs;

   avail_sum = (allsize!=sumofs);  //? 0 : allsize - sumofs;

   fseek(inchar, (long)((long)charofs)<<7, 0);
   fseek(inpara, (long)((long)paraofs)<<7, 0);

#ifdef maybe
// printf("Ofs- chr %d, para %d, div %d, boza %d, hdr %d, ftn %d, page %d, sum %d, all %d\n",charofs, paraofs, divofs, bozaofs, hdrofs, ftnofs, pageofs, sumofs, allsize);

   avail_ftn = (allsize==ftnofs)  ? 0 : bozaofs - ftnofs;
   avail_page= (allsize==pageofs) ? 0 : hdrofs  - pageofs;
   avail_hdr = (allsize==hdrofs)  ? 0 : divofs  - hdrofs;
   avail_div = (allsize==divofs)  ? 0 : sumofs  - divofs;

// printf("V- char %d, para %d, div %d, hdr %d, ftn %d, page %d, sum %d\n",charvalidblock, paravalidblock, avail_div, avail_hdr, avail_ftn, avail_page, avail_sum);


   if (avail_div) {
             indiv   = fopen(infn, inatr);
         //  outdiv  = fopen(outndiv, outatr);
             fseek(indiv, ((long)divofs)<<7, 0);
             lother(&divbf, indiv); divbp = divbf+4;
             divalidescr = *(int *)divbf;
           }

   if (avail_ftn) {
             inftn  = fopen(infn, inatr);
       //    outftn  = fopen(outnftn, outatr);
             fseek(inftn, ((long)ftnofs)<<7, 0);
             lother(&ftnbf, inftn); ftnbp = ftnbf+4;
             ftnvalidescr = *(int *)ftnbf * 2;
           }

   if (avail_page) {
             inpage  = fopen(infn, inatr);
     //      outpage = fopen(outnpage, outatr);
             fseek(inpage, ((long)pageofs)<<7, 0);
             lother(&pagebf, inpage); pagebp = pagebf+4;
             pagevalidescr = *(int *)pagebf +1;
             L_pageDESCR = *(int *)(pagebf+2);
           }

   if (avail_hdr) {
             inhdr  = fopen(infn, inatr);
   //        outhdr = fopen(outnhdr, outatr);
             fseek(inhdr, ((long)hdrofs)<<7, 0);
             lother(&hdrbf, inhdr); hdrbp = hdrbf+4;
             hdrvalidescr = *(int *)hdrbf +1;
             L_hdrDESCR = *(int *)(hdrbf+2);
           }
#endif

   for (H=0; H < HHH; H++) {
      fread((cp)&txtptr,4,1,ptrf);
      prehyph();
    }

   txtptr = textsize+2; // cause last paradescr points textsize+1, not textsize
   prehyph();

   txtptr = textsize + HHH;      //new textsize

   diff = ((long)(txtptr-1L)>>7)+2 - charofs;

   *(long *)(header+LtextEND) = txtptr+128L;  //textend 0E

   *(uint *)(header+LparaOFS) +=diff;  //paraofs   12

#ifndef maybe
   ftnofs+=diff;
   *(uint *)(header+LftnOFS)  =ftnofs;  //ftnofs    14
   *(uint *)(header+LbozaOFS) =ftnofs;  //bozaofs   16
   *(uint *)(header+LdivOFS)  =ftnofs;  //divofs    18
   *(uint *)(header+Lsum1OFS) =ftnofs;  //sum1ofs   1A
   *(uint *)(header+LsumOFS)  =ftnofs;  //sumofs    1C
   memcpy(header+64,Fill128,64);

#else

   *(uint *)(header+LftnOFS)  +=diff;  //ftnofs    14
   *(uint *)(header+LbozaOFS) +=diff;  //bozaofs   16
   *(uint *)(header+LdivOFS)  +=diff;  //divofs    18
   *(uint *)(header+Lsum1OFS) +=diff;  //sum1ofs   1A
   *(uint *)(header+LsumOFS)  +=diff;  //sumofs    1C

   if (allofs)   *(uint *)(header+LallOFS)  +=diff;   //  6A
   if (pageofs)  *(uint *)(header+LpageOFS) +=diff;   //  76
   if (boza1ofs) *(uint *)(header+Lboza1OFS)+=diff;   //  78
   if (hdrofs)   *(uint *)(header+LhdrOFS)  +=diff;   //  7C
#endif

   fclose(inchar);  fclose(outchar);  fclose(outpara);
   wblock(header, outf);
   wcopy(tmpfn);
   wcopy(outnchar);
   wcopy(outnpara);

#ifdef maybe
   sother(ftnbf,  outf, ftnvalidescr,  L_ftnDESCR,0);
   sother(pagebf, outf, pagevalidescr, L_pageDESCR,1);
   sother(hdrbf,  outf, hdrvalidescr,  L_hdrDESCR,1);
   sother(divbf,  outf, divalidescr,   L_divDESCR,0);
#endif

   if (avail_sum) {
      fseek(inpara, ((long)sumofs)<<7, 0);
      loadblock(inbuf, inpara);
      *(long *)(inbuf + (i = *(int *)(inbuf+0x10))) = textsize;
      memcpy(inbuf+4+i,Fill128,128-i);
      wblock(inbuf, outf);
      for (i=(avail_sum+1+diff)%4; i>0; i--) wblock(Fill128,outf);
    }

   /****************************************************************/
exit:
   printf("\nTotal words found: %ld; Hyphenated: %ld. Saved as: %s\n",words,wordsH,outfn);
   remove(tmpfn); remove(ptrfn); remove(outnchar); remove(outnpara);

   err(0);

 } // EO main

