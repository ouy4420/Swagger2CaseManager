from SwaggerToCase import loader
from SwaggerToCase.encoder import JSONEncoder
from SwaggerToCase.parser import ParseSwagger
from SwaggerToCase.maker import MakeAPI, MakeTestcase
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
        self.parsed_swagger = {}
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
        parsed_swagger = ParseSwagger(self.item)
        parsed_swagger.parse_swagger()
        self.parsed_swagger = parsed_swagger.swagger
        self.definitoins = self.parsed_swagger["definitions"]

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

    def make_testcase(self, test_api, interface):
        reponses = interface["responses"]
        def_name = test_api["api"]["def"]
        body_data = test_api["api"]["request"].get("json", None)
        if body_data is not None:
            test_api["api"]["request"]['json'] = '$data'
        make_case = MakeTestcase(def_name, body_data, reponses)
        make_case.make_testcase()
        return make_case.name, make_case.test_case

    def make_testcases(self):
        interfaces = self.parsed_swagger["interfaces"]
        for test_api, interface in zip(self.apis, interfaces):
            self.testcases.append(self.make_testcase(test_api, interface))

    def make_testapi(self, interface):
        # -----获取解析后的参数---
        method = interface["method"]
        url = interface["url"]
        consumes = interface["consumes"]
        operationId = interface["operationId"]
        parameters = interface["parameters"]

        # -----Make API-----------
        make_api = MakeAPI()
        make_api.make_request_name(operationId)
        make_api.make_request_mothod(method)
        make_api.make_request_url(url)
        make_api.make_request_header(consumes)
        # 有时get方法没有parameters参数
        if parameters is not None:
            make_api.parse_path_url(parameters)
            make_api.make_request_query(parameters)
            make_api.make_request_body(parameters)
        make_api.make_def_name()
        return make_api.test_api

    def make_testapis(self):
        interfaces = self.parsed_swagger["interfaces"]
        for interface in interfaces:
            self.apis.append(
                {"api": self.make_testapi(interface)}
            )




    # def add_def_name(self, api_item):
    #     api_value = api_item["api"]
    #     api_name = api_value["name"]
    #     data = api_value["request"].get('json', None)
    #     if data is not None:
    #         def_name = "{}({})".format(api_name, "$data")
    #     else:
    #         def_name = "{}()".format(api_name)
    #     api_value["def"] = def_name
    #     api_item["api"] = api_value
    #     return def_name, api_item