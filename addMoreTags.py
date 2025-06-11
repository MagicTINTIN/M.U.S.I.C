import time
import os
import json
import requests
from mutagen.oggopus import OggOpus
from typing import List, Tuple, Dict, Optional

import musicbrainzngs

# Configure it with your own user-agent !
musicbrainzngs.set_useragent(
    app="M.U.S.I.C",
    version="1.0",
    contact="magictintin@proton.me"
)
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"

def fetchMusicTags_LFM(artist: str, mbID: str) -> Optional[str]:
    if not LASTFM_API_KEY:
        return None
    params = {
        "method": "artist.getTopTags",
        "api_key": LASTFM_API_KEY,
        # "track": title,
        "artist": artist,
        "autocorrect":1,
        "format": "json"
    }

    # if mbID != None:
    #     params = {
    #         "method": "artist.getTopTags",
    #         "api_key": LASTFM_API_KEY,
    #         "mbID": mbID,
    #         "artist": artist,
    #         "autocorrect":1,
    #         "format": "json"
    #     }
    # try:
    if True:
        resp = requests.get(LASTFM_API_URL, params=params, timeout=5)
        data = resp.json()
        tags = data.get("track", {}).get("toptags", {}).get("tag", [])
        print("LASTFMMMMMMMMMM ->",data, "\n=========\n",tags)
        if isinstance(tags, list) and tags:
            # take the highest-ranked tag
            print("LASTFM TAGS->", tags)
            return tags#[0].get("name")
    # except Exception as e:
    #     print("ERROR : ", e)
    #     pass
    return None

def fetchMusicTags_MB(
    artist: str,
    title: str
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    # try:
    if True:
        print(f"Searching in MB {artist} - {title}")
        res = musicbrainzngs.search_recordings(
            # query= artist + " " + title,
            # limit=1,
            # includes=["releases", "tags"]

            artist=artist,
            release=title,
            limit=1,
            # includes=["releases", "tags"]
        )
        
        recs = res.get("recording-list", [])
        print("res-> ",recs, "\n>>>", res)
        if not recs:
            return None, None

        rec = recs[0]
        # take the first release title if available
        releases = rec.get("release-list", [])
        album = releases[0]["title"] if releases else None

        # take the top tag name if available
        tags = rec.get("tag-list", [])
        genre = [el["name"] for el in tags] if tags else None

        # art = rec.get("artist", [])
        art1 = rec.get("artist-credit", [])
        print(f"1->", art1)
        # print(art)
        artistID = art1[0]["artist"]["id"]
        if True:
            artist = musicbrainzngs.get_artist_by_id(artistID, includes=["tags"]) #"genres", 
            # recs = res.get("recording-list", [])
            
            tagslist = artist.get("tag-list", [])
            if "tag-list" in artist["artist"]:
                print("AAA - res-> ",artist, "\n->>>>>",artist["artist"]["tag-list"], "\n#########> ", [el["name"] for el in artist["artist"]["tag-list"]])#, "\nAAA - >>>", res)  artist["tag-list"]
                # print()
                genre = [el["name"] for el in artist["artist"]["tag-list"]]
            else:
                print("AAAAAAAAAAAAAA - y a rien")
        return album, genre, artistID

    # except Exception as e:
    #     print(e)
    #     return None, None


def fetchMusicTags(
    artist: str,
    title: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    search MusicBrainz (or Last.fm if necessary) using artist+title.
    returns (album_name, genre) or (None, None) if not found.
    """
    album, genre, mbID = fetchMusicTags_MB(artist, title)

    # if MB had no genre try Last.fm
    if genre is None and LASTFM_API_KEY:
        print("Fetching Last.fm...")
        genre = fetchMusicTags_LFM(artist, mbID)
        print("found genre on lastfm: ", genre)

    return album, genre

def batchFetcher(
    sources: List[Tuple[str, str]],
    batch_size: int = 5,
    pause: float = 1.0
) -> List[Dict[str, Optional[str]]]:
    """
    pausing between batches.
    Returns array o f{ "artist", "title", "album", "genre" }
    """
    results = []
    total = len(sources)
    for start in range(0, total, batch_size):
        batch = sources[start : start + batch_size]
        for artist, title in batch:
            album, genre = fetchMusicTags(artist, title)
            results.append({
                "artist": artist,
                "title": title,
                "album": album,
                "genre": genre
            })
            time.sleep(1)
        if start + batch_size < total:
            time.sleep(pause)
    return results


def tagMusic(music, artist, title):
    try:
        audiofile = OggOpus(music)
        audiofile["artist"] = artist#["rock","metal"]
        audiofile["albumartist"] = ["rock","metal"]
        audiofile["album"] = "THE ALBUM"
        audiofile["genre"] = ["rock","metal"]
        audiofile["title"] = title
        audiofile.save()
        print(f"Tagged {music} with artist: {artist}, title: {title}")
    except Exception as e:
        print(f"Error tagging file {music}: {e}")

if __name__ == "__main__":
    sources = [
        # ("SHAKA PONK", "Fear ya"),
        # ("REVNOIR", "20mg"),
        ("Revnoir", "crève '"),
        # ("ARCHITECTS", "Animals"),
        # ("AVENGED SEVENFOLD", "Hail To The King"),
        # ("LANDMVRKS", "Sulfur Sombre 16")
    ]

    # do lookups in batches of 5, pausing 1 second between each batch
    results = batchFetcher(sources, batch_size=5, pause=1.0)

    for r in results:
        print(f"{r['artist']} - \"{r['title']}\" → "
              f"album: {r['album']}, genre: {r['genre']}")
        
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Wrote", len(results), "entries to results.json")
    tagMusic("SHAKA PONK - Fear Ya.opus", "SHAKA PONK", "Fear Ya")
    

