#!/bin/sh
for P in "$@"; do
	cd -- "$P"
	rename 's/JPG$/jpg/' *.JPG
	rm -rf [sS]ample
	if [ ! -s folder.jpg ]; then
		for a in ./*.jpg; do
			rename -v 's,/[^/]+.jpg,/folder.jpg,' "$a"
			break
			done
	fi
	for a in *.rar *.zip; do xx "$a"; done
	rm -f -- *README* index.*
	rm -rf -- [Ss]ample
	#rm -f *.rar

	ls -lF
	cd -
done
