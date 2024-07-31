# M.U.S.I.C

Outil pour automatiser le téléchargement de playlist YouTube, de rangement et de renommage de fichiers.\
*Tool to automate YouTube playlist dowloading, sorting and renaming files.*

### YouTube → MP3/MP4
> **Pour uniquement télécharger de YouTube des mp3 et des mp4, [cliquez ici](yt_mp3-4/)

## Linux
### Dépendances/*Dependencies*
Installez pour votre distribution les paquets suivants :\
*Install for your distribution the following packages:*
```
python3 yt-dlp ffmpeg
```
---
### Utilisation/*Usage*
> **Téléchargement/*Download***

Téléchargez les musiques de votre playlist avec `music.sh` pour la télécharger en entier, ou `individualdownload.sh` pour n'en télécharger qu'une partie.\
*Dowload your whole playlist with `music.sh`. To download only a part, use `individualdowload.sh`*

> **Tri/*Sort***

Pour lancer le tri du dossier où les musiques ont été téléchargées, lancez `sorter.py`.\
*To start sorting the directory in which the musics had been dowloaded, start `sorter.py`.*

> **Tag**

Afin que les fichiers audio contiennent le nom de l'artiste et le titre de la musique, vous pouvez utiliser `tags.py` pour mettre à jour leurs tags.
*In order to make the audio files contain the music title and artist, you can use `tags.py` to update their tag.*