#!/bin/bash
echo -ne "YOUTUBE -> MP3\nYoutube link: "
read ytlink
yt-dlp --ffmpeg-location .\ -i -R 5 --ffmpeg-location `which ffmpeg` --extract-audio --audio-format mp3 --output "downloads/%(uploader)s - %(title)s.%(ext)s" $ytlink
echo -ne "Press ENTER to exit..."
read pause