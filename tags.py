import sys, os, re, eyed3

def tag(music, artist, title):
    audiofile = eyed3.load(music)
    audiofile.tag.artist = "Token Entry"
    audiofile.tag.title = "The Edge"
    audiofile.tag.save()
    print(music, artist, title)

path = input("Give the folder to tag (Enter a path ex: rawmusic/sorted) ")
sortedFileList = sorted(os.listdir(path))
print(path)

for d in sortedFileList:
    if os.path.isdir(os.path.join(path,d)):
        for f in sorted(os.listdir(os.path.join(path,d))):
            
            tag(os.path.join(path,d,f), d, f.replace(".opus", "").split('-', 1)[1])