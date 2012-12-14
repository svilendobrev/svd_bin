all: ren
	$(MAKE) -f $(MAKEFILE_LIST) opt
ren:
	rename.pl 'y/A-Z/a-z/;s/_/1/' *JPG *jpg

ROOT ?= ./
OPTs=$(wildcard $(ROOT)*.jpg)

opt1: OPTs=$(wildcard $(ROOT)*.JPG)
opt1: opt

opt: $(OPTs:%.jpg=%.opt)
%.opt: %.jpg
	jhead $< | grep -i progressive || jpegtran -optimize -progressive -copy all $< >$@
#	diff -q $@ $< && rm $@ || mv -f $@ $<

OPT2s=$(wildcard $(ROOT)*.opt)
opt2jpg: $(OPT2s:%.opt=%.opt2)
%.opt2: %.opt
	cp $< $*.jpg ; rm $<

opt3: $(OPTs:%.jpg=%.opt3)
%.opt3: %.jpg
	/snimki/optimizejpg.sh $<

2: $(OPTs:%.jpg=2/%.jpg)
2/%.jpg: %.jpg
	/snimki/2small.sh $<

4: $(OPTs:%.jpg=4/%.jpg)
4/%.jpg: %.jpg
	SCALE=4 /snimki/2small.sh $<

# vim:ts=4:sw=4:noexpandtab
