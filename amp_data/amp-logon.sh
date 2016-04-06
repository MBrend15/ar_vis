#!/bin/bash
curl -q -c ./AMP-$AMP_USERNAME.cjar -d "credential_0=$AMP_USERNAME" -d "credential_1=$AMP_PASSWORD" -d "destination=/" -d "login=Log In" https://amp.cns.vt.edu/LOGIN
curl -q -c ./RAMP-$RAMP_USERNAME.cjar -d "credential_0=$RAMP_USERNAME" -d "credential_1=$RAMP_PASSWORD" -d "destination=/" -d "login=Log In" https://ramp.cns.vt.edu/LOGIN


