#$Id: makefile,v 1.10 2005/09/08 10:48:23 sdobrev Exp $

IGNORE_PATTERNS += "\\\$$Id:"
IGNORE_PATTERNS += "\\\$$Header:"
TARGET = stc
SOURCE_RIGHT = /mnt/srv/pub/wincor-nixdorf/in.wn.cvs/stc

EXCLUDE += java_gui develop
EXCLUDE += *.proj *.snprj *.tpr *.dfState .dummy *.removed
EXCLUDE += *.solibs *.so *.gen CVS [Mm]akefile* *.class
EXCLUDE += Agreements.xls
EXCLUDE += *.pdf
#AllComponents.cfg #CnProcessInfo.*
EXCLUDE += gui_server5 gui_server_common_old gui_server2 #gui_server1
EXCLUDE += bmcstest snifferstart consoletest
EXCLUDE += newmakes.tar.bz  old
#EXCLUDE += linux_*

#EXCLUDE += customer
#DOlib += common
#DOlib += ticket
#DOlib += handler
#DOlib += bmcs_factory
#DOsrv += operationmode
#DOsrv += console
#DOsrv += status
#DOsrv += sign
#DOsrv += custdisplay
#DOsrv += password
#DOsrv += game
#EXCLUDE += $(DOlib:%=%_lib) $(DOsrv:%=%*)

EXCLUDE += *cification.pdf
#EXCLUDE += StartUp.cfg TCP*.cfg
EXCLUDE += CnArchive_Co.* testArchive.*

EXCLUDE += customer
EXCLUDE += new	#base/general

#wn-base stuff
EXCLUDE += Changelog.txt Application.cfg.txt .\#*
#EXCLUDE += barcode_reader* smartcard* multim* java_tool* io_port* customer_di*
#EXCLUDE += $(patsubst %,printer_%,exe lib uti)
#EXCLUDE += $(patsubst %,reader_%,exe lib uti gui)
#wn-system stuff
#EXCLUDE += xisec* versi* messag* *old dl_* download_[au]* *.tpr test sys_c_*
EXCLUDE += sys_c_* noti*
#EXCLUDE += *gecko* vga*


#ECHO = sayparms.sh
EXT = .diff
TODATE = $(shell echo `date +%m%d`)
RESULT = p$(TODATE)$(EXT)

all: head.dir branch.dir branch.cvsup diff bins

.PHONY: _always

diff: $(RESULT) bins #.diff
%.dir:
	@mkdir -p $*
%.cvsup:
	-cd $*/$(TARGET); cvs up -dP 2>/dev/null | grep "^[?A-Z] "
%.diff: _always
	- cd branch/$(TARGET); $(ECHO) diff -N -up -r $(IGNORE_PATTERNS:%=-I %) $(EXCLUDE:%=-x '%') . $(SOURCE_RIGHT) > ../../$@
bins:
	@echo $(RESULT)
	@ls -lF $(RESULT)
	- grep "^Binary files" $(RESULT)

ifndef PATCH
PATCH=$(RESULT)#.diff
endif
patch: do_patch check-$(PATCH)
do_patch: #$(PATCH) 			#-p7 = 1+number of /'s in $(SOURCE_RIGHT)
	@ls -lF $(PATCH)
	@( read -p 'patch from '$(PATCH)' ?' -n 1 && [ "$$REPLY" = "y" ] && echo ''  ) || (echo ' canceled ' && false)
	cd branch/$(TARGET); patch --verbose -p7 <../../$(PATCH)

merge: head.cvsup
	@( read -p 'merge ?' -n 1 && [ "$$REPLY" = "y" ] && echo ''  ) || (echo ' canceled ' && false)
#	cd head; cvs co -j wincor-nixdorf stc
	cd head/$(TARGET); cvs up -dP -j wincor-nixdorf
	@echo cvs up:
	-cd head/$(TARGET); cvs up -dP 2>/dev/null | grep "^[?A-Z] "


IMPORT_ignore = *.tpr *.proj *.snprj Makefile* doc  *Archive* CVS $(IMPORT_ignore0)
#java_gui:
JAVA_IMPORT_ignore = *.java  applet log4j xml src images

base.importall: 	IMPORT_include = general
system.importall: 	IMPORT_include ?= [eglprt]* download_task* data_* ipc
#exclude state_compiler, sys_c*, ...	#java_gui
cfg.importall: 		IMPORT_include = gui_server1 gui_server_common
toolkit.importall: 	IMPORT_include = [lm]*

MAKEIT = $(MAKE) -f $(firstword $(MAKEFILE_LIST))

gui.importall:
	$(MAKEIT) IMPORT_include=gui\* system.importall
java.importall:
	$(MAKEIT) IMPORT_include=java\* IMPORT_ignore0="$(JAVA_IMPORT_ignore)" system.importall
systemsub.importall:
	$(MAKEIT) IMPORT_include="map* down* udp*" system.importall
sub.importall: systemsub.importall
	$(MAKEIT) server.import

%.importall:
	@echo "$@: $(IMPORT_include:%=$*/%)"
	@cd $(SOURCE_RIGHT); ls -d $(IMPORT_include:%=$*/%)
	@echo "===ignore: $(IMPORT_ignore)"
	$(MAKEIT) $(patsubst $(SOURCE_RIGHT)/%,%.import, $(wildcard $(IMPORT_include:%=$(SOURCE_RIGHT)/$*/%)))

#$(SOURCE_RIGHT)/
%.import:
	@echo import $@
	cd $(SOURCE_RIGHT)/$*; [ -n "$$WHAT" ] || cvs import -d $(IMPORT_ignore:%=-I "%") -m t$(TODATE) stc/$* wincor-nixdorf a$(TODATE)

import: base.importall system.importall cfg.importall

# vim:ts=4:sw=4:noexpandtab
