from markupsafe import Markup
from flask_flatpages import pygmented_markdown
from Jalapeno import flk
from flask import render_template_string


@flk.template_filter('excerpt')
def excerpt_spliter(article):
    sep='<!--More-->'
    if sep in article:
        pass
    else:
        sep = '\n'
    #return Markup(pygmented_markdown(article.split(sep,1)[0]))
    return Markup(pygmented_markdown(render_template_string(article.split(sep,1)[0])))