
set previewheight=12

if !exists('g:trv_minStrLen')	" minimum length of string too be translated
    let g:trv_minStrLen = 3
endif
if !exists('g:trv_editcmd')     " split pedit edit
    let g:trv_editcmd = 'pedit'
endif

if !exists('g:trv_prog')       "func/program( text) to exec
 " search phrase in dictionary, write result in temporary file
 function! g:trv_prog(str)
    let s:tmpfile1= tempname()
    let s:tmpfile = tempname()
    let y = system( "echo \"".a:str."\" | enconv -x cp1251 > " . s:tmpfile1)
    let x = system( "cbedic `cat " .s:tmpfile1.   "` > ". s:tmpfile )
	return s:tmpfile
 endfunction
endif

"** Translate string "str". If there is no string, ask for word/phrase.
function! s:TransVim(str)
    let s:txt = a:str
    if s:txt == ""                     " is there a string to search for?
    	let s:txt = input("Translate: ")
    endif
    call s:Translate(s:txt)        " translate
endfunction

function! s:Translate(str)
    " search phrase, write result in temporary file, edit it
    if strlen(a:str) < g:trv_minStrLen   " is string long enough?
        call s:Error(1)
        return
    endif

    let s:tmpfile = g:trv_prog( a:str)
    execute g:trv_editcmd . " " . s:tmpfile

    if has('win32')
        call delete(s:tmpfile)
    endif
endfunction

" the mappings:
if !hasmapto('<Plug>TRV_TransVimVisual')
    vmap <silent> <unique> <Leader>tr <Plug>TRV_TransVimVisual
endif
if !hasmapto('<Plug>TRV_TransVimNormal')
    nmap <silent> <unique> <Leader>tr <Plug>TRV_TransVimNormal
endif
if !hasmapto('<Plug>TRV_TransVimAsk')
    map <silent> <unique> <Leader>ta <Plug>TRV_TransVimAsk
endif

"insmode?
vmap <silent> <unique> <script> <Plug>TRV_TransVimVisual y:call <SID>TransVim("<c-r>"")<CR>
nmap <silent> <unique> <script> <Plug>TRV_TransVimNormal  :call <SID>TransVim(expand("<cword>"))<CR>
map  <silent> <unique> <script> <Plug>TRV_TransVimAsk     :call <SID>TransVim()<CR>

imap <c-F4> <c-o><Leader>tr
map  <c-F4> <Leader>tr
