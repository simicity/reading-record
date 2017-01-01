import os
import pymysql
import webbrowser
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse

class Article:
	def __init__( self ):
		self.conn = pymysql.connect( host = 'localhost', unix_socket = '/var/mysql/mysql.sock', user = 'root', password = os.environ['MYSQL_PW'], db = 'mysql' )	
		self.cur = self.conn.cursor()
		self.cur.execute( "USE reading_record" )	

	#--------------------------------
	# function: add article with tag 
	#--------------------------------
	def addArticle( self, url = None, tag = None ):
		if url == None:
			return	

		self.cur.execute( "SELECT * FROM article WHERE url = %s", (url) )
		if self.cur.rowcount == 0:
			self.cur.execute( "INSERT INTO article ( url, tag, last_modified ) VALUES ( %s, %s, CURRENT_DATE() )", ( url, tag ) )
			self.conn.commit()	

		return
	# def addArticle End #	

	#-----------------------------
	# function: fetch all article 
	#-----------------------------
	def fetchAllArticle( self ):
		self.cur.execute( "SELECT * FROM article" )
		if self.cur.rowcount != 0:
			return self.cur	

		return
	# def fetchAllArticle End #	

	#-------------------------------
	# function: fetch article by id 
	#-------------------------------
	def fetchArticleById( self, id ):
		if id == None:
			return	

		self.cur.execute("SELECT * FROM article WHERE id = %s", (id) )
		if self.cur.rowcount != 0:
			return self.cur
		
		return
	# def fetchArticleByTag End #

	#--------------------------------
	# function: fetch article by tag 
	#--------------------------------
	def fetchArticleByTag( self, tag = None ):
		if tag == None:
			return	

		self.cur.execute("SELECT * FROM article WHERE tag = %s", (tag) )
		if self.cur.rowcount != 0:
			return self.cur
		
		return
	# def fetchArticleByTag End #

	#---------------------------------
	# function: fetch article by word 
	#---------------------------------
	def fetchArticleByWord( self, word = None ):
		if word == None:
			return	

		self.cur.execute("SELECT * FROM article")
		if self.cur.rowcount != 0:
			has_word = set()
			for row in self.cur:
				try:
					pagetext = urlopen(row[1]).read().decode()
					if word in pagetext:
						print(word)
						has_word.add(row[0])
				except HTTPError as e:
					continue
				except URLError as e:
					continue
				else:
					continue

		return has_word
	# def fetchArticleByWord End #	

	#-------------------------------
	# function: modify article info 
	#-------------------------------
	def modifyArticle( self, id = None, url = None, tag = None ):
		if id == None:
			return	

		self.cur.execute( "SELECT * FROM article WHERE id = %s", (int(id)) )
		if self.cur.rowcount != 0:
			self.cur.execute( "UPDATE article SET url = %s, tag = %s, last_modified = CURRENT_DATE() WHERE id = %s", (url, tag, int(id)) )
			self.conn.commit()	

		return
	# def modifyArticle End #	

	#--------------------------
	# function: delete article 
	#--------------------------
	def deleteArticle( self, id ):
		if id == None:
			return	

		self.cur.execute( "SELECT * FROM article WHERE id = %s", (int(id)) )
		if self.cur.rowcount != 0:
			self.cur.execute( "DELETE FROM article WHERE id = %s", (int(id)) )
			self.conn.commit()	

		return
	# def deleteArticle End #	
