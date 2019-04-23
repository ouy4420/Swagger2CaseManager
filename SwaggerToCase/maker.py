import logging
import sys
import urllib.parse as urlparse


class MakeAPI(object):
    def __init__(self):
        self.test_api = {}

    # name
    def _make_request_name(self, operationId):
        # TODO : try 机制
        self.test_api["name"] = operationId

    # request -> method
    def _make_request_mothod(self, method):
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
    def _make_request_url(self, url):
        parsed_object = urlparse.urlparse(url)
        self.test_api["request"]["url"] = parsed_object.geturl()
        return

    def _parse_path_url(self, params):
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
    def _make_request_query(self, params):
        # Todo: 补充url的querystring(已完成！)
        query_pramas = params.query_param
        query_dict = {}
        [query_dict.update(item) for item in query_pramas]
        self.test_api["request"]["params"] = query_dict

    # request -> headers
    def _make_request_header(self, consumes):
        headers = {}
        # 添加content-type字段
        if consumes:
            headers["content-type"] = ";".join(consumes)
            self.test_api["request"]["headers"] = headers

    def _add_header_from_parameters(self, params):
        # 添加parameters中的其它header字段
        headers = self.test_api["request"]["headers"]
        query_pramas = params.query_param
        [headers.update(item) for item in query_pramas]

    # request -> data
    def _make_request_body(self, params):
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
    def _make_response_schema_validate(self, test_api):
        # parse_responses
        # test_api['validate'] =
        pass

    def _make_def_name(self):
        api_name = self.test_api["name"]
        data = self.test_api["request"].get('json', None)
        if data is not None:
            def_name = "{}({})".format(api_name, "$data")
        else:
            def_name = "{}()".format(api_name)
        self.test_api["def"] = def_name

    def _make_testapi(self, interface):
        # -----获取解析后的参数---
        method = interface["method"]
        url = interface["url"]
        consumes = interface["consumes"]
        operationId = interface["operationId"]
        parameters = interface["parameters"]

        self.test_api = {"request": {}}
        # -----Make API-----------
        self._make_request_name(operationId)
        self._make_request_mothod(method)
        self._make_request_url(url)
        self._make_request_header(consumes)
        # 有时get方法没有parameters参数
        if parameters is not None:
            self._parse_path_url(parameters)
            self._make_request_query(parameters)
            self._make_request_body(parameters)
        self._make_def_name()
        return self.test_api

    def make_testapis(self, apis, interfaces):
        for interface in interfaces:
            apis.append(
                {"api": self._make_testapi(interface)}
            )


class MakeTestcase(object):
    def __init__(self):
        self.test_case = []

    def _make_config(self, name):
        config = {
            "config": {
                "name": name,
                "request": {
                    "base_url": "$base_url",
                    "headers": {
                        "Content-Type": "application/json;charset=UTF-8"
                    }
                }
            }
        }
        self.test_case.append(config)

    def _make_request_variable(self, body_data):
        if body_data is not None:
            config = self.test_case[0]["config"]
            config.update({"variables": {"data": body_data}})

    def _make_response_variable(self, responses):
        # self.responses
        pass

    def _make_teststep(self, name, def_name):
        teststep = {
            "test": {
                "name": name,
                "api": def_name
            }
        }
        self.test_case.append(teststep)

    def _make_validate(self):
        validate = {"validate": []}
        validate_list = validate["validate"]
        eq = {"eq": ["status_code", 200]}
        validate_list.append(eq)
        # validate_schema = {"validate_schema": ["content", "$schema"]}
        # validate_list.append(validate_schema)
        teststep = self.test_case[1]["test"]
        teststep.update(validate)

    def _make_testcase(self, test_api, interface):
        self.test_case = []
        responses = interface["responses"]
        def_name = test_api["api"]["def"]
        name = def_name.split("(")[0]
        body_data = test_api["api"]["request"].get("json", None)
        if body_data is not None:
            test_api["api"]["request"]['json'] = '$data'
        self._make_config(name)
        self._make_request_variable(body_data)
        self._make_response_variable(responses)
        self._make_teststep(name, def_name)
        self._make_validate()
        return name, self.test_case

    def make_testcases(self, apis, testcases, interfaces):
        for test_api, interface in zip(apis, interfaces):
            testcases.append(self._make_testcase(test_api, interface))


