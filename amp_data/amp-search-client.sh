#!/bin/bash
DATE=`date +"%Y-%M-%d-%H-%M"`
FNAME="${1//':'/-}_client_search_$DATE.xml"
curl -b ./AMP-$AMP_USERNAME.cjar --output "AMP_$FNAME"  https://amp.cns.vt.edu/client_search.xml?query=$1
curl -b ./RAMP-$RAMP_USERNAME.cjar --output "RAMP_$FNAME"  https://ramp.cns.vt.edu/client_search.xml?query=$1

