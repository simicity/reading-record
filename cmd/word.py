import os
import pymysql

conn = pymysql.connect( host = 'localhost', unix_socket = '/var/mysql/mysql.sock', user = 'root', password = os.environ['MYSQL_PW'], db = 'mysql' )

cur = conn.cursor()
cur.execute( "USE reading_record" )

#--------------------
# function: add word 
#--------------------
def addWord( word = None ):
	if word == None:
		return

	word = word.replace('_', ' ')
	cur.execute( "SELECT * FROM word WHERE word = %s", ( word ) )
	if cur.rowcount == 0:
		cur.execute( "INSERT INTO word ( word ) VALUES ( %s )", ( word ) )
		conn.commit()
	else:
		print( "the word already exists" )
	return
# def addWord End #

#-------------------------
# function: show all word 
#-------------------------
def showWord():
	cur.execute( "SELECT * FROM word" )
	if cur.rowcount == 0:
		print( "no word exists" )
	else:
		print( '\n' )
		print( ' id | word ' )
		print( '-----------' )
		for row in cur:
			print( '{}: {}'.format(row[0], row[1]) )
		print( '\n' )
	return
# def showWord End #

#-------------------------------------
# function: modify word or article id  
#-------------------------------------
def modifyWord( id = None, word = None ):
	if id == None:
		return

	cur.execute( "SELECT * FROM word WHERE word = %s", (word) )
	if cur.rowcount == 0:
		print( "the word doesn't exist" )
	else:
		word = word.replace('_', ' ')
		cur.execute( "UPDATE word SET word = %s WHERE word = %s", (word) )
		conn.commit()

	return
# def modifyWord End #

#--------------------------
# function: delete word 
#--------------------------
def deleteWord( ids ):
	if ids == None:
		return

	for id in ids:
		cur.execute( "SELECT * FROM word WHERE id = %s", (int(id)) )
		if cur.rowcount == 0:
			print( "word #{} doesn't exists", (int(id)) )
		else:
			cur.execute( "DELETE FROM word WHERE id = %s", (int(id)) )
			conn.commit()

	return
# def deleteWord End #
