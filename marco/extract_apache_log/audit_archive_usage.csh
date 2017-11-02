#!/bin/csh

# set search directory
set BASEDIR = /data/archive/scratch/

# set output file
set DATAFILE = ${BASEDIR}/searchaudit.dat

# generate empty output file if not exist
if (! -e $DATAFILE) touch $DATAFILE

cd $BASEDIR

# loop thorugh 
foreach uniqueid ( [123456789]*[0123456789] )

  # if not a directory
  if ( ! -d $uniqueid ) continue

  # if already saved, ignored
  if (`awk '($1=='$uniqueid')' $DATAFILE | wc -l `) then
    continue
  endif

  cd $uniqueid


  set timestamp = `stat --printf=%Z ${uniqueid}_prog.html `
  
  set targname = `awk '($2=="targname" && $3!="[]")' ${uniqueid}_prog.html | sed 's/^.*\[//' | sed 's/\]//' | tr " " "_"`
  if ( "$targname" != "" ) then
    echo $uniqueid $targname >> $BASEDIR/search_name.dat
    set targname = 1
  else
    set targname = 0
  endif

  set resoltargname = `awk '($2=="resoltargname" && $3!="[]")' ${uniqueid}_prog.html | sed 's/^.*\[//' | sed 's/\]//' | tr " " "_"`
  if ( "$resoltargname" != "" ) then
    echo $uniqueid $resoltargname >> $BASEDIR/resolv_name.dat
    set resoltargname = 1
  else 
    set resoltargname = 0
  endif


  set coord_equ = 0
  set coord_gal = 0
  set coordsearch = `awk '($2=="targco1" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  if ( $coordsearch ) then
    set co1type = `awk '($2=="co1type" && $3!="[]")' ${uniqueid}_prog.html | sed 's/^.*\[//' | sed 's/\]//' `
    if ("$co1type" == "equ" ) set coord_equ = 1
    if ("$co1type" == "gal" ) set coord_gal = 1
  endif

  set exptime = `awk '($2=="exptime" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  set seeing = `awk '($2=="seeing" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  set airmass = `awk '($2=="airmass" && $3!="[]")' ${uniqueid}_prog.html | wc -l `

  #set instrument = `awk '($2=="instrument" && $3!="[]")' ${uniqueid}_prog.html | tail -1 | sed 's/^.*\[//' | sed 's/\]//' | tr "|" " " | wc -w`
  set instrument = `awk '($2=="instrument" && $3!="[]")' ${uniqueid}_prog.html | tail -1 | sed 's/^.*\[//' | sed 's/\]//' `
  if ( "$instrument" == "" ) set instrument = "-"
  set ratcam = `echo $instrument | grep -ic RATCam`
  set ringo = `echo $instrument | grep -ic ringo`
  set supircam = `echo $instrument | grep -ic supircam`
  set meaburn = `echo $instrument | grep -ic meaburn`
  set rise = `echo $instrument | grep -ic rise`
  set frodospec = `echo $instrument | grep -ic frodospec`
  set ioo = `echo $instrument | grep -ic io:o`
  set ioi = `echo $instrument | grep -ic io:i`
  set thor = `echo $instrument | grep -ic thor`

  set spec_criteria = `awk '($2=="lambda" && $3!="[]")' ${uniqueid}_prog.html | wc -l ` 
  @ spec_criteria += `awk '($2=="specres" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  @ spec_criteria += `awk '($2=="dispersion" && $3!="[]")' ${uniqueid}_prog.html | wc -l `

  set tag_criteria = `awk '($2=="tagid" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  @ tag_criteria += `awk '($2=="userid" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  @ tag_criteria += `awk '($2=="propid" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  @ tag_criteria += `awk '($2=="groupid" && $3!="[]")' ${uniqueid}_prog.html | wc -l `
  @ tag_criteria += `awk '($2=="obsid" && $3!="[]")' ${uniqueid}_prog.html | wc -l `

  # Simple count of how may files were returned by the search 
  if ( -e cat${uniqueid}.txt ) then
    set files_returned = ` cat cat${uniqueid}.txt | wc -l `   
    if ( $files_returned ) @ files_returned--
  else
    set files_returned = nan
  endif

  # Was a tarball made
  set reduced_tarball = `/usr/bin/find . -name \*reduced.t\* | wc -l `
  set raw_tarball =     `/usr/bin/find . -name \*raw.t\* | wc -l `
  if ( $reduced_tarball ) then
    set download_reduced_tarball = 0
    foreach fn ( `/usr/bin/find . -name \*reduced.t\*` )
      @ download_reduced_tarball += `cat /var/log/httpd/access_log /var/log/httpd/access_log.1 | grep -c "GET.*/${fn:t}"  `
    end
  else 
    set download_reduced_tarball = nan
  endif
  if ( $raw_tarball ) then
    set download_raw_tarball = 0
    foreach fn ( `/usr/bin/find . -name \*raw.t\*` )
      @ download_raw_tarball += `cat /var/log/httpd/access_log /var/log/httpd/access_log.1 | grep -c "GET.*/${fn:t}" `
    end
  else 
    set download_raw_tarball = nan
  endif


  # Look in access_logs to see if data were downloaded
  set download_pub_jpg  = `cat /var/log/httpd/access_log /var/log/httpd/access_log.1 | grep     "GET.*/${uniqueid}/.*/Pub/.*\.jpg"  | grep -vc "_sm" `
  set download_pub_fits  = `cat /var/log/httpd/access_log /var/log/httpd/access_log.1 | grep -c "GET.*/${uniqueid}/.*/Pub/.*\.fits" `
  set download_priv_jpg = `cat /var/log/httpd/access_log /var/log/httpd/access_log.1 | grep     "GET.*/${uniqueid}/.*/Priv/.*\.jpg"  | grep -vc "_sm" `
  set download_priv_fits = `cat /var/log/httpd/access_log /var/log/httpd/access_log.1 | grep -c "GET.*/${uniqueid}/.*/Priv/.*\.fits" `

#           1       2          3            4              5         6         7       8        9      10      11       12     13       14    15         16   17    18   19              20                21               22             23                   24                 25                   26             27              28                      29        
  echo $uniqueid $timestamp $targname $resoltargname $coord_equ $coord_gal $exptime $seeing $airmass $ratcam $ringo $supircam $meaburn $rise $frodospec $ioo $ioi $thor $spec_criteria $tag_criteria $files_returned $download_pub_jpg $download_pub_fits $download_priv_jpg $download_priv_fits $reduced_tarball $raw_tarball $download_reduced_tarball $download_raw_tarball >> $DATAFILE
  cd $BASEDIR


end



