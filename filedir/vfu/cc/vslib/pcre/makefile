
### MAKEMAKE STARTS HERE #######################################################


### Created by makemake.pl on Wed Dec 29 04:47:29 2004 #########################


### GLOBAL TARGETS #############################################################

default: all

re: rebuild

li: link

all: libpcre.a 

clean: clean-libpcre.a 

rebuild: rebuild-libpcre.a 

link: link-libpcre.a 

### GLOBAL (AND USER) DEFS #####################################################


AR = ar rv
CC = gcc
LD = gcc
MKDIR = mkdir -p
RANLIB = ranlib
RMDIR = rm -rf
RMFILE = rm -f
SRC = *.c *.cpp *.cc *.cxx


### TARGET 1: libpcre.a ########################################################

CC_1       = gcc
LD_1       = gcc
AR_1       = ar rv
RANLIB_1   = ranlib
CCFLAGS_1  = -I. -O2 $(CCDEF) 
LDFLAGS_1  = $(LDDEF)
DEPFLAGS_1 = 
ARFLAGS_1  = 
TARGET_1   = libpcre.a

### SOURCES FOR TARGET 1: libpcre.a ############################################

SRC_1= \
     chartables.c \
     get.c \
     pcre.c \
     pcreposix.c \
     study.c \

#### OBJECTS FOR TARGET 1: libpcre.a ###########################################

OBJ_1= \
     .OBJ.libpcre.a/chartables.o \
     .OBJ.libpcre.a/get.o \
     .OBJ.libpcre.a/pcre.o \
     .OBJ.libpcre.a/pcreposix.o \
     .OBJ.libpcre.a/study.o \

### TARGET DEFINITION FOR TARGET 1: libpcre.a ##################################

.OBJ.libpcre.a: 
	$(MKDIR) .OBJ.libpcre.a

libpcre.a:  .OBJ.libpcre.a $(OBJ_1)
	$(AR_1) $(ARFLAGS_1) $(TARGET_1) $(OBJ_1)
	$(RANLIB_1) $(TARGET_1)

clean-libpcre.a: 
	$(RMFILE) $(TARGET_1)
	$(RMDIR) .OBJ.libpcre.a

rebuild-libpcre.a: clean-libpcre.a libpcre.a

link-libpcre.a: .OBJ.libpcre.a $(OBJ_1)
	$(RMFILE) libpcre.a
	$(AR_1) $(ARFLAGS_1) $(TARGET_1) $(OBJ_1)
	$(RANLIB_1) $(TARGET_1)


### TARGET OBJECTS FOR TARGET 1: libpcre.a #####################################

.OBJ.libpcre.a/chartables.o: chartables.c  chartables.c
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c chartables.c         -o .OBJ.libpcre.a/chartables.o
.OBJ.libpcre.a/get.o: get.c  get.c internal.h config.h pcre.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c get.c                -o .OBJ.libpcre.a/get.o
.OBJ.libpcre.a/pcre.o: pcre.c  pcre.c internal.h config.h pcre.h chartables.c
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c pcre.c               -o .OBJ.libpcre.a/pcre.o
.OBJ.libpcre.a/pcreposix.o: pcreposix.c  pcreposix.c internal.h config.h pcre.h pcreposix.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c pcreposix.c          -o .OBJ.libpcre.a/pcreposix.o
.OBJ.libpcre.a/study.o: study.c  study.c internal.h config.h pcre.h
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c study.c              -o .OBJ.libpcre.a/study.o


### MAKEMAKE ENDS HERE #########################################################

