#!/bin/bash

# Generate a sample structure for screenshots

set -x

SCREENSHOT="assets/screenshot.png"

ROOT="/Users/Browning/Dropbox/DropTheBeat"
USER1="JohnDoe"
USER2="JaneDoe"
USER3="Me"
FILE1="/tmp/New Mashup 2015.mp3"
FILE2="/tmp/My Demo Tracks.zip"
FILE3="/tmp/Live Winter Set.als"

touch "$FILE1"
touch "$FILE2"
touch "$FILE3"

dtb --root $ROOT --new $USER1
dtb --root $ROOT --new $USER2
dtb --root $ROOT --new $USER3

dtb --root $ROOT --test $USER3 --share "$FILE1"
dtb --root $ROOT --test $USER3 --share "$FILE2" --user $USER2
dtb --root $ROOT --test $USER1 --share "$FILE3"

echo "save a screenshot to: $SCREENSHOT"
dtb --root $ROOT --test $USER3 --gui

rm -r $ROOT

mogrify -resize %50 $SCREENSHOT
