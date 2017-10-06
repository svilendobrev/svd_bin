if ( --( window_title() == "... - Opera" ) and 
     ( window_class() == "Opera" ) and
     ( window_type() == "WINDOW_NORMAL" ) and 
     ( window_role() == "browser" ) and 
     --( window_application() == "... - Opera" ) and
	 true ) then
     xy(0,0 )
     size(1280,1024 )
     workspace(3)
     maximize()
end

if ( --( window_title() == "az@svilendobrev.com - Claws Mail 3.15.1" ) and 
     ( window_class() == "Claws-mail" ) and
     ( window_type() == "WINDOW_NORMAL" ) and 
     ( window_role() == "mainwindow" ) and 
     --( window_application() == "claws-mail" ) and
	 true ) then
     xy(0,0 )
     size(1280,1024 )
     workspace(2)
     maximize()
end
