from Jalapeno.lib.jalop_markdown import Jalop_markdown
from Jalapeno import flk


@flk.template_filter('excerpt')
def excerpt_spliter(article):
    sep='<!--More-->'
    if sep in article:
        pass
    else:
        sep = '\n'
    return Jalop_markdown(article.split(sep,1)[0])
