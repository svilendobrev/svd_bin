#$Id$
z: ok/allegro-non-troppo-1977
TOC = fpesni.toc
TITLE = "pesni ot detski filmi-animacia"

all: ok/aristocats.bg
all: ok/puh-winnie
all: ok/puh-hefalump
all: ok/puh-great.day.discovery
all: puh-seasons
all: ok/puh-newyear
all: ok/puh-piglet
all: ok/puh-tigger
#all: ok/puh-grand-adventure

all: robinhud
all: ok/jungle.book
all: ok/open.season
all: ok/pinkpanter
all: ok/volk.i.semero.kozlyat
all: ok/ostrov.sokrovisht--svd
all: ok/um_le_dauphin_blanc
all: ok/barbapapa
all: ok/jamie
all: ok/aristocats.en

aristocats: ok/aristocats.bg ok/aristocats.en
maugli: 	ok/jungle.book
puh-seasons: ok/puh-seasons1 ok/puh-seasons2

robinhud: ok/robin.hud
#robinhud: $(patsubst %,%.mono2stereo,$(wildcard out/robin.hud*/*wav))
%.mono2stereo: %
	ecasound -i:"$<" -o tmp.wav -chcopy 1,2
	mv tmp.wav $<

define HDR
CD_DA \
 CD_TEXT { \
  LANGUAGE_MAP { 0 : EN } \
  LANGUAGE 0 { \
	TITLE $(TITLE) \
  } }
endef
toc: toc0 trytoc
toc0:
	echo '$(HDR)' > $(TOC)
	rm -f ok/*
	$(MAKE) all WAVSPL_FLAGS="-toc=$(TOC) -n"
	chall.pl 's/"aristocats.bg/"aristokotki/g' $(TOC)
	chall.pl 's/"aristocats.en/"aristocats/g' $(TOC)
	chall.pl 's/"robin.hud.bg/"robin hud/g'    $(TOC)
	chall.pl 's/"open.season.bg/"loven sezon/g' $(TOC)
	chall.pl 's/"jungle.book.bg/"maugli/g'     $(TOC)
	chall.pl 's/"puh.great.day.discovery.bg/"puh den za otkritia/g' $(TOC)
	chall.pl 's/"puh.seasons..bg/"puh sezoni/g' $(TOC)
	chall.pl 's/"puh /"puh:/g' $(TOC)
	chall.pl 's/"um_le_dauphin_blanc.*"/"um belia delfin"/g' $(TOC)
	chall.pl 's/"pinkpanter.*"/"pinko"/g' $(TOC)
	chall.pl 's/"barbapapa.*"/"barbapapa"/g' $(TOC)
	chall.pl 's/..svd:.*?kniga//g' $(TOC)
trytoc:
	cdrdao show-toc --speed 8 --simulate $(TOC)

burn burntoc:
	cdrdao write --speed 8 $(TOC)

WAVSPL = $E $(PY) wavspl.py --makedir --path out/ $(WAVSPL_FLAGS)



#curdir
ok/%: %.wav txt/%.txt
	$(WAVSPL) $+
	touch $@
ok/%: %.bg.wav txt/%.txt
	$(WAVSPL) $+
	touch $@
ok/%: %.avi.wav txt/%.txt
	$(WAVSPL) $+
	touch $@

#wav/
ok/%: wav/%.wav txt/%.txt
	$(WAVSPL) $+
	touch $@
ok/%: wav/%.bg.wav txt/%.txt
	$(WAVSPL) $+
	touch $@
ok/%: wav/%.avi.wav txt/%.txt
	$(WAVSPL) $+
	touch $@


ok/aristocats.bg: wav/aristocats.bg.wav txt/aristocats.txt
	$(WAVSPL) $+
	touch $@
ok/aristocats.en: wav/aristocats.en.wav txt/aristocats.txt
	$(WAVSPL) $+ -offset=1.7
	touch $@

%.wav: %.avi
	mplayer -vc null -vo null -ao pcm:fast:file="$@" "$<"

whole.anlz:
	rm -f $@
	for a in wav/*wav; do echo $$a `ecasound -i:$$a -o:null -ev | grep gain` >>$@; done
parts.anlz:
	rm -f $@
	for a in out/*; do wavcat.py -o $$a/all $$a/*wav done
	for a in out/*; do ecasound -i:typeselect,.wav,$$a/all -o:null -ev | grep gain >>$@; done
	rm out/*/all

whole.gain:
	$(PY) gain.py < gains
parts.gain:
	mkdir -p outgain
	cd out; for a in *; do mkdir -p ../outgain/$$a; done
	$(PY) gain.py 'out/%(name)s/*.wav' 'outgain/%(name)s/*.wav' < gains

wav/ampl/%.wav: wav/%.wav #gains
	grep ^$* gains | $(PY) gain.py

all.gain: $(patsubst wav/%.wav,wav/ampl/%.wav,$(wildcard wav/*wav))

tar zip:
	ls -alF --color=none avi/ >avi.list
	ls -alF --color=none wav/ >wav.list
	tar cjf filmi2pesni.tbz --dereference txt *.list *.toc *.py makefile gains *.html www/cd/*.cue www/cd/*.toc
	rm *.list

mp3wrap:
	mp3wrap out/aristocats.bg/vseki-iska-da-e-kotarak.all.mp3 	out/aristocats.bg/[456]*3
	mp3wrap out/aristocats.en/vseki-iska-da-e-kotarak.all.mp3 	out/aristocats.en/[456]*3
	mp3wrap out/jamie/begin-torch.all.mp3						out/jamie/[12]*3
	mp3wrap out/jungle.book.bg/vazhnite-neshta.o.all.mp3 		out/jungle.book.bg/?.vazhnite-neshta.o?.*3
	mp3wrap out/puh-hefalump/we-stand.all.mp3 					out/puh-hefalump/[23]*3
	mp3wrap out/puh-seasons1.bg/meco-puh-nov-sezon.all.mp3		out/puh-seasons1.bg/[12]*3
	mp3wrap out/puh-winnie/winnie-the-pooh.all.mp3 				out/puh-winnie/0[12]*3
	mp3wrap out/volk.i.semero.kozlyat/volk.all.mp3 				out/volk.i.semero.kozlyat/[23]*3

list:
	echo $(TITLE) > $@
	perl -ne 'print if s/^ *TITLE//' < $(TOC) | cat -b >> $@

list2: makefile
	echo $(TITLE) > $@
	perl -ne 'print if s/^ *TITLE(.*)\n/\1/ || s/^ *FILE(.*) 0/\1/' < $(TOC) | cat -b >> $@

# vim:ts=4:sw=4:noexpandtab
