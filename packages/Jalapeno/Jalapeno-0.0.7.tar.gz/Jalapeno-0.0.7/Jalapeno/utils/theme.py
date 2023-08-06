import os
from Jalapeno.lib import themeMgr
from Jalapeno import flk
from flask import url_for
from Jalapeno.utils.profile import profile
'''
	This file is going to manage the theme
	get the templates and static
	push static dict to asset
'''


theme_name = profile['Theme']
theme = themeMgr.Theme(theme_name)
flk.static_folder = theme.static_path()
flk.template_folder = theme.template_path()


@flk.context_processor
def theme_processor():
	
	assets = theme.static_url_for()
	
	return dict(asset=assets)
