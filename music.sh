#!/bin/bash
# Music Ultimate Sorter Incredibly Cool - M.U.S.I.C.

#def -------------------- vars --------------------
TopText="Welcome in M.U.S.I.C - Music Ultimate Sorter Incredibly Cool\n------------------------------------------------------------"


#def -------------------- functions --------------------
getArray() {
    array=() # Create array
    while IFS= read -r line # Read a line
    do
        array+=("$line") # Append line to the array
        echo "$line"
    done < "$1"
}

# -------------------- program --------------------
#before beginning
printf "\e]2;M.U.S.I.C - Checks\a"
clear
echo -e $TopText
echo "Create and edit  ./bandlist write the main part of the bands in order to sort them faster"
echo "Please write one band per line and let the last one EMPTY"
echo "Some recommandations before starting : only if you haven't downloaded your playlist yet"
echo "Before downloading your playlist be sure to have yt-dlp installed"
echo "If it is not the case, please run : python3 -m pip install -U yt-dlp"
echo $'\n'
echo "Also, make sure there is no folder named rawmusic in the current folder"
echo $'\n'
read -p "If you have everything ready, press Enter to continue or Ctrl+C to abort" </dev/tty

# choose playlist
printf "\e]2;M.U.S.I.C - Choose your playlist\a"
clear
echo -e $TopText
echo -e "Do you have already downloaded your playlist [Y/n]"
read downloaded
if [ $downloaded == "n" ]
then
    echo -e "Please enter your music playlist link : "
    read playlink
    printf "\e]2;M.U.S.I.C - Choose your file format\a"
    echo -e "Please enter the file format you want (opus recommanded) : "
    read formatfile
    mkdir rawmusic
    cd ./rawmusic

    #waiting downloading
    printf "\e]2;M.U.S.I.C - Downloading\a"
    clear
    echo "A new terminal has been launched and it is actually downloading your playlist in a new folder called ./rawmusic"
    echo $'\n'
    echo "While we are waiting for the second terminal to download the entire playlist,"
    echo "You can edit the ./bandlist ./blacklist ./redirlist files writing the main part of the bands in order to sort them faster"
    echo "Please write one band per line"
    echo $'\n'
    echo "You can also see the advancement of the dowloading glancing a look at the folder ./rawmusic/"
    echo $'\n'
    commandterminal=`yt-dlp -i -R 5 --yes-playlist --extract-audio --audio-format $formatfile --audio-quality 0 --output "%(playlist_index)sþ%(uploader)sß%(title)s.%(ext)s" $playlink`
    expr $commandterminal
    echo "If there is an error just above don't worry, juste verify it downloaded the files you need"
    read -p "If you can see this, the dowloading might be done, you can press Enter" </dev/tty
else
    read -p "Then put it in a folder named rawmusic and press Enter" </dev/tty
    cd ./rawmusic
fi
printf "\e]2;M.U.S.I.C - Sorter\a"
echo -e "Please enter the last index of the files : "
read lastindex
cd ../
#getArray "./bandlist"
echo "Band list"
readarray -t array <bandlist
for e in "${array[@]}"
do
    echo "$e"
done
echo "List of not found files" > notfound
echo "-----------------------------------------------------------------"
echo $bandlist
cd ./rawmusic
for ((i=1; i<=$lastindex; i++))
do
    if (( $i < 10 ))
    then
        filebegin="000$i"
    elif (( $i < 100 ))
    then
        filebegin="00$i"
    elif (( $i < 1000 ))
    then
        filebegin="0$i"
    else
        filebegin="$i"
    fi
    #check if the file exist
    filename=""
    IFS=$'\n'; for FILE in `ls $filebegin*` #`find -name $filebegin'*'`
    do
        filename="$filename$FILE "
    done
    echo "$filename"
    if [ "$filename" == "" ]
    then
        echo "### ERROR NO FILE FOUND WITH NUMBER $filebegin"
        echo "$filebegin" >> notfound
    else
        #read nope # pas à pas
        
        
        filename="${filename::-1}"
        futurename="${filename:5}"
        
        
        band=0
        len=${#array[@]}
        notfound=true
        while [ $band -lt $len ] && $notfound;
        do
            #echo ${array[band]}
            if [[ ${filename,,} == *"${array[band],,}"* ]]
            then
                #rename
                vchannel="${futurename%ß*}"
                vtitle="${futurename##*ß}"
                if [[ ${vtitle,,} == *"${array[band],,}"* ]]
                then
                    newname="$vtitle"
                else
                    newname="$vchannel - $vtitle"
                fi
                #create directory
                if [ ! -d "./${array[band]}" ]; then
                    mkdir "${array[band]}"
                fi
                mv "$filename" "./${array[band]}/$newname"
                notfound=false
            else 
                let band++
            fi
        done
        if $notfound
        then
            echo "No band found for $filename"
            # asks for the band
            bandnotconfirmed=true
            while $bandnotconfirmed
            do
                echo "What is the name of this band ?"
                read tempband
                echo "confirm the name"
                read tempband1
                if [[ ${tempband,,} == *"${tempband1,,}"* ]]
                then
                    bandnotconfirmed=false
                fi
            done

            #check if the band is in the list but neither in the channel name nor the title
            bandinlist=0
            lenlist=${#array[@]}
            notfoundinlist=true
            while [ $bandinlist -lt $lenlist ] && $notfoundinlist;
            do
                #echo ${array[bandinlist]}
                if [[ ${tempband,,} == *"${array[bandinlist],,}"* ]]
                then
                    #rename
                    echo "The band is already in the list but neither in the channel name nor the title mentioned it"
                    notfoundinlist=false
                else 
                    let bandinlist++
                fi
            done
            #update bandlist file if there isn't the band in it
            if $notfoundinlist
            then
                cd ../
                echo "$tempband" >> bandlist
                readarray -t array <bandlist
                cd ./rawmusic
                echo "band list updated"
            fi

            if [[ ${filename,,} == *"${tempband,,}"* ]]
            then
                #rename
                vchannel="${futurename%ß*}"
                vtitle="${futurename##*ß}"
                if [[ ${vtitle,,} == *"${tempband,,}"* ]]
                then
                    newname="$vtitle"
                else
                    newname="$vchannel - $vtitle"
                fi
                #create directory
                if [ ! -d "./${tempband}" ]; then
                    mkdir "${tempband}"
                fi
                echo "mv $filename ./${tempband}/$newname"
                mv "$filename" "./${tempband}/$newname"
            else
                vtitle="${futurename##*ß}"
                newname="$tempband - $vtitle"
                #create directory
                if [ ! -d "./${tempband}" ]; then
                    mkdir "${tempband}"
                fi
                mv "${filename}" "./${tempband}/$newname"
            fi
        fi
    fi

done
echo "Exiting..."
