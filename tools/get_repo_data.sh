#!/bin/sh
cat repos-c repos-java repos-python | awk '{a=$1; gsub(/\//,"-",a); print "wget -O", a "-" $2 ".zip https://github.com/" $1 "/archive/" $2 ".zip";}' | sh
