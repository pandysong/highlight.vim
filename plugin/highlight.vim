if exists('*matchadd') == 0
    echom 'this plugin needs the function matchadd which is missing.'
    finish
endif

highlight highlight_active_lines ctermbg=darkred guibg=darkred

function! HighlightAdd(file)
    if filereadable(expand(a:file)) == 0
       echo "file " . a:file . " not exists"
       return
    endif
    " read from a file
    let serialized = readfile(a:file)[0]
    " deserialize the data to vim var
    execute "let result = " . serialized
    if exists('g:hl_dict') == 0
        call HighlightReset()
    endif
    call extend(g:hl_dict, result)
endfun

function! HighlightReset()
    let g:hl_dict = {}
endfun

function! HighlightUpdate()
    if exists('w:hl_matchid')
        silent! call matchdelete(w:hl_matchid)
        unlet w:hl_matchid
    endif
    if exists('g:hl_dict') == 0
        return
    endif

    let l:patterns = get(g:hl_dict,@%,"")
    if l:patterns == ""
        return
    endif

    let w:hl_matchid = matchadd("highlight_active_lines",patterns)

    if w:hl_matchid == -1
        echom "fail to add match pattern, Please report a bug"
    endif
endfun


autocmd BufEnter * call HighlightUpdate()
command! -nargs=1 HighlightAdd :call HighlightAdd(<f-args>)
command! HighlightReset :call HighlightReset()
