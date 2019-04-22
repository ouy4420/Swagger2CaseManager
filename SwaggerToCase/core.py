from SwaggerToCase import loader
from SwaggerToCase.encoder import JSONEncoder
from SwaggerToCase.parser import ParseParameters
from SwaggerToCase.maker import MakeAPI,MakeTestcase
import json
import yaml
import logging
import os
import shutil


class SwaggerParser(object):
    def __init__(self, config):
        self.file_or_url = config["file_or_url"]
        self.testcase_dir = config["testcase_dir"]
        self.api_file = config["api_file"]
        self.file_type = config["file_type"]
        self.item = {}
        self.paths = {}
        self.definitoins = {}
        self.apis = []
        self.testcases = []

    def execute(self):
        # 加载swagger文件
        self.load()  # 指出url和file两种方式
        # 解析文件数据
        self.parse()
        # 组装api合testcase数据
        self.make()
        # 将api和testcase写入文件
        self.write_file()

    def load(self):
        if self.file_or_url.startswith("http"):
            self.item = loader.load_by_url(self.file_or_url)
        else:
            self.item = loader.load_by_file(self.file_or_url)

    def parse(self):
        # TODO: host of swagger file
        self.paths = paths = self.item["paths"]
        self.definitoins = self.item.get("definitions", None)

    def make(self):
        self.make_testapis()
        self.make_testcases()

    def write_file(self):
        # -------写入api文件---------
        self.write_api_file()
        # --------写入testcase文件--------
        self.write_testcases_files()

    def write_api_file(self):
        if self.file_type == "YAML":
            api_file = os.path.join(self.api_file, '{}.{}'.format(self.api_file, 'yml'))
            logging.debug("Start to generate YAML apis.")
            with open(api_file, 'w', encoding="utf-8") as outfile:
                yaml.dump(self.apis, outfile, allow_unicode=True, default_flow_style=False, indent=4)
            logging.debug("Generate YAML api_file successfully: {}".format(self.api_file))
        else:
            api_file = os.path.join(self.api_file, '{}.{}'.format(self.api_file, 'json'))
            logging.debug("Start to generate JSON apis.")
            with open(api_file, 'w', encoding="utf-8") as outfile:
                my_json_str = json.dumps(self.apis, ensure_ascii=False, indent=4, cls=JSONEncoder, sort_keys=True)
                if isinstance(my_json_str, bytes):
                    my_json_str = my_json_str.decode("utf-8")
                outfile.write(my_json_str)
            logging.debug("Generate JSON api_file successfully: {}".format(self.api_file))

    def write_testcases_files(self):
        if not os.path.exists(self.testcase_dir):
            os.mkdir(self.testcase_dir)
        else:
            shutil.rmtree(self.testcase_dir)
            os.mkdir(self.testcase_dir)

        for name, case in self.testcases:
            # 将对象先转换成json字符串，进行strip去除一些杂质字符，再转回obj
            case_json = json.dumps(case)
            case_json = case_json.strip()
            case = json.loads(case_json)
            if self.file_type == 'YAML':
                case_path = os.path.join(self.testcase_dir, '{}.{}'.format(name, 'yml'))
                logging.debug("Start to generate YAML testcases.")
                with open(case_path, 'w', encoding="utf-8") as outfile:
                    yaml.dump(case, outfile, allow_unicode=True, default_flow_style=False, indent=2)
                logging.debug("Generate YAML testcase successfully: {}".format(case_path))
            else:
                case_path = os.path.join(self.testcase_dir, '{}.{}'.format(name, 'json'))
                with open(case_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(case, ensure_ascii=False, indent=4, cls=JSONEncoder, sort_keys=True)
                    if isinstance(my_json_str, bytes):
                        my_json_str = my_json_str.decode("utf-8")
                    outfile.write(my_json_str)
                logging.debug("Generate JSON testcase successfully: {}".format(case_path))

    def make_testcase(self, def_name, body_data):
        make_testcase = MakeTestcase(def_name, body_data)
        make_testcase.make_testcase()
        return make_testcase.name, make_testcase.testcase

    def make_testcases(self):
        for api in self.apis:
            def_name, api_item = self.add_def_name(api)
            body_data = api_item["api"]["request"].get("json", None)
            name_case = self.make_testcase(def_name, body_data)
            self.testcases.append(name_case)
            if body_data is not None:
                api_item["api"]["request"]['json'] = '$data'

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
        for url in self.paths:
            api_items = self.paths[url]
            for api_item in api_items.items():
                self.apis.append(
                    {"api": self.make_testapi(url, api_item)}
                )

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
