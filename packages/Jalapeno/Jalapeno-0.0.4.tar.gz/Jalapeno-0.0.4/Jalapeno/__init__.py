from flask import Flask
import os

#Flask init
flk = Flask(__name__)
'''
from Jalapeno.utils import configuration
from Jalapeno.utils.flatpage import articles
from Jalapeno.utils import excerpt
from Jalapeno.utils import theme
from Jalapeno.utils import viewer
from Jalapeno.lib import shortcuts
from Jalapeno.utils import articleimg
from Jalapeno.utils import profile
from Jalapeno.utils.flaskfroze import freezer
'''

modules =(
		  ['Jalapeno.utils','configuration'],
		  ['Jalapeno.utils.flatpage','articles'],
		  ['Jalapeno.utils','excerpt'],
		  ['Jalapeno.utils','theme'],
		  ['Jalapeno.utils','viewer'],
		  ['Jalapeno.lib','shortcuts'],
		  ['Jalapeno.utils','articleimg'],
		  ['Jalapeno.utils.flaskfroze','freezer']
		   )

for each in modules:
	print("Loading %s ..."%each[1])
	try:
		exec('from %s import %s'%(each[0],each[1]))
	except:
		print("Loading %s Error,Exit"%each[1])