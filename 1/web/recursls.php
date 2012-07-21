<HTML>
<HEAD><TITLE>Index of <?echo $PATH_DIR> </TITLE></HEAD>

<BODY TEXT="#000000" BGCOLOR="#c0c0c0" LINK="#0000EE" VLINK="#00E000" ALINK="#E00000" BACKGROUND="images/spibleue.jpg">

<CENTER><TABLE COLS=2 WIDTH="90%" >
<TR><TD><?echo $PATH_DIR>
<TD><DIV ALIGN=right> <A HREF="
<? strtok($PATH_DIR,"/"); $rt = strtok("/"); echo "/$rt" >
/index.htm"> goto root Index </A></DIV>
</TABLE>

<TABLE BORDER=0 WIDTH="95%" CELLPADDING=1 CELLSPACING=0>

<? /* 4dos' descript.ion to index.html converter.PHPv2 SvD 01'99 */


Function ion2htm $pth (
static $cnt=0; static $lvl=0; /*global line/level counters*/
 if (fileSize($pth+"DESCRIPT.ION") <=0) { echo "sorry - no description"; return 0; }
 $h = fopen(  $pth+"DESCRIPT.ION", "r"); /* fails if not found! */
 if ($h==-1) { echo "sorry"; return 0; }

 while (!feof($h)) {
  $line = fgets($h,512);

  $word = strtok($line," ");
  if ($word != "") {  /*ignore lines if empty or starting with space !*/
   echo "<TR><TD"; if (!$cnt) { echo " WIDTH=\"20%\""; }
   $word = strtoupper($word); /*all come from DOS*/
   $name = $pth+$word; echo "$lvl::";
   $pfx=""; $i=0; while ($i<$lvl) { $pfx = $pfx+"&nbsp; * &nbsp;"; $i++; }
   echo "><A HREF=\"$name\"</A>$pfx$word";
   $filesz = fileType($name);
   if ($filesz!=-1 && $filesz!="dir") { $filesz = fileSize($name); }

   echo "<TD"; if (!$cnt) { echo " WIDTH=\"60%\""; } echo ">\r\n";
   $type = "";
   $word = strtok(" ");
   $i=0;
   while (!strstr($word,"\n") && $i<99) { /*strtok skips only ONE space!*/
      if (eregi("/BG",$word)) { $type = "/in Bulgarian"; }
       elseif (eregi("/Rus",$word)) { $type = "/in Russian"; }
       else { echo " $word"; }
      $word = strtok(" ");
      $i++;
   }
   echo "\r\n<TD"; if (!$cnt) { echo " WIDTH=\"20%\""; } echo ">\r\n";
   if ($filesz == "dir") { echo "directory"; }
    elseif ($filesz<0) { echo "missing;"; }
    elseif ($filesz<8192) { echo "%d bytes" $filesz; }
    else { echo "%dK" ($filesz+1023)/1024; }

   echo " $type\r\n";
   if ($filesz == "dir" && $lvl<6) { $lvl++; ion2htm($name+"/"); $lvl--; }
   $cnt++;
  }
 }
 fclose($h);
); /*eo func*/

ion2htm( "" );

>
<!-- SvD Jan'99 -->
</TABLE></BODY></HTML>
