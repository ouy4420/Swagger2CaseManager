import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SwaggerToCase.DB_operation.models import Project, TestCase, Config, StepCase, API, Validate, Extract, Parameters, Variables

engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8",
                       encoding='utf-8',
                       # echo=True,
                       max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()


class CURD(object):
    def __init__(self):
        pass

    # 适合新的测试用例的create（ TODO ：需要，models中新增config的variable表，CURD支持Variable的CURD）
    # 然后在这个基础上修改（如：parameters、variables、name等等）
    # 也适合流程场景测试testcase的create
    # 新增testcase, 把teststep1对应的初始testcase查询出来
    # 然后在这个testcase基础上进行修改
    def create(self, old_case_id, case_name):
        old_case_obj = session.query(TestCase).filter(TestCase.id == old_case_id)
        new_case_obj = TestCase(name=case_name, project_id=old_case_obj.project_id)
        session.add(new_case_obj)
        session.commit()

        old_config_obj = session.query(Config).filter(Config.testcase_id == old_case_id).join(TestCase).first()
        name = old_config_obj.name  # ToDo 支持config name 的update（其实这个就是testcasename，测试用例描述）
        body = old_config_obj.body
        config_obj = Config(name=name, body=body, testcase_id=new_case_obj.id)
        session.add(config_obj)
        session.commit()

        old_teststeps_obj = session.query(StepCase).filter(StepCase.testcase_id == old_case_id).join(TestCase).all()
        for old_step_obj in old_teststeps_obj:
            name = old_step_obj.name
            api_name = old_step_obj.api_name
            body = old_step_obj.body
            step_obj = StepCase(name=name, step=1, api_name=api_name, body=body, testcase_id=new_case_obj.id)
            session.add(step_obj)
            session.commit()

    def delete(self, case_id):
        session.query(TestCase).filter_by(id=case_id).delete()

    # 下面对config的update和对teststep的update就是对testcase的update
    def update(self):
        pass

    # update config
    def add_parameter(self, config_id, parameter):
        key = parameter['key']
        value = parameter["value"]
        parameter_obj = Parameters(key=key,
                                   value=value,
                                   config_id=config_id)
        session.add(parameter_obj)
        session.commit()

    def update_parameter(self, config_id, parameter):
        key = parameter['key']
        value = parameter["value"]
        parameter_obj = session.query(Parameters).filter(Parameters.id == config_id)
        parameter_obj.key = key
        parameter_obj.value = value
        session.add(parameter_obj)
        session.commit()

    def delete_parameter(self, parameter_id):
        session.query(Parameters).filter_by(id=parameter_id).delete()

    def add_step(self, case_id, test_step, step_pos):
        name = test_step["name"]
        step = step_pos
        api_name = test_step["api"]
        body = json.dumps({"test": test_step})
        testcase_id = case_id
        step_obj = StepCase(name=name,
                            step=step,
                            api_name=api_name,
                            body=body,
                            testcase_id=testcase_id)
        session.add(step_obj)
        session.commit()

    def delete_step(self, step_id):
        session.query(StepCase).filter_by(id=step_id).delete()

    # update_step:
    #              add_validate、update_validate、delete_validate
    #              add_extract、update_extract、delete_extract
    def add_validate(self, step_id, validate):
        comparator = validate['comparator']
        check = validate["check"]
        expected = validate["expected"]
        validate_obj = Validate(comparator=comparator,
                                check=check,
                                expected=expected,
                                stepcase_id=step_id)
        session.add(validate_obj)
        session.commit()

    def update_validate(self, validate_id, validate):
        comparator = validate['comparator']
        check = validate["check"]
        expected = validate["expected"]
        validate_obj = session.query(Validate).filter(Validate.id == validate_id)
        validate_obj.comparator = comparator
        validate_obj.check = check
        validate_obj.expected = expected
        session.add(validate_obj)
        session.commit()

    def delete_validate(self, validate_id):
        session.query(Validate).filter_by(id=validate_id).delete()

    def add_extract(self, step_id, extract):
        key = extract['key']
        value = extract["value"]
        extract_obj = Extract(key=key,
                              value=value,
                              stepcase_id=step_id)
        session.add(extract_obj)
        session.commit()

    def update_extract(self, step_id, extract):
        key = extract['key']
        value = extract["value"]
        extract_obj = session.query(Extract).filter(Extract.id == step_id)
        extract_obj.key = key
        extract_obj.value = value
        session.add(extract_obj)
        session.commit()

    def delete_extract(self, extract_id):
        session.query(Extract).filter_by(id=extract_id).delete()

    # TODO：待拆分
    def retrieve(self, pro_name, case_ids):
        '''
        从数据库中查询并组装好某个project中某些测试用例用于测试执行
        :param pro_name:
        :param case_ids:
        :return:
        '''
        project_obj = session.query(Project).filter(Project.name == pro_name).first()
        testcases_obj = session.query(TestCase).filter(TestCase.project_id == project_obj.id).join(Project).all()
        test_cases = [case for case in testcases_obj if case.id in case_ids]
        testcases = []  # 要执行的测试用例
        testapis = []  # 测试用例执行相关的api
        for case_obj in test_cases:
            case_name = case_obj.name
            test_case = []  # testcase, include config and teststeps
            print("case : ", case_obj)

            # ----------------------------测试用例的config数据 ----------------------------
            config_obj = session.query(Config).filter(Config.testcase_id == case_obj.id).join(TestCase).first()
            print("config: ", config_obj)
            case_config = json.loads(config_obj.body)

            # parameters of config
            parameters_obj = session.query(Parameters). \
                filter(Parameters.config_id == config_obj.id).join(Config, isouter=True).all()
            print("parameters: ", parameters_obj)
            parameter_list = []
            for item in parameters_obj:
                element = {item.key: item.value}
                parameter_list.append(element)
            case_config["config"].update({"parameters": parameter_list})

            # variables of config
            variables_obj = session.query(Variables). \
                filter(Variables.config_id == config_obj.id).join(Config, isouter=True).all()
            print("parameters: ", variables_obj)
            variable_list = []
            for item in variables_obj:
                element = {item.key: json.loads(item.value)}
                variable_list.append(element)
            case_config["config"].update({"variables": variable_list})

            test_case.append(case_config)

            # ----------------------------测试用例的teststeps数据 ----------------------------
            teststeps_obj = session.query(StepCase).filter(StepCase.testcase_id == case_obj.id).join(TestCase).all()
            print(type(teststeps_obj), teststeps_obj)
            case_steps = []  # teststeps
            teststeps_obj = sorted(teststeps_obj, key=lambda x: x.step)
            for step_obj in teststeps_obj:
                print("step: ", step_obj)

                step = json.loads(step_obj.body)  # teststep的主体信息

                # testcase corresponding api
                api_obj = session.query(API).filter(API.stepcase_id == step_obj.id).join(StepCase, isouter=True).first()
                if api_obj is not None:
                    print("api: ", api_obj)
                    api = json.loads(api_obj.body)  # api的主体信息
                    testapis.append(api)
                else:
                    name = step_obj.name
                    names = [i["api"]["name"] for i in testapis]
                    if name not in names:
                        api_obj = session.query(API).filter(API.name == name).first()
                        api = json.loads(api_obj.body)  # api的主体信息
                        testapis.append(api)

                # validate of teststep
                validates_obj = session.query(Validate).filter(Validate.stepcase_id == step_obj.id).join(StepCase,
                                                                                                         isouter=True).all()
                # if validates_obj is not None:
                print("validates: ", validates_obj)
                validate_list = []
                for item in validates_obj:
                    comparator = item.comparator
                    check = item.check
                    expected = item.expected
                    if expected in ["200", "404", "500", "401"]:
                        expected = int(expected)
                    element = {comparator: [check, expected]}
                    validate_list.append(element)
                step["test"].update({"validate": validate_list})  # teststep中的validate可能会add\update\delete，所以要update

                # validate of teststep
                extracts_obj = session.query(Extract). \
                    filter(Extract.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                print("extracts: ", extracts_obj)
                extract_list = []
                for item in extracts_obj:
                    element = {item.key: item.value}
                    extract_list.append(element)
                step["test"].update({"extract": extract_list})  # teststep中的extract可能会add\update\delete，所以要update

                case_steps.append(step)

            test_case = test_case + case_steps
            testcases.append((case_name, test_case))

        return testapis, testcases
