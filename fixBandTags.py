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

bandToFix = input("Give the band to fix: ")


with open('tagsPerBand.json') as f:
    bandTags = json.load(f)

# tagMusic("./test.opus", "moi", "c'est moi")
# for d in sortedFileList:
if os.path.isdir(os.path.join(path,bandToFix)):
    genres = bandTags[bandToFix]["genre"]
    print(bandToFix + " : ", genres)
    for f in sorted(os.listdir(os.path.join(path,bandToFix))):
        if not f.startswith(bandToFix + " - "):
            input("ERROR: '" + f + "' is not a valid filename for the band '" + bandToFix + "'. ")
        print(bandToFix + " : " + f.replace(".opus", "")[len(bandToFix)+2:].lstrip())
        tagMusic(os.path.join(path,bandToFix,f), bandToFix, f.replace(".opus", "")[len(bandToFix)+2:].lstrip(), genres)