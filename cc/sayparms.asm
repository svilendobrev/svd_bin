; args
PSP_CMD = 080h
        mov si, PSP_CMD
        lodsb           ;get cmdline size; cmd line follows
        sub bx,bx
        mov bl,al

ifdef USE_DOS_FN9
        mov word ptr [si+bx], 0240ah  ;term.  \n$
        mov dx,si
        mov ah,9
        int 021h        ;print - up to $

else    ;USE_BIOS_10
        push bx         ;save sz
        mov ah,0fh      ;get mode/ bh=page
        int 010h
        mov ah,3        ;get cursor
        int 010h
        mov bl, 7       ;white on black
        mov bp,si       ;ofs
        pop cx          ;sz
        mov ax,01301h   ;func13 print, subfunc 1 leave cursor @ eostring
        int 010h
endif
        mov ah,04ch
        int 021h
