if ( --( window_title() == "... - Opera" ) and 
        ( window_class() == "Opera" or window_class() == "Firefox" ) and
        ( window_type() == "WINDOW_NORMAL" ) and 
        --( window_role() == "browser" ) and 
        --( window_application() == "... - Opera" ) and
        true ) then
    xy(0,0 )
    --size(1280,1024 )
    workspace(3)
    --maximize()
    fullscreen()
end

if ( -- opera-start-dialog:
      false and
        ( window_class() == "Opera" ) and
        ( window_type() == "WINDOW_DIALOG" ) and
        ( window_role() == "" ) and
        true ) then
    --xy(40,40 )
    --size(580,524 )
    --workspace(3)
    --maximize()
    os.execute("xdotool windowactivate " 
                    .. window_xid() .. 
                    " ; sleep 0.1 ; xdotool key --window " 
                    .. window_xid() .. 
                    " Return")
end


if ( --( window_title() == ".. Claws Mail .." ) and 
        ( window_class() == "Claws-mail" ) and
        ( window_type() == "WINDOW_NORMAL" ) and 
        ( window_role() == "mainwindow" ) and 
        --( window_application() == "claws-mail" ) and
        true ) then
    xy(0,0 )
    size(1280,1024 )
    workspace(2)
    --maximize()
    fullscreen()
end

-- vim:ts=4:sw=4:expandtab
