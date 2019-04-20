import json
import yaml
import logging
import sys
import urllib.parse as urlparse
import re
from collections import OrderedDict
from SwaggerToCase import utils
from SwaggerToCase.encoder import JSONEncoder
from SwaggerToCase.parse import ParsePostData
import datetime
import os

class SwaggerParser(object):
    def __init__(self, file_path=None, filter_str=None, exclude_str=None):
        self.item = utils.load_item(file_path)
        # self.item = utils.load_item(file_path)
        self.user_agent = None
        self.filter_str = filter_str
        self.exclude_str = exclude_str or ""
        self.ordered_dict = False
        self.parse_post_data = ParsePostData()

    def init_dict(self):
        return OrderedDict() if self.ordered_dict else {}

    @staticmethod
    def parse_value_from_type(value):
        if value.lower() == "false":
            return False
        elif value.lower() == "true":
            return True
        else:
            return str(value)

    @staticmethod
    def _make_request_name(testcase_dic, request_json):
        # TODO : try 机制
        testcase_dic["name"] = request_json['operationId']

    def _make_request_body(self, testcase_dic, request_json):
        try:
            body = {}
            parameters = request_json.get("parameters")
            for param in parameters:
                if param["in"] == 'body':
                    body["required"] = param.get("required", None)
                    body["schema"] = param.get("schema", None)
                    if body["required"]:
                        if body["schema"]:
                            schema = body["schema"]['$ref']
                            ref = schema.split('/')[-1]
                            definitons = self.item["definitions"]
                            body_format = definitons[ref]['properties']
                            # ToDo
                            raw_data = {'language': 'c++', 'id': 0}
                            raw_data_json = json.dumps(raw_data)
                            testcase_dic["request"]["data"] = raw_data_json

            # if body_content is None:
            #     return
            # mode = body_content.get("mode")
            # post_data = body_content.get(mode)
            # if not len(post_data): return
            # data_parse_type = {
            #     "raw": self.parse_post_data.parse_raw_type,
            #     "urlencoded": self.parse_post_data.parse_urlencoded_type,
            #     "formdata": self.parse_post_data.parse_formdata_type,
            #     "file": self.parse_post_data.parse_file_type,
            # }
            # data_parse_type[mode](testcase_dic, post_data)
        except Exception as e:
            logging.exception("can't convert postman file to json file.")
            sys.exit(1)

    def _make_request_url(self, testcase_dic, url):
        if isinstance(url, str):
            parsed_object = urlparse.urlparse(url)
            testcase_dic["request"]["url"] = parsed_object.geturl()
            return
        elif isinstance(url, dict):
            url_dict = url
            url_keys = url_dict.keys()
            if "raw" in url_keys:
                url = url_dict["raw"]
                parsed_object = urlparse.urlparse(url)
                url = parsed_object.geturl()
                url = url.split("?")[0]
                if url.startswith("{{"):
                    url = re.sub(r"{{\w+}}", "", url, count=1)

                testcase_dic["request"]["url"] = url
            params = {}
            if "query" in url_keys:
                for query in url_dict.get("query"):
                    params[query["key"]] = self.parse_value_from_type(query["value"])  # value可能是什么类型?
            if len(params):
                testcase_dic["request"]["params"] = params
            return

    @staticmethod
    def _make_request_mothod(testcase_dic, method):
        method = method.upper()
        list_method = ["POST", "GET", "PUT", "DELETE", "PATCH", "OPTIONS"]
        if method is None:
            logging.exception("method missed in request.")
            sys.exit(1)
        if method not in list_method:
            logging.exception("method is not correct.")
            sys.exit(1)
        testcase_dic["request"]["method"] = method

    @staticmethod
    def _make_request_header(testcase_dic, request_json):
        headers = {}
        headers_data = request_json.get("consumes", [])
        if headers_data:
            headers["content-type"] = ";".join(headers_data)
            testcase_dic["request"]["headers"] = headers

    def make_testapi(self, url, api_item):
        testcase_dic = self.init_dict()  # OrderedDict没起作用？

        testcase_dic["request"] = {}
        method = api_item[0]
        request_data = api_item[1]
        self._make_request_name(testcase_dic, request_data)
        self._make_request_url(testcase_dic, url)
        self._make_request_mothod(testcase_dic, method)
        self._make_request_header(testcase_dic, request_data)
        self._make_request_body(testcase_dic, request_data)
        return testcase_dic

    def make_testapis(self):
        def is_exclude(url, exclude_str):
            exclude_str_list = exclude_str.split("|")
            for exclude_str in exclude_str_list:
                if exclude_str and exclude_str in url:
                    return True

            return False

        test_apis = []
        # TODO 先写死一个URL的restful,后面再扩展到多个URL
        url = '/language'
        api_items = self.item["paths"][url]
        for api_item in api_items.items():
            # TODO: host of swagger file

            # url = entry_json["request"].get("url")
            # if self.filter_str and self.filter_str not in url:
            #     continue
            #
            # if is_exclude(url, self.exclude_str):
            #     continue

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
    s2case = SwaggerParser()
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



