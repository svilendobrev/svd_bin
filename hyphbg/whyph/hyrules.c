
#define PUT_PTRS

#include "svd.h"

#ifdef PUT_PTRS
  extern void * ptrf;
  extern long txtptr;
  extern bool WORD5;
  static long z;
#endif

extern long words,wordsH;
extern chr TABLE[];
extern chr HYPHEN;

#define vocal(xxxx) (((chr)(xxxx))>127)


void translate(dest,src,n) cp dest,src; chr n; { register int i;
   for (i=n-1; i>=0; i--) *dest++= TABLE[(chr)*src++];
 }

bool hyphrules(word,x) cp word; int x; {
bool res;
chr cpp, cp, cx, cn;   // pre-previous, previous, current (x-th), next char

cpp= word[x-2]; cp = word[x-1]; cx = word[x]; cn = word[x+1];

#if 0
/*
   I. vocal CX : 1. vocal CP - YES - ����� ������                    @vV
                 ELSE  NO - ���� �������� � ����� ������             @nV
   II. !vocal CX
    1. vocal CP
      1. vocal CN    1. vocal CPP & vocal CPPP - NO -
                       -  ���� ������ ������ ����� ����! ��������  @vvvNv
                      ELSE YES - ���� ������ ����� ����! ��������    @vNv
      2. !vocal CN   1. CX,CN = "��" - YES - ���� ������ ����� ��    @v��
                      ELSE NO - ���� ������ ����� ���! ��������      @vNn
    2. !vocal CP :
      1. CX="�" | CP=CPP | CX=CN   - NO  -    ����� �������� � �     @n�
                                             ����  ������! �������� @zzN
                                             ����� ������! ��������  @nZZ
      2. CP,CX = "��" - NO - ����� ��                                @��
      3. CP="�" 3.1 !vocal CN - NO  - ���� � ����� ��� ��������      @�Nn
      ELSE YES  ����� ��� ��������                                   @nN

     Remarks: ������� ������� �� �������� �������� ���-�����, � ����-����
*/
#endif

   if (vocal(cx)) res = vocal(cp);
    else if (vocal(cp))
            if (vocal(cn))  res = !(x>2 && vocal(word[x-3]) && vocal(cpp));
              else res = cx==TABLE[(chr)'�'] && cn==TABLE[(chr)'�'];
          else
            res = !(cx==TABLE[(chr)'�'] || cpp==cp || cx==cn ||
                    cp==TABLE[(chr)'�'] && cx==TABLE[(chr)'�'] ||
                    cp==TABLE[(chr)'�'] && !vocal(cn) );
   return(res);
 }

bool hyphword(dest,src,n) chr n; cp src,dest; {
int i, firstH, lastH, res=0;  // 1st and last hyphenable char-position in word
static chr wordbuf[512];

// px(src,n);

   if (n<4) goto nohyph;
   translate(wordbuf,src,n);

   for (firstH=0; firstH<n && !vocal(wordbuf[firstH]); firstH++); // FIRST vocal

   for (lastH=n-1; lastH>=0 && !vocal(wordbuf[lastH]); lastH--);  // LAST vocal
   if (firstH<2) firstH=2;           // LONELY letters are not hyphenated
   if (lastH==n-1) lastH--;
   if (firstH>lastH) {
nohyph:                              // Word is too SHORT
      memcpy(dest,src,n);
      goto wexit;
    }

   for (i=0; i<n; i++) {
      if (i>=firstH && i<=lastH)
         if (hyphrules(wordbuf,i)) {
               #ifdef PUT_PTRS
                 if (WORD5) {
                    z = txtptr + i;
                    fwrite((cp)&z, 4,1, ptrf);
                  }
               #endif

           *dest++ = HYPHEN; res++; }    // ? Hyphenable BEFORE i-th position
      *dest++ = *src++;
     }

/* *dest = 0; */
wexit:
   if (res) wordsH++;
   words++;
   return res;
 }

