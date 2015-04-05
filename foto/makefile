ROOT ?= ./

all:
	@echo i3c ? i6c ? ren6v ? opt ? optjpg ? autorot ?autodate

BIN = $(dir $(MAKEFILE_LIST))

i3c 3c c3 300: ren3
	$(MAKE) -f $(MAKEFILE_LIST) opt
ren3:
	rename.pl 'y/A-Z/a-z/+s/_/1/' $(ROOT)*JPG $(ROOT)*jpg

ix index:
	~/src/bin/foto/indexer.sh *.jpg > index.html
autorot:
	jhead -autorot $(ROOT)*.jpg
autodate:
	jhead -ft $(ROOT)*.jpg

OPTs=$(wildcard $(ROOT)*.jpg)
OPTs1=$(wildcard $(ROOT)*.JPG)

jpg2opt: $(OPTs:%.jpg=%.opt) $(OPTs1:%.JPG=%.opt)
opt: jpg2opt
	$(MAKE) -f $(MAKEFILE_LIST) opt1jpg

%.opt: %.jpg
	jhead "$<" | grep -i progressive || jpegtran -optimize -progressive -copy all -outfile "$@" "$<"
%.opt: %.JPG
	jhead "$<" | grep -i progressive || jpegtran -optimize -progressive -copy all -outfile "$@" "$<"

#	diff -q $@ $< && rm $@ || mv -f $@ $<

OPT2s=$(wildcard $(ROOT)*.opt)
opt1jpg: $(OPT2s:%.opt=%.opt1)
opt2jpg: $(OPT2s:%.opt=%.opt2)
opt3jpg: $(OPT2s:%.opt=%.opt3)
%.opt1: %.opt
	mv -f $< $*.jpg
%.opt2: %.opt
	cp $< $*.jpg ; rm $<

opt3: $(OPTs:%.jpg=%.opt3)
%.opt3: %.jpg
	$(BIN)/jpgoptmz1.sh $<

#AUTOROT=1
2: $(OPTs:%.jpg=2/%.jpg)
2/%.jpg: %.jpg
	-$(BIN)/2small.sh $<

#AUTOROT=1
4: $(OPTs:%.jpg=4/%.jpg)
4/%.jpg: %.jpg
	-SCALE=4 $(BIN)/2small.sh $<

optjpg:
	rename.pl 's/opt$$/jpg/' $(ROOT)*.opt

600 c6 6c i6c: ren6
	$(MAKE) -f $(MAKEFILE_LIST) opt
	$(MAKE) -f $(MAKEFILE_LIST) optjpg
	$(MAKE) -f $(MAKEFILE_LIST) autodate
ren6:
	rename.pl 'y/A-Z/a-z/+s/img_9/i6c09/+s/img_/i6c1/' $(ROOT)*.JPG $(ROOT)*.jpg
ren6v:
	rename.pl 'y/A-Z/a-z/+s/mvi_9/v6c09/+s/mvi_/v6c1/' $(ROOT)*.MOV* $(ROOT)*.mov*

diffix:
	diff -btw index.html .. | perl -ne 'print if s/.*"(.*)".*/$$1 /' > ../rmm

view:
	qiv -s -m -i -f -d 1 *.jpg
%.ffmpeg.mkv: %.MOV
	ffmpeg -i $< -sameq $@
%.ffmpeg.mkv: %.mov
	ffmpeg -i $< -sameq $@

dati:
	find . -type d -exec sh -c 'jhead -ft "{}"/*jpg' \;

# vim:ts=4:sw=4:noexpandtab
