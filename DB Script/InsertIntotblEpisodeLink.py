# The query will insert the link for each episode in tblEpisodeLink. The input file is created by
# Written by: Tushar

import os

#from enum import Enum

#Class sitcom(Enum):#
#    Friends = 1
#    TheBigBangTheory = 2

home = os.environ['HOME']
source = home + '/Documents/sitcomSeasonList.txt'
destination = home + '/Documents/sitcomquery.txt'
query = "INSERT INTO tblEpisodeLink (sitcomID,season,link) VALUES \n"
f=open(source,'r')
w=open(destination,'w')
read = 0
written = 0
for line in f:
    read = read + 1
    #print line
    sitcomName = line[0:50].strip()
    season=line[50:65].strip()
    link=line[65:].strip()

    if sitcomName == 'Friends':
        sitcomID = 1
    elif sitcomName == "The Big Bang Theory":
        sitcomID = 2

    seasonNum = season.split(" ")[1]
    #print type(seasonNum)
    #print type(link)
    #print type(query)
    query = query + "(" + str(sitcomID) + "," + (seasonNum) + ",'" + link.replace("'","\\'") + "'),\n"
    #print query
    #print "%^%*kjnf:" + str(read)
    #if read == 10:
#        break

w.write(query)

print 'read :' + str(read)
#print 'written: ' + str(written)

f.close
w.close
