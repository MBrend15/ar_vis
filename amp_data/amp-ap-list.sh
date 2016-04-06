#!/bin/bash
./amp-logon.sh
DATE=`date +"%Y-%m-%d-%H-%M"`
FNAME="ap_list_$DATE.xml"
curl -b ./AMP-$AMP_USERNAME.cjar --output "AMP_$FNAME"  https://amp.cns.vt.edu/ap_list.xml
curl -b ./RAMP-$RAMP_USERNAME.cjar --output "RAMP_$FNAME"  https://ramp.cns.vt.edu/ap_list.xml





