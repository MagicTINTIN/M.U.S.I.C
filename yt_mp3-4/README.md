# YouTube → MP3 / MP4

## Windows
> Peu testé sous windows, mais ça doit marcher
### Dépendances
Assurez vous d'avoir bien copié tout le dossier [`windows`](windows), puis mettez-y les executables [`**yt-dlp.exe**` (téléchargeable ici)](https://github.com/yt-dlp/yt-dlp/releases) et [`**ffmpeg.exe**` (téléchargeable ici)](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip) [*[site web]*](https://ffmpeg.org/download.html).\
Note: *Vous pouvez renomer le dossier [`windows`](windows) et ne garder que ce dossier et son contenu. Il est indépendant du reste des fichiers.

Votre dossier doit ressembler à ça désormais :
```
└── windows (peut être renommé en "youtube-mp3" par exemple)
        ├── ffmpeg.exe
        ├── yt-dlp.exe
        ├── ytmp4.exe
        ├── ytmp3.bat
        ├── ytmp3.ps1
        ├── ytmp4.bat
        └── ytmp4.ps1
```

*Il est peut être nécessaire de créer un sous-dossier dans ce dossier nommé `downloads` s'il n'est pas automatiquement créé au lancement du script.*



### Utilisation
Exécutez les scripts [`ytmp3.bat`](windows/ytmp3.bat) ou [`ytmp4.bat`](windows/ytmp4.bat) contenus dans le dossier [`windows`](windows).\
Vous pouvez les exécuter en **double-cliquant** dessus.

---

## Linux
### Dépendances
Vous aurez besoin d'avoir installé sur votre linux les logiciels suivants au préalable :
```
yt-dlp ffmpeg
```
### Utilisation
Exécutez les scripts [`ytmp3.sh`](linux/ytmp3.sh) ou [`ytmp4.sh`](linux/ytmp4.sh) contenus dans le dossier [`linux`](linux).