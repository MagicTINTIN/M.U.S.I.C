import sys, os, json, datetime

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


#################### ADD (band, channel, label) ####################
def addbanduploader(band, name="notaband", othername=False):
    uploader = name if othername else band
    if band in bands["bandnames"]:
        print("  + UPL : " + uploader + " (" + band + ")")
        bands["bandnames"][band].append(uploader)
    else:
        print("  + BND : " + band)
        bands["bandnames"][band] = [ uploader ]
    
def addchannel(band, name="notaband", othername=False):
    if othername:
        bands["uploaders"][name] = band
    else:
        bands["uploaders"][band] = band
    return addbanduploader(band, name, othername)

def addlabel(labelname):
    bands["labels"].append(labelname)
    print("  + LBL : " + labelname)


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
        for bandn in bands["uploaders"]:
            if bandn in ch and len(bandn) > maxlen:
                maxlen = len(bandn)
                chband = bandn
                foundband = True
                chfound = True

    if ch == 0 or not foundband:
        for bandn in bands["uploaders"]:
            if bandn in title and len(bandn) > maxlen:
                maxlen = len(bandn)
                chband = bandn
                foundband = True

    if not islabel and not chfound:
        islabel = confirm("Is this channel ("+ ch +") a label channel (or provides musics from multiple bands) ? (Y/n) ")
    if islabel and ch != 0:
        addlabel(ch)
    elif foundband:
        if confirm("Is this channel ("+ ch +") an uploader of " + chband + " musics ? (Y/n) "):
            addchannel(chband, ch, True)
        else:
            foundband = False
    
    if not foundband:
        print("----------------------- No bandname found for '" + original + "' -----------------------")
        print("(" + ch + " || " + title + ")")

        newband = ""
        nameconfirmed = False
        while not nameconfirmed:
            newband = unidecode(input("What band is it ? ")).upper()
            nameconfirmed = confirm("Do you confirm the name of the band is '" + newband + "' ? (Y/n) " )
        chband = newband

        if newband not in bands["uploaders"]:
            addchannel(newband)
        
        if newband != ch and not islabel:
            addchannel(newband, ch, True)
        elif newband not in title:
            titletrigger = ""
            triggerconfirmed = False
            while not triggerconfirmed:
                titletrigger = unidecode(input("What word(s) made you think the band is " + newband + " in the title ? ")).upper()
                triggerconfirmed = confirm("Do you confirm the name of the band is '" + newband + "' ? (Y/n) " )
            addchannel(newband, titletrigger, True)

    return chband

#################### FIND (name) ####################
def findaname(ch, title):
    channelname = unidecode(ch).upper().replace(" OFFICIAL", "").replace("OFFICIAL", "").replace(" - TOPIC", "")
    if channelname in bands["labels"]:
        tmp=0
    elif channelname in bands["uploaders"]:
        tmp=0
    else:
        tmp=1
    return ""


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
                print("Band names successfully imported")
        else:
                print("Error while importing band names")
    else:
        print("Import cancelled")

with open('bands.json', 'w') as f:
    json.dump(bands, f, indent=4)




#################### BEGIN ####################
print("\n\n------------------------------------------------------------\nM.U.S.I.C - Music Ultimate Sorter Incredibly Cool - Sorter\n------------------------------------------------------------")
prevmusicnb = int(input("Enter the first number of the files to sort ? (Enter a number) "))
path = input("Give the folder to sort (Enter a path ex: rawmusic/) ")


#################### PREPARATION ####################
with open("missingmusics", "a") as myfile:
    myfile.write('\n\n---------------------------------------\n' + str(datetime.datetime.now()) + '\n---------------------------------------\n')

os.makedirs(os.path.join(path,"/sorted/"), exist_ok = True)
sortedFileList = sorted(os.listdir(path))
totalnbfile = len(sortedFileList)
fileincrement = 0


#################### FILE ITERATOR ####################
for i in sortedFileList:
    if "--logs" in sys.argv:
        fileincrement += 1
        print("File " + fileincrement + "/" + totalnbfile)
    if os.path.isfile(os.path.join(path,i)) and 'þ' in i and 'ß' in i:
        arrFilename = i.split('þ')
        filepoint = i.split('.')
        filext = filepoint[len(filepoint) - 1]

        uploadArtist = arrFilename[1].split('ß')
        
        actmusicnb = int(arrFilename[0])
        print(actmusicnb, i)

        diffnb = actmusicnb - prevmusicnb
        if diffnb > 0:
            with open("missingmusics", "a") as myfile:
                myfile.write("\n[" + str(diffnb) + " missing] : from " + str(prevmusicnb - 1) + " to " + str(actmusicnb))
        elif diffnb < 0:
            with open("missingmusics", "a") as myfile:
                myfile.write("\n(" + str(diffnb) + " already existing) : from " + str(actmusicnb) + " (supposed to be " + str(prevmusicnb) + ")")
        
        prevmusicnb = actmusicnb + 1
        
        namefound = findaname(uploadArtist[0], uploadArtist[1])
        newname = namefound[1] + "." + filext
        os.makedirs(os.path.join(path, "/sorted/", namefound[0]), exist_ok = True)
        os.replace(os.path.join(path,i), os.path.join(path, "/sorted/", namefound[0], newname))

print("---------------------- THIS IS THE END ----------------------")

