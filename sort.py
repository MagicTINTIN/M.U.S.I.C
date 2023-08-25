import sys, os, json, datetime, pip

try:
    from unidecode import unidecode
except ImportError:
    print("Unidecode is not installed on this computer.\nPlease install it with pip install Unidecode (or with pacman -Sy python-unidecode)")
    exit(1)

yes = {'yes','y', 'ye', ''}
no = {'no','n'}

def addbanduploader(band, name="notaband", othername=False):
    uploader = name if othername else band
    if band in bands["bandnames"]:
        bands["bandnames"][band].append(uploader)
    else:
        bands["bandnames"][band] = [ uploader ]
    
def addchannel(band, name="notaband", othername=False):
    if othername:
        bands["uploaders"][name] = band
    else:
        bands["uploaders"][band] = band
    return addbanduploader(band, name, othername)

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

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

# opens the previous config if there was one
try:
    with open('bands.json') as f:
        bands = json.load(f)
        print("Previous config found")

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

# bands = json.dumps(jsonfilecfg)
if "--import" in sys.argv:
    notanswered = True

    while notanswered:
        choice = input("Do you have a file containing bands name named ./bandlist ? (Y/n) ").lower()
        if choice in yes:
            notanswered = False
            if importfile():
                print("Band names successfully imported")
            else:
                print("Error while importing band names")
        elif choice in no:
            notanswered = False
            print("Import cancelled")
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'\n")

with open('bands.json', 'w') as f:
    json.dump(bands, f, indent=4)

print("\n\n------------------------------------------------------------\nM.U.S.I.C - Music Ultimate Sorter Incredibly Cool - Sorter\n------------------------------------------------------------")
prevmusicnb = int(input("Enter the first number of the files to sort ? (Enter a number) "))

path = input("Give the folder to sort (Enter a path ex: rawmusic/) ")
dirname = os.path.dirname(__file__)


with open("missingmusics", "a") as myfile:
    myfile.write('\n\n---------------------------------------\n' + str(datetime.datetime.now()) + '\n---------------------------------------\n')

for i in sorted(os.listdir(path)): #os.path.join(dirname,)
    if os.path.isfile(os.path.join(path,i)) and 'þ' in i and 'ß' in i: #dirname,
        arrFilename = i.split('þ')
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
        
        channelname = uploadArtist[0].replace(" - Topic", "")
        if channelname in bands["labels"]:
            tmp=0
        elif channelname in bands["uploaders"]:
            tmp=0
        else:
            tmp=1

#mkdir("test")
#os.rename('test', 'hello world')

