Write-Output "YOUTUBE -> MP3"
$ytlink= Read-Host "Entrez un lien youtube"
Write-Output "Telechargement de $ytlink!"
.\yt-dlp --ffmpeg-location .\ -i -R 5 --extract-audio --audio-format mp3 --output "downloads\%(uploader)s - %(title)s.%(ext)s" $ytlink
Read-Host "Appuyez sur ENTREE pour terminer..."
