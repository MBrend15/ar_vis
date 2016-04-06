#!/bin/bash
./amp-logon.sh
DATE=`date +"%Y-%m-%d-%H-%M"`
FNAME="ap_detail_id_$1_$DATE.xml"
curl -b ./AMP-$AMP_USERNAME.cjar --output "AMP_$FNAME" -d "id=$1" https://amp.cns.vt.edu/ap_detail.xml
curl -b ./RAMP-$RAMP_USERNAME.cjar --output "RAMP_$FNAME" -d "id=$1" https://ramp.cns.vt.edu/ap_detail.xml




