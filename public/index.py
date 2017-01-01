# -*- coding: utf-8 -*-
 
import os
 
from bottle import route, run, static_file
from bottle import TEMPLATE_PATH, jinja2_template as template
#from bottle import static_file

from app.controllers.article import *
from app.controllers.word import *

# Get the full path of index.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set the path of index file
TEMPLATE_PATH.append(BASE_DIR + "/views")

@route('/css/<filename>')
@route('/articles/css/<filename>')
@route('/articles/list/tag/css/<filename>')
@route('/articles/list/word/css/<filename>')
@route('/articles/add/css/<filename>')
@route('/articles/modify/css/<filename>')
@route('/words/css/<filename>')
@route('/words/modify/css/<filename>')
def css_dir(filename):
    return static_file(filename, root=BASE_DIR+"/static/css")

@route('/js/<filename>')
@route('/articles/js/<filename>')
@route('/articles/list/tag/js/<filename>')
@route('/articles/list/word/js/<filename>')
@route('/articles/add/js/<filename>')
@route('/articles/modify/js/<filename>')
@route('/words/js/<filename>')
@route('/words/modify/js/<filename>')
def js_dir(filename):
    return static_file(filename, root=BASE_DIR+"/static/js")

@route('/font/<filename>')
@route('/articles/font/<filename>')
@route('/articles/list/tag/font/<filename>')
@route('/articles/list/word/font/<filename>')
@route('/articles/add/font/<filename>')
@route('/articles/modify/font/<filename>')
@route('/words/font/<filename>')
@route('/words/modify/font/<filename>')
def font_dir(filename):
    return static_file(filename, root=BASE_DIR+"/static/fonts")

@route('/')
@route('/top')
def top():
    return template('top')
 
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)