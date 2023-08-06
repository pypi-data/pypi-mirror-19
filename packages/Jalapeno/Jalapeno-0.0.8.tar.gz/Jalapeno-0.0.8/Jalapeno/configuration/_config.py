import os
from Jalapeno.path import path
from Jalapeno.lib.jalop_markdown import Jalop_markdown





#REPO_NAME = "what-is-this"
DEBUG = True


#APP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = path()+os.sep+'Jalapeno'

IMAGE_DIR = APP_DIR+os.sep+'source'+os.sep+'image'
JS_EXTENSION_DIR = APP_DIR+os.sep+'source'+os.sep+'extension'

def parent_dir(path):
	return os.path.abspath(os.path.join(path,os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)+os.sep+'Jalapeno'+os.sep+'build'

FREEZER_DESTINATION = PROJECT_ROOT

FREEZER_REMOVE_EXTRA_FILES = False


FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite','tables','toc','markdown.extensions.meta']

FLATPAGES_ROOT = os.path.join(APP_DIR,'source'+os.sep+'pages')
#FLATPAGES_ROOT = APP_DIR+'/source' 
FLATPAGES_EXTENSION ='.md'


#deal with the jinja render before markup



FLATPAGES_HTML_RENDERER = Jalop_markdown