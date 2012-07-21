" Vim syntax file
" Language:	Verilog-A
" Maintainer:	Jason Wandel <A14116@email.mot.com>
" Last Update:  Thurs Feb 17 9:05:12 CST 1999

" Remove any old syntax stuff hanging around
syn clear
set iskeyword=@,48-57,_,192-255,+,-,?


" A bunch of useful Verilog keywords
syn keyword verilogaStatement   parameter function endfunction
syn keyword verilogaStatement   analog module endmodule
syn keyword verilogaStatement   branch transition slew
syn keyword verilogaStatement   input output inout electrical ground voltage
syn keyword verilogaStatement   initial_step final_step analysis
syn keyword verilogaStatement   cross last_crossing timer discontinuity idt ddt
syn keyword verilogaStatement   laplace_nd laplace_zp laplace_zd laplace_np
syn keyword verilogaStatement   zi_nd zi_zp zi_zd zi_np idtmod limexp
syn keyword verilogaStatement   noise_table white_noise flicker_noise
syn keyword verilogaStatement   discipline enddiscipline nature endnature
syn keyword verilogaStatement   defparam bound_step delay absdelay
syn keyword verilogaStatement   integer real genvar

syn keyword verilogaLabel       begin end 
syn keyword verilogaConditional if else case default endcase
syn keyword verilogaRepeat      repeat while for generate

syn keyword verilogaTodo contained TODO

syn match   verilogaOperator "[&|~><!)(*#%@+/=?:;}{,.\^\-\[\]]"

syn region  verilogaComment start="/\*" end="\*/" contains=verilogaTodo
syn match   verilogaComment "//.*" oneline

syn match   verilogaGlobal "`[a-zA-Z0-9_]\+\>"
syn match   verilogaGlobal "$[a-zA-Z0-9_]\+\>"

syn match   verilogaConstant "\<[A-Z][A-Z0-9_]\+\>"

syn match   verilogaNumber   "\<[+-]\=[0-9_]\+\(\.[0-9_]*\|\)\(e\(+\|-\|\)[0-9_]*\|T\|G\|M\|k\|K\|m\|u\|n\|f\|p\|a\|\)\>"

syn region  verilogaString start=+"+  end=+"+

" Directives

"Modify the following as needed.  The trade-off is performance versus
"functionality.
syn sync lines=50

if !exists("did_veriloga_syntax_inits")
  let did_veriloga_syntax_inits = 1
 " The default methods for highlighting.  Can be overridden later

  hi link verilogaCharacter       Character
  hi link verilogaConditional     Conditional
  hi link verilogaRepeat          Repeat
  hi link verilogaString          String
  hi link verilogaTodo            Todo
  hi link verilogaComment         Comment
  hi link verilogaConstant        Constant
  hi link verilogaLabel           Label
  hi link verilogaNumber          Number
  hi link verilogaOperator        Special
  hi link verilogaStatement       Statement
  hi link verilogaGlobal          Define
  hi link verilogaDirective       SpecialComment
endif

let b:current_syntax = "veriloga"

" vim: ts=8
