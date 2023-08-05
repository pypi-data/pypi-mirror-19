from Jalapeno import flk 
from Jalapeno.lib.fileMgr import Mgr 
import os
from Jalapeno.utils.profile import profile
from Jalapeno.path import path



file_mgr = Mgr(path())
views = profile['views']
for each in views:
        exec('from Jalapeno.views.%s import %s'%(each,each))
        flk.register_blueprint(eval(each))

'''

from Jalapeno.views.article import article
from Jalapeno.views.postwall import postwall
from Jalapeno.views.copyright import copyright
flk.register_blueprint(copyright)
flk.register_blueprint(article)
flk.register_blueprint(postwall)'''