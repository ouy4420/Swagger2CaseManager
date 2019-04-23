import json
import yaml
import logging
import os
import shutil
from SwaggerToCase.encoder import JSONEncoder


class DumpFile(object):
    def __init__(self, config, test_apis, test_cases):
        self.testcase_dir = config["testcase_dir"]
        self.api_file = config["api_file"]
        self.file_type = config["file_type"]
        self.test_apis = test_apis
        self.test_cases = test_cases

    def dump_api_file(self):
        if self.file_type == "YAML":
            api_file = os.path.join(self.api_file, '{}.{}'.format(self.api_file, 'yml'))
            logging.debug("Start to generate YAML apis.")
            with open(api_file, 'w', encoding="utf-8") as outfile:
                yaml.dump(self.test_apis, outfile, allow_unicode=True, default_flow_style=False, indent=4)
            logging.debug("Generate YAML api_file successfully: {}".format(self.api_file))
        else:
            api_file = os.path.join(self.api_file, '{}.{}'.format(self.api_file, 'json'))
            logging.debug("Start to generate JSON apis.")
            with open(api_file, 'w', encoding="utf-8") as outfile:
                my_json_str = json.dumps(self.test_apis, ensure_ascii=False, indent=4, cls=JSONEncoder, sort_keys=True)
                if isinstance(my_json_str, bytes):
                    my_json_str = my_json_str.decode("utf-8")
                outfile.write(my_json_str)
            logging.debug("Generate JSON api_file successfully: {}".format(self.api_file))

    def dump_testcases_files(self):
        if not os.path.exists(self.testcase_dir):
            os.mkdir(self.testcase_dir)
        else:
            shutil.rmtree(self.testcase_dir)
            os.mkdir(self.testcase_dir)

        for name, case in self.test_cases:
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
