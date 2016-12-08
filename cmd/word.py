import os
import pymysql

conn = pymysql.connect( host = 'localhost', unix_socket = '/var/mysql/mysql.sock', user = 'root', password = os.environ['MYSQL_PW'], db = 'mysql' )

cur = conn.cursor()
cur.execute( "USE reading_record" )

#--------------------
# function: add word 
#--------------------
def addWord( word = None, article_id = None ):
	if word == None:
		return

	word = word.replace('_', ' ')
	cur.execute( "SELECT * FROM word WHERE word = %s", ( word ) )
	if cur.rowcount == 0:
		cur.execute( "INSERT INTO word ( word, article_id ) VALUES ( %s, %s )", ( word, article_id ) )
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
		print( ' id | word | article_id' )
		print( '------------------------' )
		for row in cur:
			print( '{}: {} [{}]'.format(row[0], row[1], row[2]) )
		print( '\n' )
	return
# def showWord End #

#-------------------------------------------
# function: show word in a specific article 
#-------------------------------------------
def showWordByArticle( article_ids = None ):
	if len( article_ids ) < 2:
		return
	else:
		article_ids.pop( 0 )

	print( '\n' )
	print( ' id | url | article_id' )
	print( '-----------------------' )

	found = False
	cur.execute("SELECT * FROM word WHERE article_id IS NOT NULL" )
	if cur.rowcount != 0:
		for row in cur:
			for article_id in article_ids:
				if article_id == row[2]:
					print( '{}: {} [{}]'.format(row[0], row[1], row[2]) )
					if found == False:
						found = True
					break

	if found == False:
		print("no word is found")

	print( '\n' )
	
	return
# def showWordByArticle End #

#-------------------------------------
# function: modify word or article id  
#-------------------------------------
def modifyWord( id = None, col = None ):
	if id == None:
		return

	if col == 'word':
		cur.execute( "SELECT * FROM word WHERE word = %s", (word) )
		if cur.rowcount == 0:
			print( "the word doesn't exist" )
		else:
			word = input( "new word: " )
			cur.execute( "UPDATE word SET word = %s WHERE word = %s", (word) )
			conn.commit()
	elif col == 'id':
		cur.execute( "SELECT * FROM word WHERE article_id = %s", (int(id)) )
		if cur.rowcount == 0:
			print( "the word doesn't exist" )
		else:
			article_id = input( "new article id: " )
			cur.execute( "UPDATE word SET article_id = %s WHERE article_id = %s", (int(article_id)) )
			conn.commit()
	else:
		print( "spicify word or article id to modify" )

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
