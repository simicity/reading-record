import os
from bottle import route, post, request, redirect, run
from bottle import TEMPLATE_PATH, jinja2_template as template

import app.models.article
article = app.models.article.Article()

# Get the full path of index.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set the path of index file
TEMPLATE_PATH.append(BASE_DIR + "../../views")

@route('/articles/add')
def addArticle():
	return template('add_article')

@post('/articles/add/execute')
def executeAddArticle():
	url = request.forms.get('url')
	tag = request.forms.get('tag')
	if url:
		article.addArticle(url, tag)
		redirect("/articles/list")
	return template('add_article_err')

@route('/articles/list')
def showArticleList():
	cursors = article.fetchAllArticle()
	return template('article_list', cursors=cursors)

@route('/articles/list/tag/<tag>')
def findArticleByTag(tag):
	cursors = article.fetchArticleByTag(tag)
	if cursors != None:
		return template('article_list', cursors=cursors)
	return showArticleList()

@route('/articles/list/word/<word>')
def findArticleByWord(word):
	has_word = article.fetchArticleByWord(word)
	cursors = article.fetchAllArticle()
	if cursors != None:
		return template('article_list_word', cursors=cursors, has_word=has_word)
	return showArticleList()

@route('/articles/modify/<id:int>')
def modifyArticle(id):
	cursors = article.fetchArticleById(id)
	if cursors != None:
		for row in cursors:
			return template('edit_article', id=id, url=row[1], tag=row[2])
	return showArticleList()

@post('/articles/modify/<id:int>/execute')
def executeModifyArticle(id):
	url = request.forms.get('url')
	tag = request.forms.get('tag')
	if url:
		article.modifyArticle(id, url, tag)
		redirect("/articles/list")
	return template('modify_article_err')

@route('/articles/delete/<id:int>')
def deleteArticle(id):
	article.deleteArticle(id)
	redirect("/articles/list")