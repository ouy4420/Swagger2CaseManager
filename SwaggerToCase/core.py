from SwaggerToCase import loader
from SwaggerToCase.encoder import JSONEncoder
from SwaggerToCase.parser import ParseParameters
from SwaggerToCase.maker import MakeAPI
import json
import yaml
import logging
import os
import shutil


class SwaggerParser(object):
    def __init__(self, file_or_url=None):
        self.file_or_url = file_or_url
        self.item = None
        self.definitoins = None
        self.apis = []
        self.testcases = []

    def execute(self, testcase_dir, api_file, file_type):
        # 加载swagger文件
        self.load()  # 指出url和file两种方式
        # 解析文件数据
        self.parse()
        # 组装api合testcase数据
        self.make()
        # 将api和testcase写入文件
        self.write_file(testcase_dir, api_file, file_type)

    def load(self):
        if self.file_or_url.startswith("http"):
            self.item = loader.load_by_url(self.file_or_url)
        else:
            self.item = loader.load_by_file(self.file_or_url)

    def parse(self):
        # TODO: host of swagger file
        self.definitoins = self.item.get("definitions", None)

    def make(self):
        self.apis = self.make_testapis()
        for api in self.apis:
            def_name, api_item = self.add_def_name(api)
            body_data = api_item["api"]["request"].get("json", None)
            name_case = self.make_testcase(def_name, body_data)
            self.testcases.append(name_case)
            if body_data is not None:
                api_item["api"]["request"]['json'] = '$data'

    def write_file(self, testcase_dir, api_file, file_type):
        # -------写入api文件---------
        if file_type == "yml":
            logging.debug("Start to generate YAML apis.")
            with open(api_file, 'w', encoding="utf-8") as outfile:
                yaml.dump(self.apis, outfile, allow_unicode=True, default_flow_style=False, indent=4)
            logging.debug("Generate YAML api_file successfully: {}".format(api_file))
        else:
            logging.debug("Start to generate JSON apis.")
            with open(api_file, 'w', encoding="utf-8") as outfile:
                my_json_str = json.dumps(self.apis, ensure_ascii=False, indent=4, cls=JSONEncoder, sort_keys=True)
                if isinstance(my_json_str, bytes):
                    my_json_str = my_json_str.decode("utf-8")
                outfile.write(my_json_str)
            logging.debug("Generate JSON api_file successfully: {}".format(api_file))

        # --------写入testcase文件--------
        if not os.path.exists(testcase_dir):
            os.mkdir(testcase_dir)
        else:
            shutil.rmtree(testcase_dir)
            os.mkdir(testcase_dir)

        for name, case in self.testcases:
            case_path = os.path.join(testcase_dir, '{}.{}'.format(name, file_type))
            # 将对象先转换成json字符串，进行strip去除一些杂质字符，再转回obj
            case_json = json.dumps(case)
            case_json = case_json.strip()
            case = json.loads(case_json)
            if file_type == 'yml':
                logging.debug("Start to generate YAML testcases.")
                with open(case_path, 'w', encoding="utf-8") as outfile:
                    yaml.dump(case, outfile, allow_unicode=True, default_flow_style=False, indent=2)
                logging.debug("Generate YAML testcase successfully: {}".format(case_path))
            else:
                with open(case_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(case, ensure_ascii=False, indent=4, cls=JSONEncoder, sort_keys=True)
                    if isinstance(my_json_str, bytes):
                        my_json_str = my_json_str.decode("utf-8")
                    outfile.write(my_json_str)
                logging.debug("Generate JSON testcase successfully: {}".format(case_path))

    def make_testcase(self, def_name, body_data):
        name = def_name.split("(")[0]
        testcase = []
        # ToDo: 到时候，config中的name设置成description
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
        if body_data is not None:
            config["config"].update({"variables": {"data": body_data}})
        testcase.append(config)
        teststep = {
            "test": {
                "name": name,
                "api": def_name
            }
        }
        testcase.append(teststep)
        return name, testcase

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
        data = api_value["request"].get('json', None)
        if data is not None:
            def_name = "{}({})".format(api_name, "$data")
        else:
            def_name = "{}()".format(api_name)
        api_value["def"] = def_name
        api_item["api"] = api_value
        return def_name, api_item





