#!/bin/bash

file=~/C0d34L1F3/mp3LyricDownloader/currentLyric.txt

while true; do
    inotifywait -e modify $file
    clear
    cat $file
done

