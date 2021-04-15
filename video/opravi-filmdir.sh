#!/bin/sh
shopt -s nullglob
for P in "$@"; do
    cd -- "$P"
    rename 's/JPG$/jpg/' *.JPG
    if [ ! -s folder.jpg ]; then
        for a in ./*.jpg; do
            ln -f "$a" folder.jpg
            #rename -v 's,/[^/]+.jpg,/folder.jpg,' "$a"
            break
            done
        fi
    for a in *.rar *.zip; do xx "$a"; done
    for a in ./*.mkv ./*.avi ./*.mp4; do
        echo "$a" | grep -i sample > /dev/null && continue
        #for b in ./*.srt; do
#            ln -f "$b" `perl -e '$_=$ARGV[0]; s/\.[^.]+$/.srt/ ; print ' "$a"`
        #    break
        #    done
        python3 -c "import os,sys; a,b=sys.argv[1:3]; os.link( b, os.path.splitext( a)[0]+'.srt')" "$a" ./*.srt
        break
        done

    ls -lF
    cd -
done

# vim:ts=4:sw=4:expandtab
