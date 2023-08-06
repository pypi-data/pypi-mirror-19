from flask import Blueprint, render_template,url_for
from Jalapeno.utils.flatpage import articles
from Jalapeno import flk
from Jalapeno.utils.profile import profile
from Jalapeno.lib import pagination as Pag
tags = Blueprint('tags',__name__)


@tags.route('/tag/<path:tag>/')
@tags.route('/tag/<path:tag>/<int:page>/')
def posts(tag,page=1):

	print(tag)
	posts = [article for article in articles if 'date' in article.meta and tag == article.meta['tag']]

	PER_PAGE = 6

	sorted_posts = sorted(posts,reverse = True,key = lambda page:page.meta['date'])
	

	if profile['Pagination']:
		pager_obj = Pag.Pagination(page,PER_PAGE,sorted_posts)
	else:
		pager_obj = sorted_posts

	return render_template('index.html',pagination = pager_obj)#,asset = static_assets)



