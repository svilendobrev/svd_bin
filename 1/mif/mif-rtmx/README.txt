some guidelines for using rtmx generator
sd Aug'99

terminology: the REQ name is named trace-tag.
1. you need to have EITHER character OR paragraph tag named LTrace.
    this is what is associated with your file
2. you need to have EITHER character OR paragraph tag named Trace-whatever.
    this is where you trace to. you may have more than one of these
3. anything inside the above tags/with above tags is considered trace-tags
3. you could have multiple trace-tags on one line/inside one traceability definition (see 1,2,3).
4. the separator used is white space. everything else is considered part of the tag.
    no limit for size of tag
5. for doc2mif conversion, frame 5.5 requires files to be Writeable,
    therefore, this will temporary copy input files into *.cpy

6. at the end, you may remove all the .MIF files - they are quite big (they are where .doc's are)

makefile usage:
 run make to get the results, then use the rtmx.txt;
 any update of some docs will force that particular MIF/rtmx...tab to be rebuilt and the
  whole rtmx.txt to be rebuilt too;
 to add/change documents/paths, see in the makefile
requires:
 - the MAKEFILE (and some GNUMAKE compatible make)
 - TRACEDOC.L (will build executable TRACE_DOC from it, hence C COMPILER and LEX/FLEX)
 - PERL for MRTMX.PL
 - FMBATCH  for proper version of frame

