import json

from django.http import HttpResponse


class JSONResponse(HttpResponse):
    """ Base response class for encoding stuff to JSON
    """
    def __init__(self, data, *args, **kwargs):
        payload = json.dumps(data)
        kwargs['content_type'] = 'text/json'
        super(JSONResponse, self).__init__(payload, *args, **kwargs)


class JSONResponseError(JSONResponse):
    """ Base response for API errors, with a code and description
    An optional message can be passed along as well, so we know whats acutally
    going on
    """
    def __init__(self, exception=None, *args, **kwargs):
        data = {'success': False, 'error': self.reason_phrase}
        if exception and exception.message:
            data['message'] = exception.message
        payload = json.dumps(data)
        kwargs['content_type'] = 'text/json'
        super(JSONResponse, self).__init__(payload, *args, **kwargs)


class JSONResponseNotFound(JSONResponseError):
    status_code = 404
    reason_phrase = 'NOT FOUND'


class JSONResponseUnauthorized(JSONResponseError):
    status_code = 401
    reason_phrase = 'UNAUTHORIZED'


class JSONResponseBadRequest(JSONResponseError):
    status_code = 400
    reason_phrase = 'BAD REQUEST'


class JSONResponseNotImplemented(JSONResponseError):
    status_code = 501
    reason_phrase = 'NOT IMPLEMENTED'

