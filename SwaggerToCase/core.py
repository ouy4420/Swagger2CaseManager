import json
import yaml
import logging
import sys
import urllib.parse as urlparse
import re
from SwaggerToCase import utils
from SwaggerToCase.encoder import JSONEncoder
from SwaggerToCase.parse import ParseParameters
import datetime
import os


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


class SwaggerParser(object):
    def __init__(self, file_or_url=None, filter_str=None, exclude_str=None):
        if file_or_url.startswith("http"):
            self.item = utils.load_by_url(file_or_url)
        else:
            self.item = utils.load_by_file(file_or_url)
        # TODO: host of swagger file
        self.definitoins = self.item.get("definitions", None)

    def make_testapi(self, url, api_item):
        method = api_item[0]
        request_data = api_item[1]
        make_api = MakeAPI()
        make_api.make_request_url(url)
        make_api.make_request_header(request_data)
        make_api.make_request_name(request_data)
        make_api.make_request_mothod(method)
        # 有时get方法没有parameters参数
        if 'parameters' in request_data:
            params = ParseParameters(self.definitoins, request_data['parameters'])
            params.parse_parameters()
            make_api.parse_path_url(params)
            make_api.make_request_query(params)
            make_api.make_request_header(request_data)
            make_api.make_request_body(request_data, params)
        # self.make_response_schema_validate()
        return make_api.test_api

    def make_testapis(self):
        test_apis = []
        paths = self.item["paths"]
        for url in paths:
            api_items = paths[url]
            for api_item in api_items.items():
                test_apis.append(
                    {"api": self.make_testapi(url, api_item)}
                )

        return test_apis

    def add_def_name(self, api_item):
        api_value = api_item["api"]
        api_name = api_value["name"]
        text = json.dumps(api_item)
        variables = re.findall(r'{{(\w+)}}', text)
        variables = list(set(variables))
        for var in variables:
            for key, value in api_value.items():
                text = json.dumps(value)
                text = text.replace(r"{{%s}}" % var, "$" + var)
                value = json.loads(text)
                api_value[key] = value
        variables = map(lambda x: "$" + x, variables)
        variables = ', '.join(variables)
        def_name = "{}({})".format(api_name, variables)

        api_value["def"] = def_name
        api_item["api"] = api_value
        return api_item

    def gen_json(self, json_file):
        """ dump Swagger josn file to json testset
        """
        logging.debug("Start to generate JSON apis.")
        self.apis = self.make_testapis()
        apis = []
        for api in self.apis:
            apis.append(self.add_def_name(api))
        print(apis)
        api_names = [api['api']["name"] for api in apis]
        with open(json_file, 'w', encoding="utf-8") as outfile:
            my_json_str = json.dumps(apis, ensure_ascii=False, indent=4, cls=JSONEncoder, sort_keys=True)

            if isinstance(my_json_str, bytes):
                my_json_str = my_json_str.decode("utf-8")
            outfile.write(my_json_str)
        logging.debug("Generate JSON testset successfully: {}".format(json_file))
        return api_names

    def gen_yaml(self, yaml_file):
        """ dump item of Collection v2.1 josn file to yaml testset
       """
        logging.debug("Start to generate YAML spis.")
        self.apis = self.make_testapis()
        apis = []
        for api in self.apis:
            apis.append(self.add_def_name(api))
        api_names = [api['api']["name"] for api in apis]
        with open(yaml_file, 'w', encoding="utf-8") as outfile:
            yaml.dump(apis, outfile, allow_unicode=True, default_flow_style=False, indent=4)

        logging.debug("Generate YAML testset successfully: {}".format(yaml_file))
        return api_names


if __name__ == '__main__':
    cwd = os.getcwd()
    test_pro_path = os.path.join(cwd, 'TestProject')
    log_level = getattr(logging, 'debug'.upper())
    logging.basicConfig(level=log_level)
    # s2case = SwaggerParser('http://192.168.1.107:5000/swagger.json')
    s2case = SwaggerParser(r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\haha.json')
    apifilename = 'mytest' + datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    apifilepath = os.path.join(test_pro_path, 'api')
    # api_names = s2case.gen_json(r"{}\{}.json".format(apifilepath, apifilename))
    api_names = s2case.gen_yaml("{}\{}.yml".format(apifilepath, apifilename))
    from SwaggerToCase.myrun import run

    testcase_obj = [
        {
            "config": {
                "name": "xxx",
                "request": {
                    "base_url": "$base_url",
                    "headers": {
                        "Content-Type": "application/json;charset=UTF-8"
                    }
                }
            }
        }
    ]
    teststep = {
        "test": {
            "name": "post_language",
            "api": "post_language()"
        }
    }
    import copy

    for name in api_names:
        teststep = copy.deepcopy(teststep)
        teststep["test"]["name"] = name
        teststep["test"]["api"] = name + "()"
        testcase_obj.append(teststep)
    print(api_names)
    testcasename = apifilename
    testcase_json = json.dumps(testcase_obj)
    casesfilepath = os.path.join(test_pro_path, 'testcases')
    print(r'{}\{}.json'.format(casesfilepath, testcasename))
    # with open(r'{}\{}.json'.format(casesfilepath, testcasename), 'w') as f:
    #     f.write(testcase_json)
    with open(r'{}\{}.yml'.format(casesfilepath, testcasename), 'w', encoding="utf-8") as outfile:
        yaml.dump(testcase_obj, outfile, allow_unicode=True, default_flow_style=False, indent=4)
    run(test_pro_path, [testcasename + '.yml'])
    # run(test_pro_path, [testcasename + '.json'])
