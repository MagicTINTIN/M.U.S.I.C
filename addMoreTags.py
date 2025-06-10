import time
import json
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

def fetchMusicTags_LFM(artist: str, title: str) -> Optional[str]:
    if not LASTFM_API_KEY:
        return None

    params = {
        "method": "track.getInfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "track": title,
        "format": "json"
    }
    try:
        resp = requests.get(LASTFM_API_URL, params=params, timeout=5)
        data = resp.json()
        tags = data.get("track", {}).get("toptags", {}).get("tag", [])
        if isinstance(tags, list) and tags:
            # take the highest-ranked tag
            return tags#[0].get("name")
    except Exception as e:
        print("ERROR : ", e)
        pass
    return None

def fetchMusicTags_MB(
    artist: str,
    title: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    search MusicBrainz using artist+title.
    returns (album_name, genre) or (None, None) if not found.
    """
    try:
        res = musicbrainzngs.search_recordings(
            artist=artist,
            recording=title,
            limit=1,
            includes=["releases", "tags"]
        )
        recs = res.get("recording-list", [])
        if not recs:
            return None, None

        rec = recs[0]
        # take the first release title if available
        releases = rec.get("release-list", [])
        album = releases[0]["title"] if releases else None

        # take the top tag name if available
        tags = rec.get("tag-list", [])
        genre = tags[0]["name"] if tags else None

        return album, genre

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
    album, genre = fetchMusicTags_MB(artist, title)

    # if MB had no genre try Last.fm
    if genre is None and LASTFM_API_KEY:
        print("Fetching Last.fm...")
        genre = fetchMusicTags_LFM(artist, title)
        print("found")

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
        if start + batch_size < total:
            time.sleep(pause)
    return results


def tagMusic(music, artist, title):
    try:
        audiofile = OggOpus(music)
        audiofile["artist"] = ["rock","metal"]
        audiofile["albumartist"] = artist
        audiofile["album"] = "THE ALBUM"
        audiofile["genre"] = ["rock","metal"]
        audiofile["title"] = title
        audiofile.save()
        print(f"Tagged {music} with artist: {artist}, title: {title}")
    except Exception as e:
        print(f"Error tagging file {music}: {e}")

if __name__ == "__main__":
    sources = [
        ("SHAKA PONK", "Fear ya"),
        ("REVNOIR", "crève '"),
        ("ARCHITECTS", "Animals"),
        ("AVENGED SEVENFOLD", "Hail To The King"),
        ("LANDMVRKS", "Sulfur Sombre 16")
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
    

