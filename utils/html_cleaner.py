import re

def clear_html_tag(html):
    return re.sub(r'<.*?>', '', html)