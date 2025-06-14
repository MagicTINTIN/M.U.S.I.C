originalPath=`pwd`
cd /run/media/user/Music/M.U.S.I.C/downloaded
yt-dlp -i -R 5 --extract-audio --audio-format opus --audio-quality 0 --output "0þ%(uploader)sß%(title)s.%(ext)s" $1
cd ../
LASTFM_API_KEY="`cat ../k`"
export LASTFM_API_KEY
python3 addToSorter.py --no-save
cd $originalPath