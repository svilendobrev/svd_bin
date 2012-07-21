" Vim filetype detection file
" Language:	Taskpaper (http://hogbaysoftware.com/projects/taskpaper)
" Maintainer:	David O'Callaghan <david.ocallaghan@cs.tcd.ie>
" URL:		http://www.cs.tcd.ie/David.OCallaghan/taskpaper.vim/
" Version:	1
" Last Change:  2007 Sep 25
"
augroup taskpaper
  au!
  au BufRead,BufNewFile *.taskpaper   setfiletype taskpaper
  au FileType taskpaper  setlocal iskeyword+=@-@ foldmethod=syntax foldlevel=99 nofoldenable
  au FileType taskpaper  map <buffer> <silent> <LocalLeader>td <Plug>ToggleDone
  au FileType taskpaper  map <buffer> <silent> <LocalLeader>tc <Plug>ShowContext
"use zR  au! FileType taskpaper  map <buffer> <silent> <LocalLeader>ta <Plug>ShowAll
"use ZM  au! FileType taskpaper  map <buffer> <silent> <LocalLeader>tp <Plug>FoldAllProjects
augroup END
"helptags ~/.vim/doc
