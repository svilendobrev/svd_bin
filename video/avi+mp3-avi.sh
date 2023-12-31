#!/bin/sh
mau "$1.wav"
mau "$1.mp3"
ffmpeg -i "$1" -i "$1".mp3 -map 1:a -c:a copy -map 0:v -c:v copy "$1".avi
#   42  ffmpeg -i *avi -i *p3 -map 1:a -c:a copy -map 0:v -c:v copy x.avi

#1  cd /media/na/detski/filmi/-kratki/-pixar/malki/
#    2  cp for.the.birds.2000.avi /home/tmp/
#    3  nd x
#    4  mv ../for.the.birds.2000.avi .
#    5  emf
#    6  ema
#    7  man ffmpeg
#    8  cd ~/src/bin/video/
#    9  d variouslib
#   10  t variouslib
#   11  cd -
#   12  e `which menc1 `
#   13  l `which menc1 `
#   14  a-search mencoder
#   15  cd -
#   16  g ffmp *
#   17  g ffmp -R .
#   18  g ffmpe -R .
#   19  mkvextract -h
#   20  cd -
#   21  cd /home/tmp/x/
#   22  mkvextract  *i tracks 1:au.ac3
#   23  mau avi2wav
#   24  ema
#   25  mau for.the.birds.2000.avi.wav
#   26  ema
#   27  mau for.the.birds.2000.avi.wav -r
#   28  mau -r for.the.birds.2000.avi.wav
#   29  alg mau
#   30  e ~/_myalias
#   31  cd /home/qini/
#   32  g -r mau .
#   33  e aliasi/audio.alias.bsh
#   34  mau --he
#   35  cd -
#   36  mau -r -d for.the.birds.2000.avi.wav
#   37  mau for.the.birds.2000.avi.wav
#   38  wav2mp3 *v
#   39  g ffmpe ~/src/bin/
#   40  g ffmpe ~/src/bin/ -r
#   41  ffmpeg -i *avi -i *p3 -map 1:a copy -map 0:v copy x.avi
#   42  ffmpeg -i *avi -i *p3 -map 1:a -c:a copy -map 0:v -c:v copy x.avi
#   43  uu b1
#   44  mm b1
#   45  mv x.avi for.the.birds.2000.mp3.avi
#   46  ren_ *
#   47  mau Вдигнат_\(извънземно_на_изпит\).avi.wav
#   48  mau Престо\!_фокуси\!.2008.avi.wav
#   49  mau
#   50  history >avi+mp3-avi.sh
