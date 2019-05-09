import json
import yaml
import logging
import os
import shutil
from SwaggerToCase.encoder import JSONEncoder
from sqlalchemy.orm import sessionmaker
from backend.models.models import Project, TestCase, Config, StepCase, API, Validate, Extract, Parameters, \
    VariablesLocal
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8",
                       encoding='utf-8',
                       # echo=True,
                       max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()


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

    def dump_to_file(self):
        self.dump_api_file()  # 写入api文件
        self.dump_testcases_files()  # 写入testcase文件


class DumpDB(object):
    def __init__(self, test_apis, test_cases):
        self.test_apis = test_apis
        self.test_cases = test_cases

    @staticmethod
    def insert_extract(step, step_obj):
        step_case = step["test"]
        extract = step_case.get("extract", None)
        if extract is not None:
            extract_list = extract
            for item in extract_list:
                key, value = tuple(item.items())[0]
                extract_obj = Extract(key=key, value=value, stepcase_id=step_obj.id)
                session.add(extract_obj)
                session.commit()

    @staticmethod
    def insert_validate(step, step_obj):
        validate_list = step["test"]["validate"]
        for item in validate_list:
            key, value = tuple(item.items())[0]
            comparator = key
            check = value[0]
            expected = value[1]
            if isinstance(expected, int):
                expected_type = "int"
            else:
                expected_type = "str"
            validate_obj = Validate(comparator=comparator,
                                    check=check,
                                    expected=expected,
                                    expected_type=expected_type,
                                    stepcase_id=step_obj.id)
            session.add(validate_obj)
            session.commit()

    def insert_api(self, project_obj):
        for api in self.test_apis:
            test_api = api["api"]
            api_func = test_api["def"]
            request = test_api["request"]
            url = request["url"]
            method = request["method"]
            body = json.dumps(api)
            api_obj = API(api_func=api_func, url=url, method=method, body=body, project_id=project_obj.id)
            session.add(api_obj)
            session.commit()

    @staticmethod
    def insert_stepcase(step, case_obj):
        step_case = step["test"]
        name = step_case["name"]
        api_name = step_case["api"]
        body = json.dumps(step)
        step_obj = StepCase(name=name, step=1, api_name=api_name, body=body, testcase_id=case_obj.id)
        session.add(step_obj)
        session.commit()
        return step_obj

    @staticmethod
    def insert_parameters(config, config_obj):
        config_field = config["config"]
        parameters = config_field.get("parameters")
        for item in parameters:
            key, value = tuple(item.items())[0]
            try:
                value = json.loads(value)
                value_type = "json_list"
            except Exception as e:
                value_type = "defined_func"
            parameter_obj = Parameters(key=key,
                                       value=value,
                                       value_type=value_type,
                                       config_id=config_obj.id)
            session.add(parameter_obj)
            session.commit()

    @staticmethod
    def insert_variables_local(step, case_obj):
        variables = step["test"]["variables"]
        for item in variables:
            key, value = tuple(item.items())[0]
            value = json.dumps(value)
            variable_obj = VariablesLocal(key=key, value=value, stepcase_id=case_obj.id)
            session.add(variable_obj)
            session.commit()

    @staticmethod
    def insert_config(config, case_obj):
        name = config["config"]["name"]
        body = json.dumps(config)
        config_obj = Config(name=name, body=body, testcase_id=case_obj.id)
        session.add(config_obj)
        session.commit()
        return config_obj

    @staticmethod
    def insert_testcase(case_name, project_obj):
        case_obj = TestCase(name=case_name, project_id=project_obj.id)
        session.add(case_obj)
        session.commit()
        return case_obj

    def insert_project(self, project):
        # insert into project
        name = project["name"]
        if project["url"]:
            mode = "url"
        else:
            mode = "file"
        desc = project["desc"]
        owner = project["owner"]
        project_obj = Project(name=name, mode=mode, desc=desc, owner=owner)
        session.add(project_obj)
        session.commit()

        # insert into testcase
        for case in self.test_cases:
            case_name, test_case = case
            case_obj = self.insert_testcase(case_name, project_obj)
            config = test_case[0]
            config_obj = self.insert_config(config, case_obj)
            # insert_parameters没什么意义，初始parameters为空列表
            self.insert_parameters(config, config_obj)
            for step in test_case[1:]:
                step_obj = self.insert_stepcase(step, case_obj)
                self.insert_variables_local(step, case_obj)
                self.insert_validate(step, step_obj)
                # insert_parameters没什么意义，初始extract为空列表
                self.insert_extract(step, step_obj)

        # insert into test_api
        self.insert_api(project_obj)

    def dump_to_db(self, config):
        project = config["project"]
        try:
            self.insert_project(project)
        except Exception as e:
            session.rollback()
            raise
