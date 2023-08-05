import os
from Jalapeno.path import path

'''
        This file is build for future post-installation parts
        Help user get a shortcut at user's home dir
'''
def create_shortcuts():
	source = path()+os.sep+'Jalapeno'
	home = os.path.expanduser("~")
	base = home+os.sep+'Jalapeno'

	subdir = ['page','build','articleimg','configuration']
	

	page_source = source+os.sep+'page'
	page = base+os.sep+'page'

	build_source = source+os.sep+'build'
	build = source + os.sep + 'build'
	os.symlink(source,base)
