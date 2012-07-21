autocmd BufEnter */stc* setl tags-=~/src/stc/tags tags+=~/src/stc/tags
autocmd BufLeave */stc* setl tags-=~/src/stc/tags 
"autocmd BufEnter */hor* setl tags-=~/src/hor-trunk/tags tags+=~/src/hor-trunk/tags
"autocmd BufLeave */hor* setl tags-=~/src/hor-trunk/tags 
if filereadable('.vimrc')
	source .vimrc
endif

