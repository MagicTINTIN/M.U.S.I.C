import os, json, datetime

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

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

with open('bands.json', 'w') as f:
    json.dump(bands, f)


#mkdir("test")
#os.rename('test', 'hello world')

