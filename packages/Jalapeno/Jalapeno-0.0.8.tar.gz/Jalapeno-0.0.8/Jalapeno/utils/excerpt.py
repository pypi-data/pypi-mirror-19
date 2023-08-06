from Jalapeno.lib.jalop_markdown import Jalop_markdown
from Jalapeno import flk
'''

@flk.template_filter('excerpt')
def excerpt_spliter(article):
    
    sidesep = '<!--Sidebar-->'

    if sidesep in article:
        article = article.split(sidesep,1)[1]
        print(article)

    sep='<!--More-->'
    if sep in article:
        pass
    else:
        sep = '\n'
    return Jalop_markdown(article.split(sep,1)[0])




@flk.template_filter('sidebar')
def excerpt_spliter(article):
    
    sidesep = '<!--Sidebar-->'
    if sidesep in article:
        pass
    else:
        sep = '\n'
    return Jalop_markdown(article.split(sidesep,1)[0])
    '''

@flk.template_filter('excerpt')
def excerpt_spliter(article):

    content = Jalop_markdown(article)
    
    sidesep = '<!--Sidebar-->'

    if sidesep in content:
        content = content.split(sidesep,1)[1]

    sep='<!--More-->'
    return content.split(sep,1)[0] if sep in content else content


@flk.template_filter('content')
def content_spliter(article):

    content = Jalop_markdown(article)
    sep='<!--More-->'
    return content.split(sep,1)[1] if sep in content else content


@flk.template_filter('sidebar')
def content_spliter(article):

    content = Jalop_markdown(article)
    sep='<!--Sidebar-->'
    return content.split(sep,1)[0] if sep in content else content



























