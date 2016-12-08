import os
from bottle import route, post, request, redirect, run
from bottle import TEMPLATE_PATH, jinja2_template as template

import app.models.word
word = app.models.word.Word()

# Get the full path of index.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set the path of index file
TEMPLATE_PATH.append(BASE_DIR + "../../views")

@route('/words/add')
def createWord():
	return template('add_word')

@post('/words/add/execute')
def executeAddArticle():
	word = request.forms.get('word')
	if url:
		article.addArticle(word)
		redirect("/words/list")
	return template('input_err')

@route('/words/list')
def showWordList():
	cursors = word.fetchAllWord()
	return template('word_list', cursors=cursors)

@route('/words/modify/<id:int>')
def modifyWord(id):
	cursors = word.fetchWordById(id)
	if cursors != None:
		for row in cursors:
			return template('edit_word', id=id, word=row[1])
	return showWordList()

@post('/words/modify/<id:int>/execute')
def executeModifyWord(id):
	word = request.forms.get('word')
	article.modifyWord(id, word)
	redirect("/words/list")

@route('/words/delete/<id:int>')
def deleteWord(id):
	cursors = word.deleteWord(id)
	return template('word_list', cursors=cursors)