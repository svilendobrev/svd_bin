ROOT ?= ./

all:
	@echo i3c ? i6c ? ren6v ? opt ? optjpg

BIN = $(dir $(MAKEFILE_LIST))

i3c 3c c3 300: ren3
	$(MAKE) -f $(MAKEFILE_LIST) opt
ren3:
	rename.pl 'y/A-Z/a-z/+s/_/1/' $(ROOT)*JPG $(ROOT)*jpg

OPTs=$(wildcard $(ROOT)*.jpg)
OPTs1=$(wildcard $(ROOT)*.JPG)

opt: $(OPTs:%.jpg=%.opt) $(OPTs1:%.JPG=%.opt)

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

2: $(OPTs:%.jpg=2/%.jpg)
2/%.jpg: %.jpg
	-$(BIN)/2small.sh $<

4: $(OPTs:%.jpg=4/%.jpg)
4/%.jpg: %.jpg
	-SCALE=4 $(BIN)/2small.sh $<

optjpg:
	rename.pl 's/opt/jpg/' $(ROOT)*.opt

600 c6 6c i6c: ren6
	$(MAKE) -f $(MAKEFILE_LIST) opt
	$(MAKE) -f $(MAKEFILE_LIST) optjpg
ren6:
	rename.pl 'y/A-Z/a-z/;s/img_/i6c0/' $(ROOT)*.JPG $(ROOT)*.jpg
ren6v:
	rename.pl 'y/A-Z/a-z/;s/mvi_/v6c0/' $(ROOT)*.MOV* $(ROOT)*.mov*

# vim:ts=4:sw=4:noexpandtab
