from functools import lru_cache
import pprint

import falcon
import json
import logging

from falsy.swagger_proxy.operator_loader import OperatorLoader
from falsy.swagger_proxy.spec_loader import SpecLoader

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def default_error_handler(req, resp, e):
    resp.body = json.dumps({'error': str(e)})
    resp.status = falcon.HTTP_500
    resp.content_type = 'application/json'


def http_not_found_handler(req, resp, e):
    resp.body = e.title
    resp.status = e.status
    resp.content_type = 'application/json'


def http_missing_param_handler(req, resp, e):
    resp.body = json.dumps({'error': e.title + ':' + ' '.join([p for p in e.args])})
    resp.status = e.status
    resp.content_type = 'application/json'


def http_invalid_param_handler(req, resp, e):
    resp.body = json.dumps({'error': e.title + ':' + ' '.join([p for p in e.args])})
    resp.status = e.status
    resp.content_type = 'application/json'


class SwaggerServer:
    def __init__(self, errors=None):
        self.default_content_type = 'application/json'
        self.specs = {}  # Meta()
        self.custom_error_map = errors
        self.op_loader = OperatorLoader()

    def __call__(self, req, resp):  # , **kwargs):
        # log.info(dir(req))
        log.info(req.remote_addr)
        # self.req = req
        # self.resp = resp
        self.process(req, resp)

    def load_specs(self, swagger_spec):
        self.specs = SpecLoader().load_specs(swagger_spec)
        self.basePath = self.specs['basePath']

    def process(self, req, resp):
        if req.method == 'OPTIONS':
            self.process_preflight_request(req, resp)
            return
        try:
            self.dispatch(req, resp)
        except Exception as e:
            error_type = type(e)
            error_map = {
                falcon.errors.HTTPNotFound: http_not_found_handler,
                falcon.errors.HTTPMissingParam: http_missing_param_handler,
                falcon.errors.HTTPInvalidParam: http_invalid_param_handler,
            }
            if self.custom_error_map:
                error_map.update(self.custom_error_map)

            error_func = error_map.get(error_type)
            if error_func:
                error_func(req, resp, e)
            else:
                default_error_handler(req, resp, e)

    def process_preflight_request(self, req, resp):
        log.info("Got an OPTIONS request: ".format(req.relative_uri))
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        resp.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        resp.set_header('Access-Control-Allow-Headers',
                        'Authorization, X-Auth-Token, Keep-Alive, Users-Agent, X-Requested-With, If-Modified-Since, Cache-Control, Content-Type')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days

        response_body = '\n'

        response_body += 'All Swagger operations:\n\n'
        response_body += 'nothing here\n\n'

        resp.body = response_body
        resp.status = falcon.HTTP_200

    def dispatch(self, req, resp):
        base_before, base_after, base_excp = self.op_loader.load_base(self.specs)
        try:
            if base_before:
                base_before(req=req, resp=resp)
            for uri_regex, spec in self.specs.items():
                try:
                    route_signature = '/' + req.method.lower() + req.relative_uri
                    if route_signature.find('?') > 0:
                        route_signature = route_signature[:route_signature.find('?')]
                    if type(uri_regex) == str:
                        continue
                    match = uri_regex.match(route_signature)
                    if match:
                        handler, params, before, after, excp, mode = self.op_loader.load(req=req, spec=spec,
                                                                                         matched_uri=match)
                        handler_return = None
                        try:
                            if before:
                                before(req=req, resp=resp, **params)

                            if mode == 'raw':
                                handler_return = handler(req=req, resp=resp)
                            else:
                                if mode == 'more':
                                    handler_return = handler(req=req, resp=resp, **params)
                                else:
                                    handler_return = handler(**params)
                                self.process_response(req, resp, handler_return)

                            if after:
                                after(req=req, resp=resp, response=handler_return, **params)
                        except Exception as e:
                            if excp is None:
                                raise e
                            if excp is not None:
                                excp(req=req, resp=resp, error=e)
                        return
                except AttributeError as e:
                    print(e, 'catched')
            if base_after:
                base_after(req=req, resp=resp)
        except Exception as e:
            if base_excp is None:
                raise e
            if base_excp is not None:
                base_excp(req=req, resp=resp, error=e)
        log.info("Request URL does not match any route signature: {}".format(route_signature))
        raise falcon.HTTPNotFound()

    def process_response(self, req, resp, handler_return):
        content_type = 'text/plain'
        if handler_return is None:
            return
        if type(handler_return) == tuple:
            data = handler_return[0]
            http_code = handler_return[1]
            if len(handler_return) > 2:
                content_type = handler_return[2]
            else:
                if type(data) == dict or type(data) == list:
                    content_type = 'application/json'
        else:
            data = handler_return
            http_code = falcon.HTTP_200
            if type(data) == dict or type(data) == list:
                content_type = 'application/json'
        if resp.body:
            try:
                pre_body = json.loads(resp.body)
            except Exception as e:
                pre_body = resp.body
            if type(pre_body) == dict:
                if 'json' in content_type:
                    pre_body.update(data)
                    resp.body = json.dumps(pre_body, indent=2)
                else:
                    resp.body = json.dumps(pre_body) + data
            else:
                resp.body = pre_body + json.dumps(data, indent=2) if 'json' in content_type else json.dumps(
                    pre_body) + data
        else:
            resp.body = json.dumps(data, indent=2) if 'json' in content_type else data
        resp.content_type = content_type
        resp.status = http_code
