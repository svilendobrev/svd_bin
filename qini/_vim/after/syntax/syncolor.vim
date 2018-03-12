"somehow run all this AFTER $VIMRUNTIME/syntax/syncolors.vim -
" put in $HOME/.vim/after/syntax/ or append to $VIMRUNTIME/syntax/syncolors.vim
"linux console (man console_codes) and KDE's konsole can change color-mapping 
"  (blue -> something lighter?)

if &t_Co >= 8
    "no blue on black, please
    hi Statement    cterm=none ctermfg=brown
    hi Identifier   cterm=none ctermfg=darkgreen	"darkcyan by default
    hi Comment      cterm=none ctermfg=darkgray		"if Normal is gray, this is darkgray; !! reverse is invisible (selection)!
    hi PreProc      cterm=none ctermfg=darkmagenta
    hi Constant     cterm=none ctermfg=darkred
    hi Type         cterm=none ctermfg=darkcyan
    hi Search       cterm=none ctermfg=black    ctermbg=brown "gray
    hi Folded       cterm=none ctermfg=darkgray

    hi IncSearch    cterm=none ctermfg=black ctermbg=brown
    hi DiffText     cterm=none ctermfg=black ctermbg=darkred
    hi DiffChange   cterm=none ctermfg=black ctermbg=darkmagenta
    hi DiffDelete   cterm=none ctermfg=black ctermbg=darkgreen
    hi DiffAdd      cterm=none ctermfg=black ctermbg=darkcyan

    "hi Todo        cterm=none ctermfg=darkcyan
    "hi Question    cterm=none ctermfg=darkcyan
    hi Directory    cterm=none ctermfg=darkcyan
    "hi NonText      cterm=none ctermfg=darkcyan
    hi SpecialKey   cterm=none ctermfg=darkcyan
    "hi Special      cterm=none ctermfg=darkcyan
    hi WarningMsg   cterm=none ctermfg=gray     ctermbg=darkred
    hi ErrorMsg     cterm=none ctermfg=gray     ctermbg=darkred
    hi Error        cterm=none ctermfg=gray     ctermbg=darkred
    hi ModeMsg      cterm=none ctermfg=brown

	if version >= 700
    	hi Pmenu 	cterm=none ctermbg=darkblue
    	hi PmenuSel cterm=none ctermfg=darkblue
    	hi PmenuSbar  cterm=none ctermbg=darkgray
    	hi PmenuThumb cterm=none ctermbg=gray
		hi MatchParen cterm=none ctermbg=gray ctermfg=none
	endif
endif


hi StatusLine    gui=reverse cterm=reverse term=reverse
hi Visual        gui=reverse "guifg=none guibg=none
hi Visual        cterm=reverse ctermbg=none ctermfg=none

"""colorscheme torte
"""set background=dark
"" dark display
"hi Normal guifg=gray72 guibg=rgb:4000/3c00/3000
hi Normal       gui=none guifg=gray50 guibg=black
"hi Statement     gui=none guifg=#a0a000  "yellow-ochre-ish 
hi Statement    gui=none guifg=#986000  "brown-orange-ish 
"hi Identifier guifg=darkcyan
hi Identifier   gui=none guifg=#209040  "green-ish1
"hi Comment      gui=none guifg=#6090c0  "blue-ish
hi Comment      gui=none guifg=gray40
hi PreProc      gui=none guifg=#a020a0  "magenta-ish
hi Constant     gui=none guifg=#802020  "red-ish
"hi Type         gui=none guifg=#508050  "green-ish2
hi Type         gui=none guifg=#6090c0  "blue-ish
hi Search       gui=none guifg=bg guibg=gray
hi IncSearch    gui=none guifg=bg guibg=#b08020 "orange-ish

hi DiffText     gui=none guibg=darkred
hi DiffChange   gui=none guibg=darkmagenta
hi DiffDelete   gui=none guifg=gray guibg=blue
hi DiffAdd      gui=none guifg=gray guibg=blue

hi Todo         gui=none guibg=darkred guifg=darkgray
hi Question     gui=none guifg=#90b090  "light-green-ish
hi Directory    gui=none guifg=darkcyan "rgb:8000/c000/d000
hi NonText      gui=none guifg=seagreen
hi SpecialKey   gui=none guifg=darkcyan
hi Special      gui=none guifg=darkcyan
hi WarningMsg   gui=none guifg=darkgray guibg=darkred
hi ErrorMsg     gui=none guifg=gray     guibg=darkred
hi Error        gui=none guifg=gray     guibg=darkred
hi ModeMsg      gui=none guifg=gray50   "brown  "#a8a050 yellow-ochre-ish

"no bold for gui
hi Statement    gui=none 
hi Question     gui=none
hi NonText      gui=none
hi Type         gui=none
hi ModeMsg      gui=none
hi MoreMsg      gui=none
hi VisualNOS    gui=none
hi Title        gui=none
hi ModeMsg      gui=none

