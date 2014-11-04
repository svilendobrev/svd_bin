all: mp3 flac

ifneq ($(MONO),)
OPTS+=-m m
endif
%.flac: %.wav
	flac --force -o "$@" "$<"
LAME= lame --nohist --disptime 2 -h -v -V 6 $(OPTS)

%.mp36: %.mp3
	$(LAME) "$<" "$@"
#%.mp3: %.wav
#	$(LAME) "$<" "$@"
#%.mp3: %.flac
#	flac -d "$<" -o - | $(LAME) - "$@"

%.wav: %.flac
	flac -d -o "$@" "$<"
%.wav: %.mp3
	lame --decode --nohist --quiet "$<" "$@"

%.mkv: %.wmv
	ffmpeg -i "$<" "$@"
VQ=-sameq
%.avi: %.mkv
	ffmpeg -i "$<" $(VQ) -acodec copy "$@"
%.mkv: %.avi
	mkvmerge $< -o $@


ROOT=./
WAVs = $(wildcard $(ROOT)*.wav)
MP3s = $(wildcard $(ROOT)*.mp3)
FLACs = $(wildcard $(ROOT)*.flac)
flac: $(WAVs:%.wav=%.flac)
mp3 : $(WAVs:%.wav=%.mp3)
mp36: mp3mp3
mp3mp3 : $(patsubst %.mp3,%.mp36,$(wildcard $(ROOT)*.mp3))
363:
	rename.pl s/mp36/mp3/ *mp36

flacwav: $(FLACs:%.flac=%.wav)
flac2mp3: $(FLACs:%.flac=%.mp3)
mp3wav : $(MP3s:%.mp3=%.wav)
flac2wav: flacwav
mp32wav:  mp3wav
wav: $(FLACs:%.flac=%.wav) $(MP3s:%.mp3=%.wav)

#WMVs= $(wildcard *.wmv)
#wmv2mkv: $(WMVs:%.wmv=%.mkv)
wmv2mkv: $(patsubst %.wmv,%.mkv,$(wildcard *.wmv))
mkv2avi: $(patsubst %.mkv,%.avi,$(wildcard *.mkv))
avi2mkv: $(patsubst %.avi,%.mkv,$(wildcard *.avi))

wavcat:
	wavcat.py -o ooo.wav $(WAVs)

SPLIT= $(wildcard $(WILD)$(SWILD))
split: $(SPLIT:%=./mm.%-001.mkv)

T?=0:0:20 #,0:4:30
./mm.%-001.mkv: #./%
	mkvmerge "$*" -o "mm.$*" --split timecodes:$T

#export MKVTOOLNIX_OPTIONS=".. .."
# mkvmerge --disable-track-statistics-tags

tags:
	for a in *tags; do sh $$a; done


%.ac3: %.wav
	aften $< $@
%.avi.wav: %.avi
	mplayer -vc null -vo null -ao pcm:fast:file="$@" "$<"
#	mp2wav $< $@

#удължаване: PERC<100.0
#скъсяване : PERC>100.0
%.pitch.wav : %.wav
	ecasound -i:"$<" -o "$@" -ei:$(PERC)
.PRECIOUS: %.pitch.wav

#RESAMPLE=1
_RESAMPLE = resample,auto,
_MONO2STEREO = -chcopy 1,2
mono2stereo.%:
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*" -o "$@" $(_MONO2STEREO)
eca.%:
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*" -o "$@" $(if $(PERC),-ei:$(PERC)) $(if $(MONO2STEREO)$(STEREO),$(_MONO2STEREO))

#!!без , ( ) в имената..
mono2stereo: $(patsubst %.wav,mono2stereo.%.wav,$(wildcard $(WILD)*.wav))
#	echo "$+"
eca: $(patsubst %.wav,eca.%.wav,$(wildcard $(WILD)*.wav))
#	echo "$+"
2x44: stereo-resample
stereo-resample: mono2stereo
stereo-resample: RESAMPLE=1

izv:
	$(PY) ~/src/bin/audio/izvadki/wavspl.py *izv*

FILMs= $(wildcard $(SFILM))
filmid: $(FILMs:%=%.filmid)
%.filmid: %
	filmid.sh "$<" >"$@"

bz bz2: $(patsubst %,%.bz2,$(wildcard $(BZ)))
%.bz2: %
	bzip2 $<

# vim:ts=4:sw=4:noexpandtab
