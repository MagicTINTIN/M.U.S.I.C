import sys, os, re
from mutagen.oggopus import OggOpus

def tagMusic(music, artist, title):
    try:
        audiofile = OggOpus(music)
        audiofile["artist"] = artist
        audiofile["title"] = title
        audiofile.save()
        print(f"Tagged {music} with artist: {artist}, title: {title}")
    except Exception as e:
        print(f"Error tagging file {music}: {e}")

path = input("Give the folder to tag (Enter a path ex: rawmusic/sorted) ")
sortedFileList = sorted(os.listdir(path))
print(path)

for d in sortedFileList:
    if os.path.isdir(os.path.join(path,d)):
        for f in sorted(os.listdir(os.path.join(path,d))):
            
            tagMusic(os.path.join(path,d,f), d, f.replace(".opus", "").split('-', 1)[1].lstrip())