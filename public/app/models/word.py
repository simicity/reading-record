import os
import pymysql

class Word:
	def __init__( self ):
		self.conn = pymysql.connect( host = 'localhost', unix_socket = '/var/mysql/mysql.sock', user = 'root', password = os.environ['MYSQL_PW'], db = 'mysql' )
		self.cur = self.conn.cursor()
		self.cur.execute( "USE reading_record" )	

	#--------------------
	# function: add word 
	#--------------------
	def addWord( self, word = None ):
		if word == None:
			return	

		self.cur.execute( "SELECT * FROM word WHERE word = %s", ( word ) )
		if self.cur.rowcount == 0:
			self.cur.execute( "INSERT INTO word ( word ) VALUES ( %s )", ( word ) )
			self.conn.commit()	

		return
	# def addWord End #	

	#--------------------------
	# function: fetch all word 
	#--------------------------
	def fetchAllWord( self ):
		self.cur.execute( "SELECT * FROM word" )
		if self.cur.rowcount != 0:
			return self.cur	

		return
	# def fetchAllWord End #

	#----------------------------
	# function: fetch word by id 
	#----------------------------
	def fetchWordById( self, id ):
		if id == None:
			return	

		self.cur.execute("SELECT * FROM word WHERE id = %s", (id) )
		if self.cur.rowcount != 0:
			return self.cur
		
		return
	# def fetchWordById End #	

	#-------------------------------------
	# function: modify word or article id  
	#-------------------------------------
	def modifyWord( self, id = None, word = None ):
		if id == None:
			return	

		self.cur.execute( "SELECT * FROM word WHERE word = %s", ( word ) )
		if self.cur.rowcount != 0:
			self.cur.execute( "UPDATE word SET word = %s WHERE word = %s", ( word ) )
			self.conn.commit()	

		return
	# def modifyWord End #	

	#--------------------------
	# function: delete word 
	#--------------------------
	def deleteWord( self, id ):
		if id == None:
			return	

		self.cur.execute( "SELECT * FROM word WHERE id = %s", (int(id)) )
		if self.cur.rowcount != 0:
			self.cur.execute( "DELETE FROM word WHERE id = %s", (int(id)) )
			self.conn.commit()	

		return
	# def deleteWord End #
