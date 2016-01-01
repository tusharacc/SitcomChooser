# Main logic that queries the episode to randomly select the not-watched episode. It uses VLC to open the video.
# OS - MAC


__author__ = 'tusharsaurabh'

import mysql.connector
import sys
import subprocess
from mysql.connector import errorcode
from random import *

class DbOperations:
    def __init__(self):

        try:
            self.dbConn =  mysql.connector.connect(user='root',
                                database='dbSitcomChooser',password='helloworld14')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def ExecuteQuery(self,query):
        cursor = self.dbConn.cursor(buffered=True)
        try:
            cursor.execute(query)
            return {'rowCount':cursor.rowcount, 'data':cursor.fetchall(),'error':0}
            cursor.close()
        except Exception as e:
            cursor.close()
            return {'rowCount':'Err', 'data':'Err','error':e}

    def UpdateQuery(self,query):

        cursor = self.dbConn.cursor()
        try:
            cursor.execute(query)
            self.dbConn.commit()
            cursor.close()
            return {'rowCount':cursor.rowcount, 'data':cursor.fetchall(),'error':0}
        except Exception as e:
            cursor.close()
            return {'rowCount':'Err', 'data':'Err','error':e}

    def CloseConn(self):
        self.dbConn.close()

debug = True
try:
    objDb = DbOperations()
except Exception as e:
    sys.exit(e)

cont = True

while cont:

    if debug:
        print "Before first query"

    query = ("SELECT sitcomID FROM tblSitcom where complete = 0 ")

    try:
        result = objDb.ExecuteQuery(query)
        rowReturned = result['rowCount']

        if rowReturned > 0:
            if rowReturned == 1:
                chosenSitcom = result['data'][0][0]
            else:
                length = len(result['data'])
                randomInt = randint(0,length-1)
                chosenSitcom = result['data'][randomInt][0]

            query = ("SELECT maxSeason FROM tblMaxSeason WHERE complete = 0 and sitcomID = "+ str(chosenSitcom))

            result = objDb.ExecuteQuery(query)
            rowReturned = result['rowCount']

            if debug:
                print "After second query"

            if rowReturned > 0:
                season = randint(1,result['data'][0][0])
                query = ("SELECT link FROM tblEpisodeLink WHERE watched = 0 and sitcomID = "+ str(chosenSitcom) + " and season =" + str(season))

                result = objDb.ExecuteQuery(query)
                rowReturned = result['rowCount']

                if debug:
                    print "After Third query"

                if rowReturned > 0:
                    if rowReturned == 1:
                        #Play the video and Update the episode as watched
                        chosenSitcomLink = result['data'][0][0]
                        query = "UPDATE tblEpisodeLink SET watched = 1 where link = '"+chosenSitcomLink +"'"
                        objDb.UpdateQuery(query)
                        cont = False
                        subprocess.call(["Open","-a", "/Applications/VLC.app",chosenSitcomLink],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
                    else:
                        length = len(result['data'])
                        randomInt = randint(0,length-1)
                        chosenSitcomLink = result['data'][randomInt][0]
                        query = "UPDATE tblEpisodeLink SET watched = 1 where link = '"+chosenSitcomLink +"'"
                        objDb.UpdateQuery(query)

                        cont = False
                        subprocess.call(["Open","-a", "/Applications/VLC.app",chosenSitcomLink],stdin=subprocess.PIPE,stdout=subprocess.PIPE)

            else:
                #Update the sitcom as completely watched
                query = "UPDATE tblSitcom SET complete = 1 where sitcomID = " + str(chosenSitcom)
                objDb.UpdateQuery()

        else:
            #reset all the complete & watch Indicator
            query = "UPDATE tblSitcom SET complete = 0"
            objDb.UpdateQuery()
            query = "UPDATE tblMaxSeason SET complete = 0"
            objDb.UpdateQuery()
            query = "UPDATE tblEpisodeLink SET watched = 0"
            objDb.UpdateQuery()



    except Exception as e:
        print e
        sys.exit(e)

objDb.CloseConn()

