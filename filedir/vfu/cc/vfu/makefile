
default: all
re: rebuild
li: link
all: vfu
clean: clean-vfu
rebuild: rebuild-vfu
link: link-vfu

AR = ar rv
MKDIR = mkdir -p
RMDIR = rm -rf
RMFILE = rm -f

### TARGET 1: vfu ##############################################################

CC_1       = g++
LD_1       = g++
AR_1       = ar rv
RANLIB_1   = ranlib
CCFLAGS_1  = -I../vslib -I../vslib/pcre -I/usr/include/ncurses -O2 $(CCDEF) -fpermissive
LDFLAGS_1  = -L../vslib -L../vslib/pcre -lvslib -lvscon -lpcre -lncursesw $(LDDEF)
DEPFLAGS_1 =
ARFLAGS_1  =
TARGET_1   = vfu

SRC_1= \
     see.cpp \
     vfu.cpp \
     vfuarc.cpp \
     vfucopy.cpp \
     vfudir.cpp \
     vfufiles.cpp \
     vfumenu.cpp \
     vfuopt.cpp \
     vfusys.cpp \
     vfutools.cpp \
     vfuuti.cpp \
     vfuview.cpp \

OBJ_1= $(SRC_1:%.cpp=.OBJ.vfu/%.o)

### TARGET DEFINITION FOR TARGET 1: vfu ########################################

.OBJ.vfu:
	$(MKDIR) .OBJ.vfu

vfu:  .OBJ.vfu $(OBJ_1) ../vslib/libvslib.a ../vslib/libvscon.a ../vslib/pcre/libpcre.a
	$(LD_1) $(OBJ_1) $(LDFLAGS_1) -o $(TARGET_1)

zz: .OBJ.vfu/zz.o
	$(LD_1) $+ $(LDFLAGS_1) -o $@

clean-vfu:
	$(RMFILE) $(TARGET_1)
	$(RMDIR) .OBJ.vfu

rebuild-vfu: clean-vfu vfu

link-vfu: .OBJ.vfu $(OBJ_1)
	$(RMFILE) vfu
	$(LD_1) $(OBJ_1) $(LDFLAGS_1) -o $(TARGET_1)

.OBJ.vfu/%.o : %.cpp
	$(CC_1) $(CFLAGS_1) $(CCFLAGS_1) -c $< -o $@


### TARGET OBJECTS FOR TARGET 1: vfu ###########################################

.OBJ.vfu/see.o: see.cpp  see.cpp see.h
.OBJ.vfu/vfu.o: vfu.cpp  vfu.cpp vfu.h vfusetup.h vfusys.h vfuopt.h see.h vfuuti.h vfufiles.h vfucopy.h vfudir.h vfuview.h vfumenu.h vfuarc.h vfutools.h
.OBJ.vfu/vfuarc.o: vfuarc.cpp  vfuarc.cpp vfuarc.h vfu.h vfusetup.h vfusys.h vfuuti.h vfuopt.h see.h vfudir.h vfucopy.h vfufiles.h
.OBJ.vfu/vfucopy.o: vfucopy.cpp  vfucopy.cpp vfu.h vfusetup.h vfusys.h vfudir.h vfumenu.h vfuuti.h vfufiles.h vfuview.h vfuopt.h see.h vfucopy.h
.OBJ.vfu/vfudir.o: vfudir.cpp  vfudir.cpp vfudir.h vfu.h vfusetup.h vfusys.h vfuopt.h see.h vfuuti.h vfufiles.h vfuview.h vfumenu.h
.OBJ.vfu/vfufiles.o: vfufiles.cpp  vfufiles.cpp vfu.h vfusetup.h vfusys.h vfufiles.h vfuopt.h see.h vfuuti.h vfuview.h vfumenu.h vfudir.h
.OBJ.vfu/vfumenu.o: vfumenu.cpp  vfumenu.cpp vfu.h vfusetup.h vfusys.h vfuopt.h see.h vfuuti.h vfumenu.h vfuview.h
.OBJ.vfu/vfuopt.o: vfuopt.cpp  vfuopt.cpp vfu.h vfusetup.h vfusys.h vfuopt.h see.h vfuuti.h vfudir.h vfuview.h vfumenu.h
.OBJ.vfu/vfusys.o: vfusys.cpp  vfusys.cpp vfu.h vfusetup.h vfusys.h vfuuti.h vfumenu.h
.OBJ.vfu/vfutools.o: vfutools.cpp  vfutools.cpp vfumenu.h vfuuti.h vfu.h vfusetup.h vfusys.h vfucopy.h vfuview.h vfuopt.h see.h vfufiles.h vfutools.h
.OBJ.vfu/vfuuti.o: vfuuti.cpp  vfuuti.cpp vfu.h vfusetup.h vfusys.h vfuuti.h vfumenu.h vfudir.h vfuopt.h see.h vfuview.h
.OBJ.vfu/vfuview.o: vfuview.cpp  vfuview.cpp vfu.h vfusetup.h vfusys.h vfufiles.h vfuview.h vfuopt.h see.h vfuuti.h


### MAKEMAKE ENDS HERE #########################################################

