from flask import Blueprint, render_template,url_for
from Jalapeno import flk 
about = Blueprint('about',__name__)

@about.route('/about')
def me():
	
	
	return render_template('about.html')