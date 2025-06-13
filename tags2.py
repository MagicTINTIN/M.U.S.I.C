import sys, os, re, json
from mutagen.oggopus import OggOpus

def tagMusic(music, artist, title, genre):
    try:
        audiofile = OggOpus(music)
        audiofile["artist"] = artist
        audiofile["title"] = title
        audiofile["albumartist"] = genre
        audiofile["album"] = artist
        audiofile["genre"] = genre
        audiofile.save()
        print(f"Tagged {music} with artist: {artist}, title: {title} : {len(genre)} genres")
    except Exception as e:
        print(f"Error tagging file {music}: {e}")

path = input("Give the folder to tag (Enter a path ex: downloaded/sorted) ")
if (path == ""):
    print("default fallback -> downloaded/sorted")
    path = "downloaded/sorted"
sortedFileList = sorted(os.listdir(path))
print(path)

with open('tagsPerBand.json') as f:
    bandTags = json.load(f)

# tagMusic("./test.opus", "moi", "c'est moi")
for d in sortedFileList:
    if os.path.isdir(os.path.join(path,d)):
        genres = bandTags[d]["genre"]
        print(d + " : ", genres)
        for f in sorted(os.listdir(os.path.join(path,d))):
            if not f.startswith(d + " - "):
                input("ERROR: '" + f + "' is not a valid filename for the band '" + d + "'. ")
            print(d + " : " + f.replace(".opus", "")[len(d)+2:].lstrip())
            tagMusic(os.path.join(path,d,f), d, f.replace(".opus", "")[len(d)+2:].lstrip(), genres)