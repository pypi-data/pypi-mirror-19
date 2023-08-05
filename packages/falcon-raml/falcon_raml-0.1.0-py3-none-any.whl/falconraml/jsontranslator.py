import json
import falcon


class JsonTranslator(object):
    """Translate from plain text to python objects."""

    def process_request(self, request, response):
        """Translate plain text to python objects in the request.

        Translated JSON is stored in request.context['json'].

        The translation will only be done if all the following conditions are
        satisfied:

        1. The content length is more than 0.
        2. The content type is "application/json".
        3. The request body can be successful parsed as a json object.

        Note that after this middleware, request.stream will left to EOF.
        """
        request.context['json'] = None

        if request.content_length in (None, 0):
            return
        if request.content_type != 'application/json':
            return

        json_bytes = request.stream.read()

        try:
            json_str = json_bytes.decode('utf8')
        except UnicodeDecodeError:
            raise falcon.HTTPBadRequest('Bad string', 'Unicode decode error')

        try:
            request.context['json'] = json.loads(json_str)
        except json.decoder.JSONDecodeError:
            raise falcon.HTTPBadRequest('Bad json', 'JSON decode error')
