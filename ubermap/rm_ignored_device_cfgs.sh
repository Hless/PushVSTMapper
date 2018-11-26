#!/bin/bash
pushd ~/Ubermap/Devices
grep -rnwl . -e 'Ignore = True' > temp.txt
awk '{gsub(/ /,"\\ ")}8' temp.txt > Ignored.txt
rm temp.txt
cat Ignored.txt | xargs rm
rm Ignored.txt
popd
