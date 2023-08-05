import falcon
import ramlfications
import jsonschema


class ParameterChecker(object):
    """Check parameters with RAML."""

    def __init__(self, raml_file_path):
        """Load the RAML file."""
        self._raml = ramlfications.parse(raml_file_path)

    def process_resource(self, request, response, falcon_resource, uri_params):
        """Check parameters in the request.

        This function checks 3 parts:

        1. headers
        2. query parameters
        3. body
          a. json body
          b. form body parameters

        Note that it overrides process_resource instead of process_request
        because request.uri_template maybe None in process_request.
        Please see:
        http://falcon.readthedocs.io/en/stable/api/request_and_response.html#Request.uri_template
        """
        raml_resource = \
            self._get_raml_resource(request.method, request.uri_template)

        if raml_resource is None:
            return

        if raml_resource.headers:
            for header in raml_resource.headers:
                self._check_header(request, header)

        if raml_resource.query_params:
            for query_param in raml_resource.query_params:
                self._check_param(request, query_param)

        if raml_resource.body:
            if request.content_type is None:
                raise falcon.HTTPBadRequest('Bad request', 'No content type')
            matched = False
            for body in raml_resource.body:
                if body.mime_type != request.content_type:
                    continue
                matched = True
                if body.mime_type == 'application/json':
                    self._check_json_body(request, body.schema)
                elif body.mime_type == 'application/x-www-form-urlencoded':
                    for form_param_tuple in body.form_params.items():
                        form_param = self._make_form_param(form_param_tuple)
                        self._check_param(request, form_param)
                else:
                    # No other content type is supported yet
                    matched = False
            if not matched:
                raise falcon.HTTPBadRequest(
                    'Bad request',
                    'Unsupported content type: {}'.format(request.content_type)
                )

    def _get_raml_resource(self, method, uri_template):
        """Get the RAML resource by method and URI template.

        This is the best we can do for now:
        https://github.com/spotify/ramlfications/issues/112
        """
        for raml_resource in self._raml.resources:
            if raml_resource.method is None or raml_resource.path is None:
                continue
            if raml_resource.method.lower() != method.lower():
                continue
            if uri_template != raml_resource.path:
                continue
            return raml_resource
        return None

    def _check_header(self, request, raml_header):
        """Check if the request headers are valid.

        It checks 2 things:

        1. the existence (if required)
        2. the type (if given)

        It raises HTTPMissingHeader and HTTPInvalidHeader,
        respectively.
        """
        header = request.get_header(raml_header.display_name)

        if raml_header.required and header is None:
            raise falcon.HTTPMissingHeader(raml_header.display_name)

        if raml_header.type and header is not None:
            self.check_value_with_raml_type(
                raml_header,
                header,
                falcon.HTTPInvalidHeader
            )

    def _check_param(self, request, raml_param):
        """Check if the request parameters are valid.

        The behavior of this function is like _check_header, but
        for query parameters and body form parameters.
        """
        param = request.get_param(raml_param.name)

        if raml_param.required and param is None:
            raise falcon.HTTPMissingParam(raml_param.name)

        if raml_param.type and param is not None:
            self.check_value_with_raml_type(
                raml_param,
                param,
                falcon.HTTPInvalidParam
            )

    def _check_json_body(self, request, raml_json_body_schema):
        """Check JSON body with jsonschema.

        This function works only if falconraml.JsonTranslator
        is used in the middlewares.
        """
        if 'json' not in request.context:
            raise falcon.HTTPInternalServerError(
                'Internal server error',
                'Please use falconraml.JsonTranslator to parse json body.'
            )

        if type(raml_json_body_schema) is not dict:
            raise falcon.HTTPInternalServerError(
                'Internal server error',
                'Failed to parse jsonschema.'
            )

        request_json_body = request.context['json']

        try:
            jsonschema.validate(request_json_body, raml_json_body_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise falcon.HTTPBadRequest('Bad request body', e.message)

    def check_value_with_raml_type(self, raml_spec, string, exception):
        """Check a string value with a RAML type.

        The listed types are from:
        https://github.com/raml-org/raml-spec/blob/master/versions/raml-08/raml-08.md#type
        """
        if raml_spec.type == 'string':
            # No need to check anything
            pass
        elif raml_spec.type == 'number':
            if not self._can_parse_as_python_type(float, string):
                raise exception('Should be a number.', raml_spec.name)
        elif raml_spec.type == 'integer':
            if not self._can_parse_as_python_type(int, string):
                raise exception('Should be an integer.', raml_spec.name)
        elif raml_spec.type == 'date':
            # Not supported yet
            pass
        elif raml_spec.type == 'boolean':
            if string not in ('true', 'false'):
                raise exception('Should be "true" or "false".', raml_spec.name)
        elif raml_spec.type == 'file':
            # Not supported yet
            pass

    def _can_parse_as_python_type(self, python_type, string):
        """Check if a string can be converted to a python type.

        Currently supports float and int.
        """
        try:
            python_type(string)
            return True
        except ValueError:
            return False

    def _make_form_param(self, param_tuple):
        """Make a FormParameter from a parameter tuple.

        This is a workaround for weird ramlfications parsing:
        https://github.com/spotify/ramlfications/issues/122
        """
        param_name = param_tuple[0]
        param_config = param_tuple[1]

        form_param = ramlfications.parameters.FormParameter(
            param_name,
            {},
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {},
            [],
        )

        if 'required' in param_config:
            form_param.required = param_config['required']
        if 'type' in param_config:
            form_param.type = param_config['type']

        return form_param
