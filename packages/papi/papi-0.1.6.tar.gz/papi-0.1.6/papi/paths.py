import papi.fp as fp
import urllib.parse
from functools import partial

def quote_path_elem(e):
    return urllib.parse.quote(e, safe='', encoding='utf-8')

def quote_query_name(n):
    return urllib.parse.quote(str(n), safe=';/?$,:', encoding='utf-8')

def quote_query_value(n):
    return urllib.parse.quote(str(n), safe=';/?$,:=', encoding='utf-8')

def join_path(path):
    return '/' + '/'.join(fp.fmap(quote_path_elem, fp.flatten(path)))

def join_query(query):
    return '?' + '&'.join(( \
        "{0}={1}".format(quote_query_name(name), quote_query_value(value)) \
        for name, value in sorted(query.items())))

def join_url(protocol=None, domain=None, path=None, query=None):
    result = ""
    if domain is not None:
        if protocol is not None:
            result += protocol
            result += ":"
        result += "//"
        result += domain
    if path is not None:
        result += join_path(path)
    if query is not None and query != {}:
        result += join_query(query)
    return result


