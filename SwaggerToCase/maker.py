import logging
import sys
import urllib.parse as urlparse
import json


class MakeAPI(object):
    def __init__(self):
        self.test_api = {"request": {}}

    @staticmethod
    def parse_value_from_type(value):
        if value.lower() == "false":
            return False
        elif value.lower() == "true":
            return True
        else:
            return str(value)

    # name
    def make_request_name(self, request_json):
        # TODO : try 机制
        self.test_api["name"] = request_json['operationId']

    # request -> method
    def make_request_mothod(self, method):
        method = method.upper()
        list_method = ["POST", "GET", "PUT", "DELETE", "PATCH", "OPTIONS"]
        if method is None:
            logging.exception("method missed in request.")
            sys.exit(1)
        if method not in list_method:
            logging.exception("method is not correct.")
            sys.exit(1)
        self.test_api["request"]["method"] = method

    # request -> url
    def make_request_url(self, url):
        parsed_object = urlparse.urlparse(url)
        self.test_api["request"]["url"] = parsed_object.geturl()
        return

    def parse_path_url(self, params):
        # 多个{}的情况也需要考虑， 写个通用的(已完成！)
        url = self.test_api["request"]["url"]
        path_params = params.path_param
        if "{" in url:
            path_dict = {}
            [path_dict.update(item) for item in path_params]
            url = url.format(**path_dict)
            self.test_api["request"]["url"] = url

            # request -> querystring

    # request -> params
    def make_request_query(self, params):
        # Todo: 补充url的querystring(已完成！)
        query_pramas = params.query_param
        query_dict = {}
        [query_dict.update(item) for item in query_pramas]
        self.test_api["request"]["params"] = query_dict

    # request -> headers
    def make_request_header(self, request_json):
        # ToDo： 通过consoums 获取content-type(已完成！)
        headers = {}
        headers_data = request_json.get("consumes", [])
        # 添加content-type字段
        if headers_data:
            headers["content-type"] = ";".join(headers_data)
            self.test_api["request"]["headers"] = headers

    def add_header_from_parameters(self, params):
        # 添加parameters中的其它header字段
        headers = self.test_api["request"]["headers"]
        query_pramas = params.query_param
        [headers.update(item) for item in query_pramas]

    # request -> data
    def make_request_body(self, request_json, params):
        try:
            body_params = params.body_param
            formdata_params = params.formdata_param
            if body_params:
                data = json.dumps(body_params[0])
                self.test_api["request"]["data"] = data
            else:
                # ToDo: 待解决！！
                # ToDo: parameter 是formdata时，要对应设置Header
                # if form_urlencoded:
                #     test_api["request"]["headers"].update({"Content-Type": "application/x-www-form-urlencoded"})
                # elif multipart:
                #     test_api["request"]["headers"].update({"Content-Type": "multipart/form-data"})
                # data = formdata_params[0]
                pass
        except Exception as e:
            logging.exception(e)
            sys.exit(1)

    # validate
    def make_response_schema_validate(self, test_api):
        # parse_responses
        # test_api['validate'] =
        pass


