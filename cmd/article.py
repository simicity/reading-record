import os
import pymysql
#import argparse
import webbrowser
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup

conn = pymysql.connect( host = 'localhost', unix_socket = '/var/mysql/mysql.sock', user = 'root', password = os.environ['MYSQL_PW'], db = 'mysql' )

cur = conn.cursor()
cur.execute( "USE reading_record" )

#--------------------------------
# function: add article with tag 
#--------------------------------
def addArticle( url = None, tag = None ):
	if url == None:
		return

	cur.execute( "SELECT * FROM article WHERE url = %s", (url) )
	if cur.rowcount == 0:
		cur.execute( "INSERT INTO article ( url, tag, last_modified ) VALUES ( %s, %s, CURRENT_DATE() )", ( url, tag ) )
		conn.commit()
	else:
		print( "the article already exists" )
	return
# def addArticle End #

#----------------------------
# function: show all article 
#----------------------------
def showArticle():
	cur.execute( "SELECT * FROM article" )
	if cur.rowcount == 0:
		print( "no article exists" )
	else:
		print( '\n' )
		print( ' id | url | tag | modified' )
		print( '---------------------------' )
		for row in cur:
			print( '{}: {} [{}] ({})'.format(row[0], row[1], row[2], row[3]) )
		print( '\n' )
	return
# def showArticle End #

#-------------------------------------------
# function: show article with arbitrary tag 
#-------------------------------------------
def showArticleByTag( tags = None ):
	if len( tags ) < 2:
		return
	else:
		tags.pop( 0 )

	print( '\n' )
	print( ' id | url | tag | modified' )
	print( '---------------------------' )

	found = False
	cur.execute("SELECT * FROM article WHERE tag IS NOT NULL" )
	if cur.rowcount != 0:
		for row in cur:
			for tag in tags:
				if tag == row[2]:
					print( '{}: {} [{}] ({})'.format(row[0], row[1], row[2], row[3]) )
					if found == False:
						found = True
					break

	if found == False:
		print("no article is found")

	print( '\n' )
	
	return
# def showArticleByTag End #

#--------------------------------
# function: find article by word 
#--------------------------------
def findArticleByWord( words = None ):
	if words == None:
		return

	cur.execute("SELECT * FROM article" )
	if cur.rowcount == 0:
		print("no article is found")
	else:
		print( '\n' )
		print( ' id | url | tag | modified' )
		print( '---------------------------' )

		found = False
		for row in cur:
			articleBsObj = getConnection( row[1] )
			for word in words:
				if word in articleBsObj.text:
					print( '{}: {} [{}] ({})'.format(row[0], row[1], row[2], row[3]) )
					if found == False:
						found = True
					break

		if found == False:
			print("no article is found")

		print( '\n' )

	return
# def findArticleByWord End #

#-------------------------------
# function: modify article info 
#-------------------------------
def modifyArticle( id = None, col = None ):
	if id == None:
		return

	if col == 'url':
		cur.execute( "SELECT * FROM article WHERE id = %s", (int(id)) )
		if cur.rowcount == 0:
			print( "the article doesn't exist" )
		else:
			url = input( "new url: " )
			cur.execute( "UPDATE article SET url = %s, last_modified = CURRENT_DATE() WHERE id = %s", (url, int(id)) )
			conn.commit()
	elif col == 'tag':
		cur.execute( "SELECT * FROM article WHERE id = %s", (int(id)) )
		if cur.rowcount == 0:
			print( "the article doesn't exist" )
		else:
			tag = input( "new tag: " )
			cur.execute( "UPDATE article SET tag = %s, last_modified = CURRENT_DATE() WHERE id = %s", (tag, int(id)) )
			conn.commit()
	else:
		print( "spicify url or tag to modify" )

	return
# def modifyArticle End #

#--------------------------
# function: delete article 
#--------------------------
def deleteArticle( ids ):
	if ids == None:
		return

	for id in ids:
		cur.execute( "SELECT * FROM article WHERE id = %s", (int(id)) )
		if cur.rowcount == 0:
			print( "article #{} doesn't exists", (int(id)) )
		else:
			cur.execute( "DELETE FROM article WHERE id = %s", (int(id)) )
			conn.commit()

	return
# def deleteArticle End #

#----------------------------------
# function: open article in safari 
#----------------------------------
def openArticle( ids = None ):
	if ids == None:
		return

	for id in ids:
		cur.execute( "SELECT * FROM article WHERE id = %s", (int(id)) )
		if cur.rowcount != 0:
			for row in cur:
				if row[1] != None:
					webbrowser.get( 'safari' ).open_new_tab( row[1] )
				break

	return
# def openArticle End #

#---------------------------
# function: connect to page 
#---------------------------
def getConnection( url ):
	try:
		html = urlopen( url )
		bsObj = BeautifulSoup( html, "html.parser" )
		return bsObj
	except HTTPError as e:
		print(e)
		return None
	except URLError as e:
		print("Not found")
		return None
	return
# def getConnection End #