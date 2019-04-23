import logging
import sys
import urllib.parse as urlparse


class MakeAPI(object):
    def __init__(self):
        self.test_api = {"request": {}}

    # name
    def make_request_name(self, operationId):
        # TODO : try 机制
        self.test_api["name"] = operationId

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
    def make_request_header(self, consumes):
        headers = {}
        # 添加content-type字段
        if consumes:
            headers["content-type"] = ";".join(consumes)
            self.test_api["request"]["headers"] = headers

    def add_header_from_parameters(self, params):
        # 添加parameters中的其它header字段
        headers = self.test_api["request"]["headers"]
        query_pramas = params.query_param
        [headers.update(item) for item in query_pramas]

    # request -> data
    def make_request_body(self, params):
        try:
            body_params = params.body_param
            formdata_params = params.formdata_param
            if body_params:
                # data = json.dumps(body_params[0])
                data = body_params[0]
                self.test_api["request"]["json"] = data
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

    def make_def_name(self):
        api_name = self.test_api["name"]
        data = self.test_api["request"].get('json', None)
        if data is not None:
            def_name = "{}({})".format(api_name, "$data")
        else:
            def_name = "{}()".format(api_name)
        self.test_api["def"] = def_name


class MakeTestcase(object):
    def __init__(self, def_name, body_data, reponses):
        self.def_name = def_name
        self.name = self.def_name.split("(")[0]
        self.body_data = body_data
        self.responses = reponses
        self.body_data = {}
        self.test_case = []

    def make_config(self):
        config = {
            "config": {
                "name": self.name,
                "request": {
                    "base_url": "$base_url",
                    "headers": {
                        "Content-Type": "application/json;charset=UTF-8"
                    }
                }
            }
        }
        self.test_case.append(config)

    def make_config_variables(self):
        self.make_request_variable()

    def make_request_variable(self):
        if self.body_data is not None:
            config = self.test_case[0]["config"]
            config.update({"variables": {"data": self.body_data}})

    def make_response_variable(self):
        # self.responses
        pass

    def make_teststep(self):
        teststep = {
            "test": {
                "name": self.name,
                "api": self.def_name
            }
        }
        self.test_case.append(teststep)

    def make_validate(self):
        validate = {"validate": []}
        validate_list = validate["validate"]
        eq = {"eq": ["status_code", 200]}
        validate_list.append(eq)
        # validate_schema = {"validate_schema": ["content", "$schema"]}
        # validate_list.append(validate_schema)
        teststep = self.test_case[1]["test"]
        teststep.update(validate)

    def make_testcase(self):
        self.make_config()
        self.make_config_variables()
        self.make_teststep()
        self.make_validate()


