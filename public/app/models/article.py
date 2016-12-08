import os
import pymysql
import webbrowser
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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
			for row in self.cur:
				articleBsObj = self.getConnection( row[1] )
				if word not in articleBsObj.text:
					self.cur.remove(row)
			return self.cur	

		return
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

	#---------------------------
	# function: connect to page 
	#---------------------------
	def getConnection( self, url ):
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