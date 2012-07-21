all: ren
	$(MAKE) -f $(MAKEFILE_LIST) opt
ren:
	rename.pl 'y/A-Z/a-z/;s/_/1/' *JPG *jpg

OPTs=$(wildcard *.jpg)

opt1: OPTs=$(wildcard *.JPG)
opt1: opt

opt: $(OPTs:%.jpg=%.opt)
%.opt: %.jpg
	jpegtran -optimize -progressive -copy all $< >$@
	diff -q $@ $< && rm $@ || mv -f $@ $<
# vim:ts=4:sw=4:noexpandtab
