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

def fetchMusicTags(
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

    except Exception as e:
        return None, None


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


if __name__ == "__main__":
    sources = [
        ("REVNOIR", "20mg"),
        ("IGORRR", "ADHD"),
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