import time
import os, sys
import json
import requests
# from mutagen.oggopus import OggOpus
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
        "user":"MagicTINTIN",
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
        rawTags = data.get("toptags", {}).get("tag", [])
        tags = [el["name"].upper() for el in rawTags[:10]] # if len(rawTags) > 10 else [el["name"] for el in rawTags]
        # print("LASTFMMMMMMMMMM ->",data, "\n=========\n",tags)
        if isinstance(tags, list) and tags:
            # take the highest-ranked tag
            # print("LASTFM TAGS->", tags)
            return tags
    return None

def fetchMusicTags_MB(artist: str) :
    # try:
    if True:
        # print(f"Searching in MB {artist}")
        res = musicbrainzngs.search_artists(
            artist=artist,
            limit=1
        )
        
        recs = res.get("artist-list", [])
        # print("res-> ",recs, "\n>>>", res)
        if not recs:
            return None

        rec = recs[0]

        # take the top tag name if available
        tags = rec.get("tag-list", [])
        genre = [el["name"].upper() for el in tags] if tags else None
        
        return genre

    # except Exception as e:
    #     print(e)
    #     return None

#################### CONFIRM FUNCTION ####################
yes = {'yes','y', 'ye', ''}
no = {'no','n'}

def confirm(message = "Reply by yes or no (yes by default) : "):
    notanswered = True

    while notanswered:
        choice = input(message).lower()
        if choice in yes:
            notanswered = False
            return True
        elif choice in no:
            notanswered = False
            return False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'\n")

def fetchMusicTags(artist: str):
    genre, mbID = None, None
    print(f">>> {artist} <<<")

    # if MB had no genre try Last.fm
    if (genre is None or genre == []) and LASTFM_API_KEY:
        print("Fetching Last.fm...")
        genre = fetchMusicTags_LFM(artist, mbID)
        print("found genre on lastfm: ", genre)
        
    
    if (genre is None or genre == []) and LASTFM_API_KEY:
        print("Fetching MB...")
        genre = fetchMusicTags_MB(artist)
        print("found genre on MB: ", genre)
    
    if (genre is None or genre == []):
        print(f"What music genre(s separated by ',') does '{artist}' play? > ", end="")
        genre = input().upper().split(",")
        while not confirm("Do you confirm the band styles? (yes by default): "):
            print(f"What music genre(s separated by ',') does '{artist}' plays? >", end="")
            genre = input().upper().split(",")

    return genre

def batchFetcher(sources: List[str], batch_size: int = 5, pause: float = 1.0):
    results = {}
    total = len(sources)
    for start in range(0, total, batch_size):
        batch = sources[start : start + batch_size]
        for artist in batch:
            genre = fetchMusicTags(artist)
            results[artist] = {
                "artist": artist,
                "genre": genre
            }
            with open("bandTags.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            time.sleep(1)
        if start + batch_size < total:
            time.sleep(pause)
    return results


# def tagMusic(music, artist, title):
#     try:
#         audiofile = OggOpus(music)
#         audiofile["artist"] = artist#["rock","metal"]
#         audiofile["albumartist"] = ["rock","metal"]
#         audiofile["album"] = "THE ALBUM"
#         audiofile["genre"] = ["rock","metal"]
#         audiofile["title"] = title
#         audiofile.save()
#         print(f"Tagged {music} with artist: {artist}, title: {title}")
#     except Exception as e:
#         print(f"Error tagging file {music}: {e}")


# ls downloaded/sorted -Qm --color="none" > bands
currentBands = ["1000MODS", "257ERS", "2CELLOS", "3TEETH", "4 NON BLONDES", "66SAMUS", "7 WEEKS", "8DEG6 CREW", "ABBIE FALLS", "ACCEPT", "ACCVSED", "AC_DC", "ACID MAMMOTH", "AC SLATER", "A DAY TO REMEMBER", "ADELE", "AEROSMITH", "AETHERWAVE", "A-HA", "AIRBOURNE", "AJ DISPIRITO", "ALESTORM", "ALEX MOFA GANG", "ALIEN ANT FARM", "ALIEN WEAPONRY", "ALLEVIATE", "ALTERGEIST", "AMARANTHE", "AMON AMARTH", "AMORPHIS", "ANAKRONIC", "ANAKRONIC ELECTRO ORKESTRA", "ANDRE ANTUNES", "ANDREW W.K.", "ANDROMIDA", "ANIMALS AS LEADERS", "ANKOR", "ANNIHILATOR", "ANNISOKAY", "ANTHRAX", "ANTI-CLONE", "ANTOINE DORSEUIL", "ANY GIVEN DAY", "APASHE", "APOCALYPSE ORCHESTRA", "APOCALYPTICA", "ARCANE", "ARCH ENEMY", "ARCHITECTS", "ARCHSPIRE", "ARCTIC MONKEYS", "ARKA'N ASRAFOKOR", "ASHEN", "AS I LAY DYING", "ASKING ALEXANDRIA", "ASTERO H", "ATREYU", "AU5", "AVATAR", "AVENGED SEVENFOLD", "AVIANA", "AVRALIZE", "AWAKENING SUN", "AWAKE THE DREAMER", "AWOLNATION", "AXEL BAUER", "AXEL ONE", "AYRON JONES", "BABYMETAL", "BADFLOWER", "BAD OMENS", "BAD SITUATION", "BAD WOLVES", "BAG RAIDERS", "BARREN", "BATTLE BEAST", "BEAR GHOST", "BEARTOOTH", "BEASTIE BOYS", "BEAST IN BLACK", "BEE GEES", "BEEPLE", "BEETHOVEN", "BEHEMOTH", "BE'LAKOR", "BELZEBUBS", "BENIGHTED", "BERURIER NOIR", "BIG SOUL", "BILLY IDOL", "BILLY TALENT", "BINGO PLAYERS", "BLACK LABEL SOCIETY", "BLACK PUG", "BLACK RAINBOWS", "BLACK SABBATH", "BLACK TONGUE", "BLACKTOOTHED", "BLACK VEIL BRIDES", "BLEED FROM WITHIN", "BLESSTHEFALL", "BLIND CHANNEL", "BLIND GUARDIAN", "BLIND WITNESS", "BLOCKHEADS", "BLOC PARTY", "BLOODHOUND GANG", "BLOODYWOOD", "BLUE OYSTER CULT", "BLUR", "BODY AND BLOOD", "BODY COUNT", "BOMFUNK MC'S", "BON JOVI", "BONOBO", "BORDERS", "BORN OF OSIRIS", "BRAND OF SACRIFICE", "BREAKDOWN OF SANITY", "BRING ME THE HORIZON", "BRUJERIA", "BRUTUS", "BULLET FOR MY VALENTINE", "BURY TOMORROW", "C2C", "CAGE THE ELEPHANT", "CALIBAN", "CALIGULA'S HORSE", "CALOGERO", "CALVA LOUISE", "CANDLEBOX", "CANDLEMASS", "CAPITAL CITIES", "CARAVAN PALACE", "CAR BOMB", "CARNIFEX", "CARPENTER BRUT", "CASIOPEA", "CAZZETTE", "CELLDWELLER", "CERBERUS", "CHAINLYNX", "CHAOSEUM", "CHARLESBERTHOUD", "CHASE & STATUS", "CHELSEA GRIN", "CHILDISH GAMBINO", "CHIMAIRA", "CHRIS TURNER", "CHRONIK FICTION", "CHUCK BERRY", "CIVIL WAR", "CLAYTON KING", "CLOVEN HOOF", "CLOWN CORE", "CLOWNS", "CLUTCH", "CNVX", "COBRA SPELL", "CODE ORANGE", "COHEED AND CAMBRIA", "COLD NIGHT FOR ALLIGATORS", "COLDRAIN", "CONFLUX", "COREY TAYLOR", "CORPSE", "CORVUS CORAX", "CRADLE OF FILTH", "CREEDENCE CLEARWATER REVIVAL", "CRISIX", "+++ (CROSSES)", "CROSSFAITH", "CRUSH 40", "CRYSTAL LAKE", "CULTIST", "CUPHEAD", "CURRENTS", "CYPECORE", "CYRILMP4", "DADI FREYR", "DAFT PUNK", "DAGOBA", "DAMIEN SAEZ", "DANCE GAVIN DANCE", "DANCE WITH THE DEAD", "DANGANRONPA", "DANKO JONES", "DANNY ELFMAN & TRENT REZNOR", "DARKEN", "DARON MALAKIAN", "DA SHOU YU MEN TONG HAO HUI ", "DAUGHTRY", "DAVE RODGERS", "DAVID CASTELLO-LOPES", "DAVIE504", "DAYSEEKER", "DEADMAU5", "DEAD OR ALIVE", "DEAD PIRATES", "DEADTHRONE", "DEATHPHONK", "DECAPITATED", "DECREATE", "DEEP PURPLE", "DEFICIENCY", "DEFOCUS", "DEMON HUNTER", "DEMUNILLUSIONS", "DE PALMAS", "DEPECHE MODE", "DEREK & THE DOMINOS", "DESTINITY", "DETHKLOK", "DEXCORE", "DIABLO SWING ORCHESTRA", "DIAMOND DEUKLO", "DICK DALE", "DIE ARZTE", "DIMMU BORGIR", "DIRE STRAITS", "DISEMBODIED TYRANT", "DISTURBED", "DJ BLYATMAN", "DOMINUM", "DOOM", "DOPPELGANGER", "DOROTHY", "DRAGONFORCE", "DREAM STATE", "DRIP EU", "DROPOUT KINGS", "DROWNING POOL", "DROWN IN SULPHUR", "DRUMEO", "DSCHINGHIS KHAN", "DW DRUMS", "DYING FETUS", "E.D.G.E", "EDOUARDO", "EIGHT SINS", "EISBRECHER", "ELECTRIC CALLBOY", "ELEKTRIC GEISHA", "ELENA SIEGMAN", "EL ESTEPARIO SIBERIANO", "ELUVEITIE", "EMIL BULLS", "EMINEM", "EMMURE", "ENGST", "ENTERPRISE EARTH", "ENTER SHIKARI", "EPICA", "EREB ALTOR", "ERIC CLAPTON", "ERRA", "ESTUDIOS GALLINERO", "EUROPE", "EURYTHMICS", "EVANESCENCE", "EVA UNDER FIRE", "EXODUS", "EYES WIDE OPEN", "FACT", "FALLING IN REVERSE", "FATALS PICARDS", "FATBOY SLIM", "FEAR, AND LOATHING IN LAS VEGAS", "FEN", "FEUERSCHWANZ", "FEVER 333", "FINCH", "FIREFLIGHT", "FIRE FROM THE GODS", "FIT FOR A KING", "FIT FOR AN AUTOPSY", "FIT FOR RIVALS", "FIVE FINGER DEATH PUNCH", "FOCUS", "FOO FIGHTERS", "FORMATION", "FOR THE FALLEN DREAMS", "FOZZY", "FRANK CARTER & THE RATTLESNAKES", "FRANZ FERDINAND", "FREAK KITCHEN", "FROG LEAP STUDIOS", "FROM ASHES TO NEW", "FROM FALL TO SPRING", "FROM THE WASTED", "FROZEN CROWN", "FU MANCHU", "FUNASSYI", "FUTURE PALACE", "GANESH2", "GAVIN LUKE", "GEOFFPLAYSGUITAR", "GESU'S ULTIMATE MAIDEN", "GET SCARED", "GHOST", "GLORIA GAYNOR", "GLORYHAMMER", "GOD FORBID", "GODSMACK", "GOJIRA", "GOREPIG", "GORILLAZ", "GOSSIP", "GOZU", "GRAVITY", "GREEN DAY", "GUNS N' ROSES", "HABSTRAKT", "HAEDETH", "HAKEN", "HALESTORM", "HALF ME", "HALLAS", "HAMMERFALL", "HANABIE", "HANK LEVY", "HANS ZIMMER", "HARDY", "HARM'S WAY", "HARPER", "HATEBREED", "HEART OF A COWARD", "HEAVEN SHALL BURN", "HEIDEVOLK", "HELLFEST", "HIPPOTRAKTOR", "HO99O9", "HOLLOW FRONT", "HOLLYWOOD UNDEAD", "HOULE", "HUNTER X HUNTER", "HUNTRESS", "HYPOCRISY", "I AM ABOMINATION", "IBRAHIM MAALOUF", "IC3PEAK", "ICE NINE KILLS", "ICHIKA NITO", "ICON FOR HIRE", "IGGY POP", "IGNITE", "IGORRR", "IMAGINE DRAGONS", "IMMINENCE", "IMMOLATION", "IMMORTAL DISFIGUREMENT", "INDOCHINE", "INFECTED RAIN", "IN FLAMES", "IN THIS MOMENT", "INVENT ANIMATE", "INVISIONS", "I PREVAIL", "IRON MAIDEN", "ISLANDER", "ITCHY SCHLONG", "JACK WHITE", "JACOB LIZOTTE", "JAMES BOND", "JAMIROQUAI", "JARED DINES", "JEAN-LOUIS AUBERT", "JEAN PIERRE FROMAGE", "JESSE BEAHLER", "JESTERPOSE", "JET", "JILUKA", "JIMI HENDRIX", "JIMMY GNECCO", "JINJER", "JOAN JETT", "JOE SATRIANI", "JOHN 5", "JOHN WASSON", "JONATHAN DAVIS", "JONATHAN YOUNG", "JOSEPH SMITH", "JOYRYDE", "JUAREZ OLIVA", "JUDAS PRIEST", "JUSTIN HURWITZ", "KALLE KOSCHINSKY", "KANONENFIEBER", "KANSAS", "KARNIVOOL", "KDREW", "KERRY KING", "KEVIN SHERWOOD", "KHEMMIS", "KILLSWITCH ENGAGE", "KIM DRACULA", "KISS", "KMAC2021", "KNIFE PARTY", "KNOCKED LOOSE", "KONTRUST", "KORN", "KORPIKLAANI", "KREATOR", "KVELERTAK", "LACUNA COIL", "LADYBABY", "LA FERME JEROME", "LAMB OF GOD", "LANDMVRKS", "LAST TRAIN", "LED ZEPPELIN", "LEFT TO SUFFER", "LEGION OF THE DAMNED", "LEMON DEMON", "LENA SCISSORHANDS", "LENNY KRAVITZ", "LEPROUS", "LES 3 FROMAGES", "LES BERURIERS NOIRS", "LES CHEVAUX SANS TETES", "LES CLAYPOOL", "LES FATALS PICARDS", "LES GARCONS BOUCHERS", "LES INCONNUS", "LES RAMONEURS DE MENHIRS", "LES SALES MAJESTES", "LES TROIS ACCORDS", "LES WAMPAS", "LEVEL 42", "LIGER", "LIMP BIZKIT", "LINDEMANN", "LINKIN PARK", "LINZEY RAE", "LIONHEART", "LIPPS INC", "LIQUIDO", "LITTLE BIG", "LITTLEVMILLS", "LLOYD", "LOKUST", "LORDI", "LORNA SHORE", "LOUISE ATTAQUE", "LOVE AND DEATH", "LOVEBITES", "LUCKY CHOPS", "LUKE", "LUKK SIREM", "LUNATIC SOUL", "LYNYRD SKYNYRD", "MACHINE GUN KELLY", "MACHINE HEAD", "MADNESS", "MAGIC SWORD", "MAGNAVOLT", "MAGNOLIA PARK", "MAGOYOND", "MAKE THEM SUFFER", "MALEVOLENCE", "MAMMOTH WVH", "MANAU", "MANEGARM", "MANUEL", "MAN WITH A MISSION", "MARCUS MILLER", "MARILYN MANSON", "MASAFUMI TAKADA", "MASS HYSTERIA", "MASTER BOOT RECORD", "MASTODON", "MATHIEU SOMMET", "MATMATAH", "MAVIS", "MAX COVERI", "MAXIMUM THE HORMONE", "MC HAMMER", "MEGADETH", "MEGANEKO", "MEGARAPTOR", "MEINL CYMBALS", "MELODICKA BROS", "MENTAL CRUELTY", "MESHUGGAH", "METALLICA", "MICHAEL JACKSON", "MICKEY 3D", "MICK GORDON", "MICROSOFT", "MIKI SANTAMARIA", "MINDFORCE", "MO-DO", "MOLCHAT DOMA", "MONKEY3", "MOTIONLESS IN WHITE", "MOTLEY CRUE", "MR. BUNGLE", "MTH", "MUDVAYNE", "MUSE", "MUSHROOMHEAD", "MWAM", "MY CHEMICAL ROMANCE", "MY DARKEST DAYS", "MYFUCKINMESS", "NAIVE NEW BEATERS", "NANOWAR OF STEEL", "NATHAN JAMES", "NEBULA", "NE OBLIVISCARIS", "NEW YEARS DAY", "NHC", "NIAGARA", "NICKELBACK", "NIGHTWISH", "NIK NOCTURNAL", "NINE LASHES", "NINGEN ISU", "NIRVANA", "NITA STRAUSS", "NO DOUBT", "NOEL GALLAGHER'S HIGH FLYING BIRDS", "NOIR DESIR", "NOKTURNAL MORTUM", "NO ONE IS INNOCENT", "NORA LAKE", "NORTHLANE", "NOTHING BUT THIEVES", "NOTHING MORE", "NOVELISTS", "NOVELISTS FR", "NOVEMBER MIGHT BE FINE", "NYAN CAT", "NYTT LAND", "OASIS", "OBTEST", "OCEANS ATE ALASKA", "OF MICE & MEN", "OH HIROSHIMA", "OLIVER TREE", "ONE MORNING LEFT", "ONE OK ROCK", "ONI", "OOMPH", "OOMPH!", "OOOOOOOOOOO", "OPETH", "OPIUM DU PEUPLE", "ORBIT CULTURE", "ORDEN OGAN", "ORELSAN", "OTHERWISE", "OUR COMMON COLLAPSE", "OUR HOLLOW, OUR HOME", "OUR MIRAGE", "OUR PROMISE", "O-ZONE", "OZZY OSBOURNE", "PADDY AND THE RATS", "PAIN", "PALEFACE SWISS", "PANTERA", "PANZERBALLETT", "PAPA ROACH", "PARADISE LOST", "PARASITE INC.", "PARKWAY DRIVE", "PATRIARKH", "PEARL JAM", "PENDULUM", "PEN OF CHAOS ET LE NAHEULBAND", "PENSEES NOCTURNES", "PENTAKILL", "PERIPHERY", "PERTURBATOR", "PETE COTTRELL", "PINK FLOYD", "PIXIES", "PLACEBO", "PLASTIC BERTRAND", "PLINI", "PNEUMONIA BREATH", "P.O.D", "P.O.D.", "POLAR", "POLARIS", "POLYPHIA", "POPPY", "PORCUPINE TREE", "POSTMODERNJUKEBOX", "POWERWOLF", "PRESIDENT", "PRIDIAN", "PRIMUS", "PROMPTS", "PROSPECTIVE", "PSYCHOSTICK", "PUNK ROCK FACTORY", "PURGE OF SANITY", "QUEEN", "QUEENS OF THE STONE AGE", "RADIOHEAD", "RAGE AGAINST THE MACHINE", "RAM JAM", "RAMMSTEIN", "RAY LUZIER", "RED HOT CHILI PEPPERS", "RED SUN ATACAMA", "REFUSED", "REGARDE LES HOMMES TOMBER", "R.E.M", "RENDEZ VOUS", "REN JIAN YI ZI ", "RESOLVE", "REVNOIR", "RHAPSODY OF FIRE", "RHODZ", "RICHAADEB", "RIMSKY KORSAKOV", "RINGS OF SATURN", "RISE AGAINST", "RISE OF THE NORTHSTAR", "RIVAL SONS", "ROADRUNNER UNITED", "ROB SCALLON", "ROB ZOMBIE", "RORY GALLAGHER", "ROYAL BLOOD", "ROYAL REPUBLIC", "RUMAHOY", "RUSH", "RUSSKAJA", "SABATON", "SABIAN CYMBALS", "SABLE HILLS", "SAEZ", "SAINT AGNES", "SAINT ASONIA", "SALTATIO MORTIS", "SALVATORE GANACCI", "SANGUISUGABOGG", "SAOR", "SASTRA", "SAUL", "SAVAGE LANDS", "SCARS ON BROADWAY", "SCATMAN JOHN", "SCHRODINGER", "SCHWARZER ENGEL", "SCORPIONS", "SEETHER", "SEMARGL", "SEMBLANT", "SERJ TANKIAN", "SETHEVERMAN", "SHAARGHOT", "SHADOW OF INTENT", "SHAKA PONK", "SHAMAN'S HARVEST", "SHEPHERDS REIGN", "SHINEDOWN", "SHINING", "SHIROBON", "SHORES OF NULL", "SHYLMAGOGHNAR", "SIDILARSEN", "SIGNS OF THE SWARM", "SILENT PLANET", "SILVERSTEIN", "SIM", "SIMPLE MINDS", "SINK THE SHIP", "SKALMOLD", "SKA-P", "SKID ROW", "SKILLET", "SKINDRED", "SKIP THE USE", "SKRILLEX", "SKYCLAD", "SKYND", "SLAUGHTER TO PREVAIL", "SLAYER", "SLEEP THEORY", "SLEEP TOKEN", "SLIPKNOT", "SLOCBAND", "SMASH HIT COMBO", "SMASHING PUMPKINS", "SNARKY PUPPY", "SNOT", "SODOM", "SOEN", "SOLUTION .45", "SONIC", "SON LUX", "SORCERER", "SOULFLY", "SOUNDGARDEN", "SOVIET SUPREM", "SPACE OF VARIATIONS", "SPEED", "SPIDERBAIT", "SPIRITBOX", "SPIRITWORLD", "SPLATOON", "SPLEEN", "SPOTLIGHTS", "SQWOZ BAB", "STARRYSKY", "STATUS QUO", "STEPPENWOLF", "STEREOPONY", "STEVEN WILSON", "STEVE TERREBERRY", "STEVIE WONDER", "STOLEN BABIES", "STOMB", "STONE SOUR", "STRATOVARIUS", "STRAY CATS", "STROMAE", "STUCK IN THE SOUND", "STUPEFLIP", "SUCHMOS", "SUICIDE SILENCE", "SUM 41", "SUMERLANDS", "SUMO CYCO", "SUN EATER", "SUNSTROKE PROJECT & OLIA TIRA", "SUPERBUS", "SURFARIS", "SURVIVOR", "SWEDISH HOUSE MAFIA", "SYNESTIA", "SYSTEM OF A DOWN", "TAGADA JONES", "TAKAYOSHI OHMURA", "TALKING HEADS", "TAPE FIVE", "TARDIGRADE INFERNO", "TEAM AMERICA", "TEARS FOR FEARS", "TELEPHONE", "TEMPT FATE", "TEN56", "TENACIOUS D", "TEN SECOND SONGS", "TESSERACT", "TETRARCH", "TEXTURES", "THE AGONIST", "THE AMITY AFFLICTION", "THE ANCHOR", "THEATRE OF TRAGEDY", "THE BITES", "THE BLACK DAHLIA MURDER", "THE BLACK KEYS", "THE BOOZE", "THE BOSSHOSS", "THE BROWNING", "THE CARDIGANS", "THECITYISOURS", "THE CLASH", "THE CORRESPONDENTS", "THE CRANBERRIES", "THE CULT", "THE DARKNESS", "THE DEAD DAISIES", "THEDOO", "THE DOORS", "THE EAGLES", "THE GAZETTE", "THE GHOST INSIDE", "THE HAUNTED", "THE HIVES", "THE HU", "THE HUSTLE STANDARD", "THE IRRADIATES", "THE LAST SIGHS OF THE WIND", "THE OFFERING", "THE OFFSPRING", "THE OKLAHOMA KID", "THEORY OF A DEADMAN", "THE PLOT IN YOU", "THE POLICE", "THE PRETTY RECKLESS", "THE PRODIGY", "THE QEMISTS", "THE ROLLING STONES", "THE SCORE", "THE SHINS", "THE SIDH", "THE STROKES", "THE TAIKONAUTS", "THE TOXIC AVENGER", "THE WEEKND", "THE WHITE STRIPES", "THE WHO", "THINK OF A NEW KIND", "THORNHILL", "THREE DAYS GRACE", "THRICE", "THROATCUT", "THROWN", "THUNDERMOTHER", "THUNDERTALE", "THURSDAY", "THY ART IS MURDER", "TILL LINDEMANN", "TIMECOP1983", "TIM SIMONEC", "TOBY FOX", "TO KILL ACHILLES", "TOM MORELLO", "TOOL", "TOO MANY ZOOZ", "TO THE GRAVE", "TOTO", "TO WHOM IT MAY", "TRAMPSTA", "TREMONTI", "TREPALIUM", "TRIPTYKON", "TRIVIUM", "TRUST", "TRYGLAV", "TWELVE FOOT NINJA", "TWIZTID", "U2", "ULTRA VOMIT", "UNDERTALE", "UNLEASH THE ARCHERS", "UNMAKER", "UNPROCESSED", "UPON A BURNING BODY", "URNE", "UUHAI", "VAN HALEN", "VAYLE MYSTERY", "VEIL OF MAYA", "VENDED", "VENJENT", "VENUES", "VERSUS ME", "VEXED", "VIANOVA", "VIC FIRTH", "VICIOUS RAIN", "VILDHJARTA", "VIOLENCE", "VIRTUE", "VISAGE", "VISIONS OF ATLANTIS", "VIVALDI", "VKT PRODACTIONS", "VOICIANS", "VOLBEAT", "VOXMAKERS", "VULFPECK", "WAGE WAR", "WARGASM", "WATEVA", "WAX TAILOR", "WE BUTTER THE BREAD WITH BUTTER", "WE CAME AS ROMANS", "WEIRD AL YANKOVIC", "WHILE SHE SLEEPS", "WHITECHAPEL", "WHO THEY FEAR", "WILLOW", "WIND ROSE", "WINDWAKER", "WINGS", "WITHIN A DREAM", "WITHIN TEMPTATION", "WITHIN THE RUINS", "WOE IS ME", "WOLVES AT THE GATE", "XAVIER CAGNA", "YANNICK CREMER", "YAZOO", "Y.BLUES", "YEAH YEAH YEAHS", "YES", "YNGWIE MALMSTEEN", "YODELICE", "YOUSEI TEIKOKU", "YUNGBLUD", "ZACKGROOVES", "ZARDONIC", "ZARRAZA", "ZETRA", "ZZ TOP"]

if __name__ == "__main__":
    sources = [
        "SHAKA PONK",
        "REVNOIR"
        # ("SHAKA PONK", "Fear ya"),
        # ("REVNOIR", "20mg"),
        # ("Revnoir", "crève '"),
        # ("ARCHITECTS", "Animals"),
        # ("AVENGED SEVENFOLD", "Hail To The King"),
        # ("LANDMVRKS", "Sulfur Sombre 16")
    ]

    # do lookups in batches of 5, pausing 1 second between each batch
    results = batchFetcher(currentBands, batch_size=5, pause=1.0)

    for v,r in results.items():
        print(f"{r['artist']} → "
              f"genre: {r['genre']}")
        
    with open("bandTagsFinal.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

