
### MAKEMAKE STARTS HERE #######################################################


### Created by makemake.pl on Wed Dec 29 04:46:52 2004 #########################


### GLOBAL TARGETS #############################################################

default: all

re: rebuild

li: link

all: modules libvslib.a libvscon.a test 

clean: clean-modules clean-libvslib.a clean-libvscon.a clean-test 

rebuild: rebuild-modules rebuild-libvslib.a rebuild-libvscon.a rebuild-test 

link: link-modules link-libvslib.a link-libvscon.a link-test 

### GLOBAL (AND USER) DEFS #####################################################


AR = ar rv
CC = g++
LD = g++
MKDIR = mkdir -p
MODULES = pcre
RANLIB = ranlib
RMDIR = rm -rf
RMFILE = rm -f
SRC = *.c *.cpp *.cc *.cxx


### TARGET 1: libvslib.a #######################################################

CC_1       = g++
LD_1       = g++
AR_1       = ar rv
RANLIB_1   = ranlib
CCFLAGS_1  = -I. -Ipcre -O2 $(CCDEF) 
LDFLAGS_1  = $(LDDEF)
DEPFLAGS_1 = 
ARFLAGS_1  = 
TARGET_1   = libvslib.a

### SOURCES FOR TARGET 1: libvslib.a ###########################################

SRC_1= \
     clusters.cpp \
     dlog.cpp \
     eval.cpp \
     fnmatch2.cpp \
     getopt2.cpp \
     scroll.cpp \
     vslib.cpp \
     vstring.cpp \
     vstrlib.cpp \
     vsuti.cpp \
     vscrc.cpp \

#### OBJECTS FOR TARGET 1: libvslib.a ##########################################

OBJ_1= \
     .OBJ.libvslib.a/clusters.o \
     .OBJ.libvslib.a/dlog.o \
     .OBJ.libvslib.a/eval.o \
     .OBJ.libvslib.a/fnmatch2.o \
     .OBJ.libvslib.a/getopt2.o \
     .OBJ.libvslib.a/scroll.o \
     .OBJ.libvslib.a/vslib.o \
     .OBJ.libvslib.a/vstring.o \
     .OBJ.libvslib.a/vstrlib.o \
     .OBJ.libvslib.a/vsuti.o \
     .OBJ.libvslib.a/vscrc.o \

### TARGET DEFINITION FOR TARGET 1: libvslib.a #################################

.OBJ.libvslib.a: 
	$(MKDIR) .OBJ.libvslib.a

libvslib.a:  .OBJ.libvslib.a $(OBJ_1)
	$(AR_1) $(ARFLAGS_1) $(TARGET_1) $(OBJ_1)
	$(RANLIB_1) $(TARGET_1)

clean-libvslib.a: 
	$(RMFILE) $(TARGET_1)
	$(RMDIR) .OBJ.libvslib.a

rebuild-libvslib.a: clean-libvslib.a libvslib.a

link-libvslib.a: .OBJ.libvslib.a $(OBJ_1)
	$(RMFILE) libvslib.a
	$(AR_1) $(ARFLAGS_1) $(TARGET_1) $(OBJ_1)
	$(RANLIB_1) $(TARGET_1)


### TARGET OBJECTS FOR TARGET 1: libvslib.a ####################################

.OBJ.libvslib.a/clusters.o: clusters.cpp  clusters.cpp clusters.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c clusters.cpp         -o .OBJ.libvslib.a/clusters.o
.OBJ.libvslib.a/dlog.o: dlog.cpp  dlog.cpp dlog.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c dlog.cpp             -o .OBJ.libvslib.a/dlog.o
.OBJ.libvslib.a/eval.o: eval.cpp  eval.cpp eval.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c eval.cpp             -o .OBJ.libvslib.a/eval.o
.OBJ.libvslib.a/fnmatch2.o: fnmatch2.cpp  fnmatch2.cpp fnmatch2.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c fnmatch2.cpp         -o .OBJ.libvslib.a/fnmatch2.o
.OBJ.libvslib.a/getopt2.o: getopt2.cpp  getopt2.cpp getopt2.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c getopt2.cpp          -o .OBJ.libvslib.a/getopt2.o
.OBJ.libvslib.a/scroll.o: scroll.cpp  scroll.cpp scroll.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c scroll.cpp           -o .OBJ.libvslib.a/scroll.o
.OBJ.libvslib.a/vslib.o: vslib.cpp  vslib.cpp
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c vslib.cpp            -o .OBJ.libvslib.a/vslib.o
.OBJ.libvslib.a/vstring.o: vstring.cpp  vstring.cpp vstring.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c vstring.cpp          -o .OBJ.libvslib.a/vstring.o
.OBJ.libvslib.a/vstrlib.o: vstrlib.cpp  vstrlib.cpp vstrlib.h vstring.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c vstrlib.cpp          -o .OBJ.libvslib.a/vstrlib.o
.OBJ.libvslib.a/vsuti.o: vsuti.cpp  vsuti.cpp vsuti.h target.h vstring.h vstrlib.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c vsuti.cpp            -o .OBJ.libvslib.a/vsuti.o
.OBJ.libvslib.a/vscrc.o: vscrc.cpp  vscrc.cpp vsuti.h target.h vstring.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c vscrc.cpp            -o .OBJ.libvslib.a/vscrc.o


### TARGET 2: libvscon.a #######################################################

CC_2       = g++
LD_2       = g++
AR_2       = ar rv
RANLIB_2   = ranlib
CCFLAGS_2  = -I. -Ipcre -I/usr/include/ncurses -O2 $(CCDEF) 
LDFLAGS_2  = $(LDDEF)
DEPFLAGS_2 = 
ARFLAGS_2  = 
TARGET_2   = libvscon.a

### SOURCES FOR TARGET 2: libvscon.a ###########################################

SRC_2= \
     ansiterm.cpp \
     conmenu.cpp \
     form_in.cpp \
     unicon.cpp \

#### OBJECTS FOR TARGET 2: libvscon.a ##########################################

OBJ_2= \
     .OBJ.libvscon.a/ansiterm.o \
     .OBJ.libvscon.a/conmenu.o \
     .OBJ.libvscon.a/form_in.o \
     .OBJ.libvscon.a/unicon.o \

### TARGET DEFINITION FOR TARGET 2: libvscon.a #################################

.OBJ.libvscon.a: 
	$(MKDIR) .OBJ.libvscon.a

libvscon.a:  .OBJ.libvscon.a $(OBJ_2)
	$(AR_2) $(ARFLAGS_2) $(TARGET_2) $(OBJ_2)
	$(RANLIB_2) $(TARGET_2)

clean-libvscon.a: 
	$(RMFILE) $(TARGET_2)
	$(RMDIR) .OBJ.libvscon.a

rebuild-libvscon.a: clean-libvscon.a libvscon.a

link-libvscon.a: .OBJ.libvscon.a $(OBJ_2)
	$(RMFILE) libvscon.a
	$(AR_2) $(ARFLAGS_2) $(TARGET_2) $(OBJ_2)
	$(RANLIB_2) $(TARGET_2)


### TARGET OBJECTS FOR TARGET 2: libvscon.a ####################################

.OBJ.libvscon.a/ansiterm.o: ansiterm.cpp  ansiterm.cpp ansiterm.h
	$(CC_2) $(CFLAGS_2) $(CCFLAGS_2) -c ansiterm.cpp         -o .OBJ.libvscon.a/ansiterm.o
.OBJ.libvscon.a/conmenu.o: conmenu.cpp  conmenu.cpp conmenu.h
	$(CC_2) $(CFLAGS_2) $(CCFLAGS_2) -c conmenu.cpp          -o .OBJ.libvscon.a/conmenu.o
.OBJ.libvscon.a/form_in.o: form_in.cpp  form_in.cpp form_in.h unicon.h target.h vstring.h clusters.h \
  scroll.h
	$(CC_2) $(CFLAGS_2) $(CCFLAGS_2) -c form_in.cpp          -o .OBJ.libvscon.a/form_in.o
.OBJ.libvscon.a/unicon.o: unicon.cpp  unicon.cpp unicon.h target.h
	$(CC_2) $(CFLAGS_2) $(CCFLAGS_2) -c unicon.cpp           -o .OBJ.libvscon.a/unicon.o


### TARGET 3: test #############################################################

CC_3       = g++
LD_3       = g++
AR_3       = ar rv
RANLIB_3   = ranlib
CCFLAGS_3  = -g -I. -Ipcre $(CCDEF) -DTEST 
LDFLAGS_3  = -g -L. -Lpcre -lvslib -lvscon -lpcre -lncurses $(LDDEF)
DEPFLAGS_3 = 
ARFLAGS_3  = 
TARGET_3   = test

### SOURCES FOR TARGET 3: test #################################################

SRC_3= \
     test.cpp \

#### OBJECTS FOR TARGET 3: test ################################################

OBJ_3= \
     .OBJ.test/test.o \

### TARGET DEFINITION FOR TARGET 3: test #######################################

.OBJ.test: 
	$(MKDIR) .OBJ.test

test: libvslib.a .OBJ.test $(OBJ_3)
	$(LD_3) $(OBJ_3) $(LDFLAGS_3) -o $(TARGET_3)

clean-test: 
	$(RMFILE) $(TARGET_3)
	$(RMDIR) .OBJ.test

rebuild-test: clean-test test

link-test: .OBJ.test $(OBJ_3)
	$(RMFILE) test
	$(LD_3) $(OBJ_3) $(LDFLAGS_3) -o $(TARGET_3)


### TARGET OBJECTS FOR TARGET 3: test ##########################################

.OBJ.test/test.o: test.cpp  test.cpp vstrlib.h vstring.h
	$(CC_3) $(CFLAGS_3) $(CCFLAGS_3) -c test.cpp             -o .OBJ.test/test.o


### MODULES ####################################################################

modules:
	make -C pcre 

clean-modules:
	make -C pcre clean

rebuild-modules:
	make -C pcre rebuild

link-modules:
	make -C pcre link


### MAKEMAKE ENDS HERE #########################################################

