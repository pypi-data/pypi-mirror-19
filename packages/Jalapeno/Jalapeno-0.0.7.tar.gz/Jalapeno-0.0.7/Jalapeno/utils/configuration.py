from Jalapeno import flk
import os
from Jalapeno.path import path

config_flatpage = path()+os.sep+'Jalapeno'+os.sep+'configuration'
flk.config.from_pyfile(config_flatpage+os.sep+'_config.py')