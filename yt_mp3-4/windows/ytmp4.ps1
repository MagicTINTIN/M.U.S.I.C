Write-Output "YOUTUBE -> MP4"
$ytlink= Read-Host "Entrez un lien youtube"
Write-Output "Telechargement de $ytlink!"
.\yt-dlp --ffmpeg-location .\ -i -R 5 --recode-video mp4 --output "downloads\%(uploader)s - %(title)s.%(ext)s" $ytlink
Read-Host "Appuyez sur ENTREE pour terminer..."
