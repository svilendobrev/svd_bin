#!/bin/sh
chall.pl 's/(OrderOfArrival)=.*/\1=false/g' 	~/.kde/share/config/kmailrc
chall.pl 's/(\n\[Folder-[\s\S]+?\nSortColumn)=.*/\1=-3/g' 		~/.kde/share/config/kmailrc
chall.pl 's/(threadMessagesBySubject)=.*/\1=true/g' 	~/.kde/share/config/kmailrc
chall.pl 's/(threadMessagesOverride)=.*/\1=false/g' 	~/.kde/share/config/kmailrc
test "$1" = icon && chall.pl 's/(NormalIconPath|UnreadIconPath)=.*/\1=music_fullnote/g' 			~/.kde/share/config/kmailrc
test "$1" = icon && chall.pl 's/(UseCustomIcons)=.*/\1=true/g' 		~/.kde/share/config/kmailrc
