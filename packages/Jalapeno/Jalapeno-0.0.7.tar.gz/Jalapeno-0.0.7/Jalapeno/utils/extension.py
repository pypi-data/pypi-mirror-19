from Jalapeno import flk
from flask import Blueprint,send_from_directory
import os
from Jalapeno.path import path
from Jalapeno.lib.fileMgr import Mgr 
from Jalapeno.lib.url_for_builder import path_url_builder

extension = Blueprint('extension',__name__)

extension_path = path()+os.sep+'Jalapeno'+os.sep+'source'+os.sep+'extension'


extension_file_mgr = Mgr(extension_path)

@flk.context_processor
def extension_mgr():
	extensions = extension_file_mgr.tree_dict()
	extensions_dict = path_url_builder(extensions,'extension.ext')
	extensions_list = [v for k,v in extensions.items()]
	return dict(extensions = extensions_list)

@extension.route('/extension/<path:path>')
def ext(path):
	return send_from_directory(flk.config['JS_EXTENSION_DIR'],
                               path, as_attachment=True)

flk.register_blueprint(extension)