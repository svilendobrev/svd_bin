export CCDEF=-D_FILE_OFFSET_BITS=64 -fpermissive

### GLOBAL TARGETS #############################################################
default: all
re: rebuild
li: link
all: modules
clean: clean-modules
rebuild: rebuild-modules
link: link-modules

MKDIR = mkdir -p
MODULES = vslib vfu
RMDIR = rm -rf
RMFILE = rm -f
SRC = *.c *.cpp *.cc *.cxx


### MODULES ####################################################################

modules:
	$(MAKE) -C vslib
	$(MAKE) -C vfu

clean-modules:
	$(MAKE) -C vslib clean
	$(MAKE) -C vfu clean

rebuild-modules:
	$(MAKE) -C vslib rebuild
	$(MAKE) -C vfu rebuild

link-modules:
	$(MAKE) -C vslib link
	$(MAKE) -C vfu link


### MAKEMAKE ENDS HERE #########################################################

