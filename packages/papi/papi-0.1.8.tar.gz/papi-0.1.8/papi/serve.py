import logging
from papi.request import parse_request_middleware
from papi.method_override_middleware import method_override_middleware
from papi.exceptions import RestException, \
                            MalformedException, \
                            NotFoundException, \
                            MethodNotAllowedException, \
                            NotAcceptableException, \
                            ConflictException, \
                            UnsupportedMediaException, \
                            ResourceException
from traceback import format_exc
import json
import papi.fp as fp
from functools import partial
from papi.hateoas import hateoas
from papi.mime import match_mime, mime_str, parse_mime_type

logger = logging.getLogger(__name__)

def uncaught_exceptions_middleware(app):
    """WSGI-level middleware that catches any and all exceptions and translates
    them into uniform HTTP 500 errors, logging the exception itself through the
    standard logging framework.
    """
    def wrapped(env, start_response):
        try:
            return app(env, start_response)
        except Exception as e:
            logger.error("Caught exception", exc_info=True)
            start_response('500 Internal Server Error',
                [('Content-Type', 'text/json')])
            return [b'{"error":"internal server error"}']
    return wrapped

def def_api_middleware(handle, resource, request):
    """No-op API-level middleware; used as a sane default for when no
    middleware is configured.
    """
    return handle(resource, request)

def serve_resource(resource, response_writers=None, api_middleware=None):
    """Turns a resource into a WSGI application.

    Args:
        resource: The root resource for the API.
        response_writers: A list of (mime-type-string, writer), such that
            writer is a response writer function. Response writers are defined
            as:
            Args:
                body: a JSON-encodable data structure (typically composed out
                    of dict, list/tuple, and scalars)
                **kwargs: the request query string; this is passed along to
                    allow clients to pass formatting options, e.g. whether to
                    pretty-print or not.
            Returns: Encoded body as a bytestring.
        api_middleware: A middleware function that attaches at the API level.
            It is defined as:
            Args:
                handler: a request handler, taking a resource and a request,
                    and returning a triple of (status_code, headers, body)
                resource: resource to pass through to the handler
                request: request to pass through to the handler
            Returns:
                A triple of (status_code, headers, body).
    """
    if api_middleware is None:
        api_middleware = def_api_middleware
    if isinstance(response_writers, dict):
        response_writers = response_writers.items()
    def application(environ, start_response):
        try:
            request = fp.assocs(
                        [
                            ('consumed_path', ()),
                            ('remaining_path', fp.path(['request', 'path'], environ)),
                            ('response_writers', response_writers or []),
                        ],
                        environ['request'])
            try:
                status, headers, body = \
                    api_middleware(handle_resource, resource, request)
            except ResourceException as e:
                e.raise_as_rest_exception()
        except RestException as e:
            status = e.get_http_status()
            status_code, status_msg = status
            headers = [('Content-type', 'text/plain;charset=utf8')]
            body = status_msg
        status_str = "{0} {1}".format(*status)
        start_response(status_str, headers)
        if type(body) is str:
            body = body.encode('utf8')
        return body
    middlewares = fp.chain(
        uncaught_exceptions_middleware,
        method_override_middleware,
        parse_request_middleware)
    return middlewares(application)

def handle_resource(resource, request, parent_resource=None):
    """Main entry point for handling an API request. Called recursively for
    nested resources.
    """
    if resource is None:
        raise NotFoundException
    remaining_path = fp.prop('remaining_path', request)
    if len(remaining_path) == 0:
        return handle_resource_self(
            resource,
            request,
            parent_resource=parent_resource)
    else:
        child_name, new_request = consume_path_item(request)
        if not hasattr(resource, 'get_child'):
            raise NotFoundException
        child = resource.get_child(child_name)
        if child is None:
            raise NotFoundException
        return handle_resource(
            child,
            new_request,
            parent_resource=resource)

def handle_resource_self(resource, request, parent_resource):
    """Handles requests on the target resource in the resource tree. In other
    words, this function gets called when the request path has been consumed
    entirely, and thus the resource that has to do the actual handling has
    been found.
    """
    method = fp.prop('method', request).upper()
    if method == 'GET':
        return handle_resource_get(resource, request, parent_resource)
    elif method == 'POST':
        return handle_resource_post(resource, request, parent_resource)
    elif method == 'PUT':
        return handle_resource_put(resource, request, parent_resource)
    elif method == 'DELETE':
        return handle_resource_delete(resource, request, parent_resource)
    else:
        raise MethodNotAllowedException

def handle_resource_get(resource, request, parent_resource):
    """Handles a GET request on a resource
    """
    if resource is None:
        raise NotFoundException
    accepts = fp.prop('accept', request)
    for mime_pattern in accepts:
        accepted = handle_resource_get_typed(mime_pattern, resource, request)
        if accepted is not None:
            return accepted
    raise NotAcceptableException

def handle_resource_put(resource, request, parent_resource):
    """Handles a PUT request on a resource
    """
    if parent_resource is None:
        raise NotFoundException
    content_type = fp.prop('content_type', request)
    path = fp.prop('consumed_path', request)
    name = fp.last(path)
    if not hasattr(parent_resource, 'store'):
        raise MethodNotAllowedException

    input = fp.prop('input',  request)
    name, body = parent_resource.store(input, name, content_type)

    return make_json_response(hateoas(path, body))

def handle_resource_delete(resource, request, parent_resource):
    """Handles a DELETE request on a resource
    """
    if parent_resource is None:
        raise NotFoundException
    path = fp.prop('consumed_path', request)
    name = fp.last(path)
    if not hasattr(parent_resource, 'delete'):
        raise MethodNotAllowedException

    parent_resource.delete(name)

    return make_empty_response()

def handle_resource_post(resource, request, parent_resource):
    """Handles a POST request on a resource
    """
    if resource is None:
        raise NotFoundException
    content_type = fp.prop('content_type', request)
    path = fp.prop('consumed_path', request)
    if not hasattr(resource, 'create'):
        raise MethodNotAllowedException

    input = fp.prop('input',  request)
    name, body = resource.create(input, content_type)

    return make_json_response(hateoas(fp.snoc(name, path), body))

def handle_resource_get_typed(mime_pattern, resource, request):
    """Serve a 'typed' response to a GET.
    """
    binary_response = handle_resource_get_binary(mime_pattern, resource, request)
    if binary_response is not None:
        return binary_response
    return handle_resource_get_structured(mime_pattern, resource, request)

def resource_accepts_ranges(resource):
    """Check whether a resource can serve ranged bodies
    """
    return hasattr(resource, 'get_typed_body_range')

def parse_range_header(s):
    """Parse a Range header.
    Args:
        s: header value
    Returns:
        (start, end): integers indicating a left-inclusive 0-based byte range.
    """
    try:
        unit, rhs = tuple(s.split('=', 1))
    except ValueError:
        raise ResourceException(ResourceException.reason_malformed)
    if unit != 'bytes':
        # Only 'bytes' range is supported
        raise ResourceException(ResourceException.out_of_range)
    try:
        start_str, end_str = tuple(rhs.split('-'))
        start = int(start_str)
        end = int(end_str)
    except ValueError:
        raise ResourceException(ResourceException.reason_malformed)
    return (start, end)

def handle_resource_get_binary(mime_pattern, resource, request):
    """Serve a binary response (raw body as reported by resource, no HATEOAS)
    based on a given MIME type pattern.
    """
    if not hasattr(resource, 'get_typed_body'):
        return None
    accepts_ranges = resource_accepts_ranges(resource)
    range_header = request['headers'].get('Range')
    if range_header is None:
        byte_range = None
    else:
        byte_range = parse_range_header(range_header)
    if byte_range is None or not accepts_ranges:
        matched = resource.get_typed_body(mime_pattern)
    else:
        matched = resource.get_typed_body_range(mime_pattern, byte_range)
    if matched is None:
        return None
    if byte_range is None:
        mime_type, body = matched
        actual_range = None
    else:
        mime_type, body, actual_range = matched
    return make_binary_response(
        mime_type, body,
        range=actual_range,
        accepts_ranges=accepts_ranges)

def get_resource_digest(resource):
    """Get a 'digest' version of the resource's body
    """
    try:
        digest = resource.get_structured_body(digest=True)
    except AttributeError:
        digest = resource
    return digest

def get_resource_body(resource):
    """Get a full version of the resource's body
    """
    try:
        digest = resource.get_structured_body()
    except AttributeError:
        digest = resource
    return digest

def get_resource_response_writers(resource):
    """Get a list of custom response writers from a resource.
    For resources that do not supply custom response writers, an empty list is
    returned.
    """
    try:
        response_writers = resource.get_response_writers()
    except AttributeError:
        response_writers = []
    if isinstance(response_writers, dict):
        response_writers = response_writers.items()
    return [(parse_mime_type(k), v) for k, v in response_writers]

falsehoods = set(['no', '0', '', 'off'])

def bool_param(key, request, default=False):
    """Leniently get a boolean from a request's query string.
    """
    query = fp.prop('query', request)
    return query.get(key, default) not in falsehoods

def int_param(key, request):
    """Get an integer value from a request's query string.
    """
    p = fp.path(('query', key), request)
    print("{0}: {1}".format(key, p))
    if p is None or p == '':
        return None
    try:
        return int(p)
    except ValueError:
        raise MalformedException()

class Filter(object):
    def __init__(self, propname, value, operator):
        self.propname = propname
        self.value = value
        self.operator = operator

def parse_filter(src):
    # TODO: currently only supports name:value syntax; needs more operators and
    # a proper parser
    propname, raw_value = tuple(src.split(':', 1))
    return Filter(propname, raw_value, "equals")

def parse_filters_param(key, request):
    p = fp.path(('query', key), request)
    if p is None or p == '':
        return None
    return tuple(map(parse_filter, p.split(',')))

def parse_ordering(src):
    descending = False
    src = src.strip()
    if src.startswith('-'):
        descending = True
        src = src[1:]
    elif src.startswith('+'):
        descending = False
        src = src[1:]
    if src.endswith('-'):
        descending = True
        src = src[:-1]
    elif src.endswith('+'):
        descending = False
        src = src[:-1]
    return (descending, src)

def parse_orderings(p):
    return tuple(map(parse_ordering, p.split(',')))

def parse_orderings_param(key, request):
    p = fp.path(('query', key), request)
    if p is None or p == '':
        return None
    return parse_orderings(p)

def handle_resource_get_structured(mime_pattern, resource, request):
    """Serve a 'structured' response.
    
    A structured response is constructed from a native data structure returned
    by the resource, to which we add HATEOAS metadata, and then feed it through
    a suitable response writer (which also covers content type negotiation),
    which yields a serialized body.
    """
    if hasattr(resource, 'get_structured_body'):
        raw_body = resource.get_structured_body()
    else:
        raw_body = {}
    current_path = fp.prop('consumed_path', request)
    name = fp.last(current_path)

    offset = int_param('offset', request)
    page = int_param('page', request)
    count = int_param('count', request)
    filters = parse_filters_param('where', request)
    order = parse_orderings_param('order', request)
    calculated_offset = offset
    if offset is None and count is not None and page is not None:
        calculated_offset = (page - 1) * count
    if offset is None and page is None:
        page = 1

    use_hateoas = bool_param('hateoas', request, True)
    print(use_hateoas)
    def add_hateoas(name, current_path, raw_body, page=None, offset=None, count=None, pageable=True):
        if use_hateoas:
            body = hateoas(current_path, raw_body, page, offset, count, pageable)
            if name is not None:
                body['_name'] = name
            return body
        else:
            return raw_body or {}
    print("PAGE: {0}".format(page))
    body = add_hateoas(name, current_path, raw_body, page, offset, count)

    if hasattr(resource, 'get_children'):
        children = resource.get_children(
            offset=calculated_offset,
            count=count,
            filters=filters,
            order=order)
    else:
        children = None
    if children is not None:
        children_alist = [
            (k, get_resource_digest(v), hasattr(v, 'get_children')) for k, v in children
        ]

        def prepare_child(kvp):
            name, value, pageable = kvp
            if use_hateoas and not isinstance(value, dict):
                value = {'_value': value}
            return fp.chain(
                    partial(add_hateoas, name, fp.snoc(name, current_path), pageable=pageable)
                )(raw_body=value)

        children_list = list(map(prepare_child, children_alist))
        body['_items'] = children_list

    response_writers = fp.concat([
        fp.prop('response_writers', request) or [],
        get_resource_response_writers(resource) or [],
        default_response_writers,
    ])
    query = fp.prop('query', request)
    for mime_type, response_writer in response_writers:
        if match_mime(mime_pattern, mime_type, ["charset"]):
            converted = response_writer(body, **query)
            return make_binary_response(mime_type, converted)

def json_writer(data, **query):
    """A response writer for JSON.
    Accepts one keyword argument:
        pretty: if present, pretty-print the output with a two-space indent.
    """
    kwargs = {}
    if query.get('pretty'):
        kwargs['indent'] = 2
    return json.dumps(data, **kwargs)

default_response_writers = [
    (parse_mime_type(k), v)
    for (k, v)
    in [
        ('text/json', json_writer),
        ('application/json', json_writer),
       ]
]

def consume_path_item(request):
    """Snatch one element from the request path.
    Args:
        request: A request object
    Returns:
        item: the snatched element, or None if the path was empty
        new_request: the updated request, with the rest of the request path in
            the 'remaining_path' key.
    """
    first_item = fp.head(fp.prop('remaining_path', request))
    if first_item is None:
        return None, request
    new_request = fp.chain(
        partial(
            fp.Lens.over,
            fp.prop_lens('remaining_path'),
            partial(fp.drop, 1)),
        partial(
            fp.Lens.over,
            fp.prop_lens('consumed_path'),
            partial(fp.snoc, first_item)))(request)
    return first_item, new_request

def make_json_response(
        data,
        status=200,
        headers=None):
    content_type = 'application/json'
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = json.dumps(data)
    if type(body) is str:
        body = body.encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

def make_binary_response(
        mime_type,
        data,
        status=None,
        headers=None,
        range=None,
        accepts_ranges=False):
    def_status = 200 if range is None else 206
    status = status or def_status
    content_type = mime_str(mime_type)
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    if range is not None:
        headers.append(('Content-Range', format_range(range)))
    if accepts_ranges:
        headers.append(('Accept-Ranges', 'bytes'))
    if type(data) is bytes:
        body = data
    else:
        body = str(data).encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

def make_empty_response(mime_type=None, status=204, headers=None):
    content_type = mime_str(mime_type or parse_mime_type("text/plain"))
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = b""
    return ((status, status_names.get(status, 'OK')), headers, body)

def format_range(range):
    """Format a range into a string suitable for a Content-Range: header.
    """
    return "bytes {0}-{1}/{2}".format(*range)

status_names = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    206: 'Partial Content',
}
