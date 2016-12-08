# -*- coding: utf-8 -*-
 
import os
 
from bottle import route, run
from bottle import TEMPLATE_PATH, jinja2_template as template
#from bottle import static_file

from app.controllers.article import *
from app.controllers.word import *

# Get the full path of index.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set the path of index file
TEMPLATE_PATH.append(BASE_DIR + "/views")

@route('/')
@route('/top')
def top():
    return template('top')
 
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)