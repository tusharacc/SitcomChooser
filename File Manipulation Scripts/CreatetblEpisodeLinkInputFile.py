# Creates the input file for DB Script - InsertIntotblEpisodeLink.py
# Will create the link of each episode.
#OS - MAC
#
# Written By: Tushar Saurabh

import os


def prepareStr(sitcom,season,filepath):
    lenSitcom = len(sitcom)
    lenSeason = len(season)
    space1 = ''
    for x in range(50-lenSitcom):
        space1 = space1 + ' '
    space2 = ''
    for x in range(15-lenSeason):
        space2 = space2 + ' '
    return sitcom + space1 + season + space2 + filepath  + '\n'



home = os.environ['HOME']
#sitcom = 'The Big Bang Theory'
sitcom = "Friends"
source = home + '/Documents/Sitcoms/' + sitcom
destination = home + '/Documents/sitcomSeasonList.txt'

w=open(destination,'w')

listOfSeason = os.listdir(source)
written = 0
for season in listOfSeason:
    if season != '.DS_Store':
        seasonFolder = source + '/' + season
        for fileName in os.listdir(seasonFolder):
            filepath = seasonFolder + '/' + fileName
            fileExtension = os.path.splitext(filepath)[1]
            if ((fileExtension != '.txt') & (fileExtension != '.jpg') & (fileExtension != '.srt') & (fileExtension != '.sub') & (fileExtension != '.idx')):
                line = prepareStr(sitcom,season,filepath)
                #line = sitcom + '  ' + season + '  ' + filepath +'\n'
                written = written + 1
                w.write(line)

print 'written: ' + str(written)


w.close
