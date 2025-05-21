import sys, os, re, datetime
from mutagen.oggopus import OggOpus

def getMusicLength(music):
    try:
        audiofile = OggOpus(music)
        return audiofile.info.length
    except Exception as e:
        print(f"Error opening file {music}: {e}")
    #     audiofile["title"] = title
    #     audiofile.save()
    #     print(f"Tagged {music} with artist: {artist}, title: {title}")

path = input("Give the folder to tag (Enter a path ex: downloaded/sorted) ")
if (path == ""):
    print("default fallback -> downloaded/sorted")
    path = "downloaded/sorted"
sortedFileList = sorted(os.listdir(path))
print(path)

timesList = list()
perBandList = list()
totalMusics = 0
totalBands = 0
totalTime = 0

for d in sortedFileList:
    folder_path = os.path.join(path, d)
    if os.path.isdir(folder_path):
        totalBands += 1
        perBand = 0
        for f in sorted(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, f)
            if f.endswith(".opus"):
                perBand+=1
                totalMusics += 1
                length = getMusicLength(file_path)
                if length:
                    # print(f"{file_path}: {length:.2f} seconds")
                    totalTime += length
                    timesList.append(length)
            # tagMusic(os.path.join(path,d,f), d, f.replace(".opus", "").split('-', 1)[1].lstrip())
        perBandList.append(perBand)
        
print(f"STATS:\n")
# print(f"Total Musics: {totalMusics}, for a total of {str(datetime.timedelta(seconds=totalTime))} ({totalTime}s)")
# print(f"Average: {str(datetime.timedelta(seconds=totalTime/totalMusics))} ({totalTime/totalMusics}s)")
# print(f"Median: {str(datetime.timedelta(seconds=timesList.sort()[len(timesList)//2]))} ({timesList.sort()[len(timesList)//2]}s)\n")

# print(f"Total Bands: {totalBands}, for a total of {totalMusics} musics")
# print(f"Average: {totalMusics/totalBands} musics per band")
# print(f"Median: {sort(perBandList)[len(perBandList)//2]} musics per band")

print(f"Total Musics: {totalMusics}, for a total of {str(datetime.timedelta(seconds=totalTime))} ({totalTime}s)")
print(f"Average: {str(datetime.timedelta(seconds=totalTime/totalMusics))} ({totalTime/totalMusics}s)")

# Use sorted() to avoid modifying the original list
sortedTimesList = sorted(timesList)
medianTime = sortedTimesList[len(sortedTimesList)//2]
print(f"Median: {str(datetime.timedelta(seconds=medianTime))} ({medianTime}s)\n")

print(f"Total Bands: {totalBands}, for a total of {totalMusics} musics")
print(f"Average: {totalMusics/totalBands} musics per band")

# Use sorted() for perBandList
sortedPerBandList = sorted(perBandList)
medianPerBand = sortedPerBandList[len(sortedPerBandList)//2]


sortedPerBandList = sorted(perBandList)
numberPerBandList = [0 for _ in range(sortedPerBandList[-1] + 1)]

weightedPerBandList = []
for nb in sortedPerBandList:
    numberPerBandList[nb] += 1
    for i in range(nb):
        weightedPerBandList.append(nb)
weightedMedianPerBand = weightedPerBandList[len(weightedPerBandList)//2]

print(f"Median: {medianPerBand} musics per band ({numberPerBandList})")
print(f"WeightedMedian: {weightedMedianPerBand} musics per band")