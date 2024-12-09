import sys, os, re, mutagen

def tag(music, artist, title):
    audiofile = mutagen.File(music)
    audiofile["artist"] = artist
    audiofile["title"] = title
    audiofile.save()
    print(music, artist, title)

path = input("Give the folder to tag (Enter a path ex: rawmusic/sorted) ")
sortedFileList = sorted(os.listdir(path))
print(path)

for d in sortedFileList:
    if os.path.isdir(os.path.join(path,d)):
        for f in sorted(os.listdir(os.path.join(path,d))):
            
            tag(os.path.join(path,d,f), d, f.replace(".opus", "").split('-', 1)[1].lstrip())