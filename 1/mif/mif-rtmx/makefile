# makefile for rtmx.txt itself
# add/change trace-matrixes into two rules: RTMX: *.tab, and  *.tab: whatever.doc(s)
# change RTMX for result text filename; FMBATCH for other frame version/path; DOC for root of docs
RTMX=rtmx.txt
TRACER=trace_doc

DOC=/project/indi/doc
FMBATCH=/usr/local/frame5.5/bin/fmbatch

all: exe rtmx
exe: $(TRACER)
rtmx: $(RTMX)
$(RTMX): SRS_rtmx.tab VCIS_rtmx.tab SDD_rtmx.tab IRSDD_rtmx.tab MITD_rtmx.tab STD_rtmx.tab
	perl mrtmx.pl $^ >$(RTMX)

CPY=.cpy
MIF=.MIF#$(CPY)
# use -v for verbose
TRACEIT=$(TRACER)  < $$x 2>>$@
GENTRACES=:>$@; for x in $^; do $(TRACEIT) ; done

SRS_rtmx.tab:	$(DOC)/req_analysis/srs/srs.doc$(MIF)
	$(GENTRACES)
VCIS_rtmx.tab:	$(DOC)/req_analysis/interface/vcis/vcis.doc$(MIF)
	$(GENTRACES)
SDD=$(wildcard $(DOC)/design/verilog_a/vlac_sdd_*.doc) 
SDD_rtmx.tab: 	$(SDD:%=%$(MIF))
	@$(GENTRACES)
IRSDD_rtmx.tab: $(DOC)/design/interface/ir/ir_spec.doc$(MIF)
	$(GENTRACES)
MITD_rtmx.tab: 	$(DOC)/test/mitd/vlc_mitd.doc$(MIF)
	$(GENTRACES)
STD_rtmx.tab: 	$(DOC)/test/std/std.doc$(MIF)
	$(GENTRACES)

cleanrtmx:
	-rm -f $(RTMX)
cleanall: cleanrtmx
	-rm -f *.tab

%$(MIF): %
	cp -f $< $<$(CPY); chmod +w $<$(CPY)
	echo "Open $<$(CPY)" >batchjob
	echo "SaveAs m $<$(CPY) $@" >>batchjob
	$(FMBATCH) batchjob
	rm -f $<$(CPY) batchjob

#TRACERPATH=/home/indi/tools/packages/rtmx_maker/
#TRACEPROC=trace_doc.perl
#TAB=rtmx_trace.tab
#TRACEIT=perl $(TRACEPROC) -f $$x; cat $(TAB) >>$@

#############
# makefile for the MIF parser
CC=gcc
LEX=flex
LFLAGS=
#yywrap() is here:
LDFLAGS=-lfl

clean:
	-rm -f $(TRACER) $(TRACER).o $(TRACER).c

%: %.c
	${CC} -o $@ $< ${LDFLAGS}
#%.o: %.c
#	${CC} -c $<
%.c: %.l
	${LEX} -t $< > $@
