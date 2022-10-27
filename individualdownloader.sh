#!/bin/bash
# Music Ultimate Sorter Incredibly Cool - M.U.S.I.C.

TopText="Welcome in M.U.S.I.C - Music Ultimate Sorter Incredibly Cool - Downloader\n------------------------------------------------------------"

printf "\e]2;M.U.S.I.C - Setting up\a"
clear
echo -e $TopText
echo "Enter your file format (recommanded aac)"
read formatfile
echo "Enter your playlist link"
read playlink
nottheend=true
printf "\e]2;M.U.S.I.C - Downloading\a"
while $nottheend
do
    echo "Enter a video ID (X or X-Y)"
    read playlistid
    if [[ ${playlistid,,} == "exit" ]]
    then
        nottheend=false
    else
        if [[ ${playlistid,,} == *"-"* ]]
        then
            playlistidstart="${playlistid%-*}"
            playlistidend="${playlistid##*-}"
        else
            playlistidstart=$playlistid
            playlistidend=$playlistid
        fi
        yt-dlp -i -R 5 --yes-playlist --extract-audio --audio-format $formatfile --audio-quality 0 --playlist-start $playlistidstart --playlist-end $playlistidend --output "%(playlist_index)sþ%(uploader)sß%(title)s.%(ext)s" $playlink
    fi
done
#commandterminal=`yt-dlp -i -R 5 --yes-playlist --extract-audio --audio-format $formatfile --audio-quality 0 --output "%(playlist_index)sþ%(uploader)sß%(title)s.%(ext)s" $playlink`
echo "Exiting..."