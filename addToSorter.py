import sys, os, json, datetime, re
from mutagen.oggopus import OggOpus


try:
    from unidecode import unidecode
except ImportError:
    print("Unidecode is not installed on this computer.\nPlease install it with pip install Unidecode (or with pacman -Sy python-unidecode)")
    exit(1)


#################### HELP ####################
if "--help" in sys.argv:
    print("This is the module S.O.R.T.E.R (Sorter Obviously Reliable To Evaluate Records) of M.U.S.I.C")
    print("The following options are available :")
    print("    --no-save : prevent S.O.R.T.E.R by making a backup of band.json")
    print("    --import  : to import a file ./bandlist containing band names")
    print("    --logs    : to activate full logs")
    exit(0)


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


#################### SAVE LIST FILE ####################
def saveListFile():
    with open('bands.json', 'w') as f:
        json.dump(bands, f, indent=4)


#################### OPERATIONS LIST FILE ####################
# AU  : added uploader
# AB  : added band
# AL  : added label

# IU  : Is uploader
# IL  : Is label ?
# IBD : Is band (found in channel and title) ?
# IBT : Is band (found with topic) ?

# GB  : Is the guess right ?

# RBG : Right band guess
# RUG : Right uploader guess
# RLG : Right label guess

# WB  : Write the band name
# WT  : Write the trigger of title which made us understand what band it is

# BF  : Band found
# CF  : Channel found
# LF  : Label found

def writeoperation(type):
    with open("operations", "a") as myfile:
        myfile.write("\n" + type)


#################### ADD (band, channel, label) ####################
        
#### BAND
def addbanduploader(band, name="notaband", othername=False):
    uploader = name if othername else band
    if band in bands["bandnames"]:
        writeoperation("AU")
        print("  + UPL : " + uploader + " (" + band + ")")
        bands["bandnames"][band].append(uploader)
    else:
        writeoperation("AB")
        print("  + BND : " + band)
        bands["bandnames"][band] = [ uploader ]
    saveListFile()

#### CHANNEL
def addchannel(band, name="notaband", othername=False):
    if othername:
        bands["uploaders"][name] = band
    else:
        bands["uploaders"][band] = band
    addbanduploader(band, name, othername)
        
#### LABEL
def addlabel(labelname):
    bands["labels"].append(labelname)
    writeoperation("AL")
    print("  + LBL : " + labelname)
    saveListFile()


#################### OS Relative ####################
def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


#################### IMPORT ####################
def importfile():
    try:
        with open('bandlist') as bandlistf:
            for line in bandlistf:
                bandname = unidecode(line.rstrip()).upper()
                if len(bandname) > 0:
                    addchannel(bandname)
        return True
    except IOError:
        print("No bandlist found")
        return False


#################### FIND (band) ####################
def findband(ch, title, original):
    foundband = False
    chfound = False
    maxlen = 0
    chband = ""
    islabel = False if ch != 0 else True

    if ch != 0:
        writeoperation("LF")
        for bandn in bands["uploaders"]:
            if bandn in ch and len(bandn) > maxlen:
                maxlen = len(bandn)
                chband = bandn
                foundband = True
                chfound = True

    if ch == 0 or not foundband:
        for bandn in bands["uploaders"]:
            if bandn in unidecode(title).upper() and len(bandn) > maxlen:
                maxlen = len(bandn)
                chband = bandn
                foundband = True

    if foundband:
        writeoperation("BF")
    if chfound:
        writeoperation("CF")
    
    topicband = False
    if not islabel and not chfound:
        print("\nHelp needed !   " + original)
        originalArtist = original.split('þ')[1].split('ß')[0]

        if originalArtist.endswith(" - Topic"):
            # Topic channels
            writeoperation("IBT")
            topicband = confirm("BAND ? Is '"+ ch +"' the right name for " + originalArtist + " ? (Y/n) ")
        elif ch in unidecode(title).upper():
            # When the name is in the title and in the channel name
            writeoperation("IBD")
            topicband = confirm("BAND ? Is '"+ ch +"' the name of the band ? (Y/n) ")
            
        if topicband:
            writeoperation("RBG")
            addchannel(ch)
            chband = ch
            foundband = True
        else:
            writeoperation("IL")
            islabel = confirm("LABEL ? Is this channel ("+ ch +") a label channel (or provides musics from multiple bands) ? (Y/n) ")
        
    if islabel and ch != 0:
        writeoperation("RLG")
        addlabel(ch)
    elif foundband and ch != 0 and not topicband:
        print("\n########## Help needed ! " + original + " ##########")
        writeoperation("IU")
        if confirm("Is this channel ("+ ch +") an uploader of " + chband + " musics ? (Y/n) "):
            writeoperation("RUG")
            addchannel(chband, ch, True)
        else:
            foundband = False
    elif not foundband and ch != 0 and not topicband:
        writeoperation("GB")
        guessband = confirm("BAND ? Is '"+ ch +"' the band name of the music ? (Y/n) ")
            
        if guessband:
            writeoperation("RBG")
            addchannel(ch)
            chband = ch
            foundband = True
    
    if not foundband:
        print("\n########## No bandname found for '" + original + "' ##########")
        print("(" + str(ch) + " || " + title + ")")

        newband = ""
        nameconfirmed = False
        writeoperation("WB")
        while not nameconfirmed:
            newband = unidecode(input("What band is it ? ")).upper()
            nameconfirmed = confirm("Do you confirm the name of the band is '" + newband + "' ? (Y/n) " )
        chband = newband

        if newband not in bands["uploaders"]:
            addchannel(newband)
        
        if not islabel and ch != 0 and newband != ch:
            addchannel(newband, ch, True)
        elif ch != 0 and newband not in unidecode(title).upper() and newband not in ch:
            titletrigger = ""
            triggerconfirmed = False
            writeoperation("WT")
            while not triggerconfirmed:
                titletrigger = unidecode(input("What word(s) made you think the band is " + newband + " in the title ? (n if there wasn't) ")).upper()
                triggerconfirmed = confirm("Do you confirm the key word(s) was/where '" + titletrigger + "' ? (Y/n) " )
            if titletrigger != 'N':
                addchannel(newband, titletrigger, True)

    return chband


#################### CLEAN (name) ####################
def cleanbegin(toclean):
    cleaner = re.compile(r'.*?([a-zA-Z0-9].*)')
    cleaned = cleaner.findall(toclean)
    if len(cleaned) > 0:
        return cleaned[0]
    else:
        return "000BANDNAME000"

def cleanname(title, band):
    
    nobandReg = re.compile(re.escape(band), re.IGNORECASE)
    title = nobandReg.sub('', title.replace('"', '').replace('.opus', ''))

    boffReg = re.compile(r'(?is)\[Official.+', re.IGNORECASE)
    title = boffReg.sub('', title)

    poffReg = re.compile(r'(?is)\(Official.+', re.IGNORECASE)
    title = poffReg.sub('', title)

    pvidReg = re.compile(r'(?is)\(Video.+', re.IGNORECASE)
    title = pvidReg.sub('', title)

    bvidReg = re.compile(r'(?is)\[Video.+', re.IGNORECASE)
    title = bvidReg.sub('', title)

    p4kReg = re.compile(r'(?is)\(4K.+', re.IGNORECASE)
    title = p4kReg.sub('', title)

    b4kReg = re.compile(r'(?is)\[4K.+', re.IGNORECASE)
    title = b4kReg.sub('', title)

    pdeoffReg = re.compile(r'(?is)\(Offiziell.+', re.IGNORECASE)
    title = pdeoffReg.sub('', title)

    clipReg = re.compile(r'(?is)\(Clip.+', re.IGNORECASE)
    title = clipReg.sub('', title)

    bclipReg = re.compile(r'(?is)\[Clip.+', re.IGNORECASE)
    title = bclipReg.sub('', title)

    pMusicReg = re.compile(r'(?is)\(Music.+', re.IGNORECASE)
    title = pMusicReg.sub('', title)

    bMusicReg = re.compile(r'(?is)\[Music.+', re.IGNORECASE)
    title = bMusicReg.sub('', title)

    audioReg = re.compile(r'(?is)\(Audio.+', re.IGNORECASE)
    title = audioReg.sub('', title)

    phqReg = re.compile(r'(?is)\(HQ.+', re.IGNORECASE)
    title = phqReg.sub('', title)

    offMReg = re.compile(r'(?is)Official Music.+', re.IGNORECASE)
    title = offMReg.sub('', title)

    offLReg = re.compile(r'(?is)Official Lyric.+', re.IGNORECASE)
    title = offLReg.sub('', title)

    offAReg = re.compile(r'(?is)Official Audio.+', re.IGNORECASE)
    title = offAReg.sub('', title)

    offVReg = re.compile(r'(?is)Official Video.+', re.IGNORECASE)
    title = offVReg.sub('', title)

    title = cleanbegin(unidecode(title)).replace("000BANDNAME000", band).replace("[HD]", "").replace("(HD)", "").replace("(HQ)", "").replace("[HQ]", "").replace("{}", "").replace("()", "").replace("[]", "").replace('"', '').rstrip()
    if title.endswith('-'):
        title = title[:-1].rstrip()
    title = ' '.join(title.split())

    return title


#################### FIND (name) ####################
def findaname(ch, title, original):
    channelname = cleanbegin(unidecode(ch).upper().replace(" OFFICIAL", "").replace("OFFICIAL", "").replace(" - TOPIC", "").replace("VEVO", "").replace("OFFICIAL", ""))
    
    if channelname in bands["labels"]:
        band = findband(0, title, original)
    elif channelname in bands["uploaders"]:
        band = bands["uploaders"][channelname]
    else:
        band = findband(channelname, title, original)
    return [ band, cleanname(title, band)]

#################### CONFIG loader ####################
# opens the previous config if there was one
try:
    with open('bands.json') as f:
        bands = json.load(f)
        print("Previous config found")

        if "--no-save" not in sys.argv:
            os.rename(
                'bands.json', 
                "bandsave" + datetime.datetime.strftime(datetime.datetime.now() ,"%Y-%m-%d_%H-%M-%S") + ".json"
                )
            saveListFile()

        categories = ["labels", "uploaders", "bandnames"]
        for el in categories:

            if not el in bands:
                print("+ " + el + " -> config")
                if el == "labels":
                    bands[el] = []
                else:
                    bands[el] = {}

except IOError:
    print("No previous config found")
    bands = {
        # channels that upload musics which publish musics for multiple bands
        "labels": [],
        # name of uploaders that publish musics for only one band
        "uploaders": {},
        # list of uploaders by band name
        "bandnames": {},
    }


#################### --IMPORT ####################
if "--import" in sys.argv:
    if confirm("Do you have a file containing band names named ./bandlist ? (Y/n) "):
        if importfile():
                saveListFile()
                print("Band names successfully imported")
        else:
                print("Error while importing band names")
    else:
        print("Import cancelled")




#################### BEGIN ####################
print("\n\n------------------------------------------------------------\nM.U.S.I.C - Music Ultimate Sorter Incredibly Cool - Sorter\n------------------------------------------------------------")
# prevmusicnb = int(input("Enter the first number of the files to sort ? (Enter a number) "))
# path = input("Give the folder to sort (Enter a path ex: rawmusic/) ")
path = "downloaded"

#################### PREPARATION ####################
# with open("missingmusics", "a") as myfile:
#     myfile.write('\n\n---------------------------------------\n' + str(datetime.datetime.now()) + '\n---------------------------------------\n')
with open("operations", "a") as myfile:
    myfile.write('\n\n---------------------------------------\n' + str(datetime.datetime.now()) + '\n---------------------------------------\n')

os.makedirs(os.path.join(path,"sorted/"), exist_ok = True)
sortedFileList = sorted(os.listdir(path))
totalnbfile = len(sortedFileList)
fileincrement = 0


#################### FILE TAGGER ####################

# def eyed3TagMusic(music, artist, title):
#     audiofile = eyed3.load(music)
#     if audiofile is None:
#         print(f"Error: {destPathFile} is not a valid audio file.")
#         return
#     audiofile.tag.artist = artist
#     audiofile.tag.title = title
#     audiofile.tag.save()
#     print(music, artist, title)

def tagMusic(music, artist, title):
    try:
        audiofile = OggOpus(music)
        audiofile["artist"] = artist
        audiofile["title"] = title
        audiofile.save()
        print(f"Tagged {music} with artist: {artist}, title: {title}")
    except Exception as e:
        print(f"Error tagging file {music}: {e}")

#################### FILE ITERATOR ####################
for i in sortedFileList:
    if "--logs" in sys.argv:
        fileincrement += 1
        print("File " + str(fileincrement) + "/" + str(totalnbfile), end= ' | ')
    if os.path.isfile(os.path.join(path,i)) and 'þ' in i and 'ß' in i:
        arrFilename = i.split('þ')
        filepoint = i.split('.')
        filext = filepoint[len(filepoint) - 1]

        uploadArtist = arrFilename[1].split('ß')
        
        # actmusicnb = int(arrFilename[0])
        # # print(actmusicnb, i)

        # diffnb = actmusicnb - prevmusicnb
        # if diffnb > 0:
        #     with open("missingmusics", "a") as myfile:
        #         myfile.write("\n[" + str(diffnb) + " missing] : from " + str(prevmusicnb - 1) + " to " + str(actmusicnb))
        # elif diffnb < 0:
        #     with open("missingmusics", "a") as myfile:
        #         myfile.write("\n(" + str(diffnb) + " already existing) : from " + str(actmusicnb) + " (supposed to be " + str(prevmusicnb) + ")")
        
        # prevmusicnb = actmusicnb + 1
        
        namefound = findaname(uploadArtist[0], uploadArtist[1], i)
        newname = namefound[0] + " - " + namefound[1] + "." + filext

        if "--logs" in sys.argv:
            print(newname)
        os.makedirs(os.path.join(path, "sorted/", namefound[0]), exist_ok = True)
        destPathFile = os.path.join(path, "sorted/", namefound[0], newname)
        os.replace(os.path.join(path,i), destPathFile)
        print(destPathFile)
        tagMusic(destPathFile, namefound[0], namefound[1])

print("---------------------- THIS IS THE END ----------------------")

