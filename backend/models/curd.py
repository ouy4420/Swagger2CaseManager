import json
from backend.models.models import Project, \
    TestCase, Config, StepCase, API, Validate, Extract, \
    Parameters, VariablesGlobal, Report, VariablesLocal, VariablesEnv, DebugTalk

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8",
                       encoding='utf-8',
                       # echo=True,
                       isolation_level='AUTOCOMMIT',  # 加上这句解决查询数据库不更新的情况
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
    def add_project(self, project):
        try:
            name = project['name']
            desc = project["desc"]
            owner = project["owner"]
            project_obj = Project(name=name,
                                  desc=desc,
                                  owner=owner,
                                  mode="common")
            session.add(project_obj)
            session.commit()
            return True, "Project创建成功！"
        except Exception as e:
            session.rollback()
            return False, "Project创建失败！" + str(e)

    def add_case(self, old_case_id, case_name):
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

    def add_report(self, report):
        try:
            report_obj = Report(name=report['name'],
                                current_time=report["current_time"],
                                render_content=report["render_content"],
                                tester=report["tester"],
                                description=report["description"],
                                project_id=report["project_id"])
            session.add(report_obj)
            session.commit()
            return True, "Report创建成功！"
        except Exception as e:
            print(e)
            session.rollback()
            return False, "Report创建失败！" + str(e)

    def add_variable_global(self, config_id, variable):
        try:
            # 注意：这里variable是字符串（传进来需要json转换）
            variable_obj = VariablesGlobal(key=variable['key'],
                                           value=variable["value"],
                                           config_id=config_id)
            session.add(variable_obj)
            session.commit()
            return True, "全局变量添加成功！"
        except Exception as e:
            session.rollback()
            return False, "全局变量添加失败！" + str(e)

    def add_variable_local(self, stepcase_id, variable):
        try:
            # 注意：这里variable是字符串（传进来需要json转换）
            variable_obj = VariablesLocal(key=variable['key'],
                                          value=variable["value"],
                                          stepcase_id=stepcase_id)
            session.add(variable_obj)
            session.commit()
            return True, "局部变量添加成功！"
        except Exception as e:
            session.rollback()
            return False, "局部变量添加失败！" + str(e)

    def add_variable_env(self, project_id, variable):
        try:
            # 注意：这里variable是字符串（传进来需要json转换）
            variable_obj = VariablesEnv(key=variable['key'],
                                        value=variable["value"],
                                        project_id=project_id)
            session.add(variable_obj)
            session.commit()
            return True, "环境变量添加成功！"
        except Exception as e:
            session.rollback()
            return False, "环境变量添加失败！" + str(e)

    def add_parameter(self, config_id, parameter):
        try:
            key = parameter['key']
            value = parameter["value"]
            parameter_obj = Parameters(key=key,
                                       value=value,
                                       config_id=config_id)
            session.add(parameter_obj)
            session.commit()
            return True, "Parameter添加成功!"
        except Exception as e:
            session.rollback()
            return False, "Parameter添加失败！" + str(e)

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

    def add_validate(self, step_id, validate):
        try:
            comparator = validate['comparator']
            check = validate["check"]
            expected = validate["expected"]
            expected_type = validate["expected_type"]
            validate_obj = Validate(comparator=comparator,
                                    check=check,
                                    expected=expected,
                                    expected_type=expected_type,
                                    stepcase_id=step_id)
            session.add(validate_obj)
            session.commit()
            return True, "Validate添加成功!"
        except Exception as e:
            session.rollback()
            return False, "Validate添加失败！" + str(e)

    def add_extract(self, step_id, extract):
        try:
            key = extract['key']
            value = extract["value"]
            extract_obj = Extract(key=key,
                                  value=value,
                                  stepcase_id=step_id)
            session.add(extract_obj)
            session.commit()
            return True, "Extract添加成功!"
        except Exception as e:
            session.rollback()
            return False, "Extract添加失败！" + str(e)

    def delete_project(self, project_id):
        try:
            testcases_obj = session.query(TestCase).filter(TestCase.project_id == project_id).join(Project).all()
            [self.delete_case(test_case.id) for test_case in testcases_obj]

            apis_obj = session.query(API).filter(API.project_id == project_id).join(Project).all()
            [self.delete_api(test_api.id) for test_api in apis_obj]

            envs_obj = session.query(VariablesEnv).filter(VariablesEnv.project_id == project_id).join(Project).all()
            [self.delete_variable_env(var_env.id) for var_env in envs_obj]

            reports_obj = session.query(Report).filter(Report.project_id == project_id).join(Project).all()
            [self.delete_report(test_report.id) for test_report in reports_obj]

            debugtalks_obj = session.query(DebugTalk).filter(DebugTalk.project_id == project_id).join(Project).all()
            [self.delete_debugtalk(debugtalk.id) for debugtalk in debugtalks_obj]

            session.query(Project).filter_by(id=project_id).delete()
            session.commit()
            return True, "Project删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Project删除失败！" + str(e)

    def delete_report(self, report_id):
        try:
            session.query(Report).filter_by(id=report_id).delete()
            session.commit()
            return True, "Report删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Report删除失败！" + str(e)

    def delete_debugtalk(self, debugtalk_id):
        try:
            session.query(DebugTalk).filter_by(id=debugtalk_id).delete()
            session.commit()
            return True, "DebugTalk删除成功！"
        except Exception as e:
            session.rollback()
            return False, "DebugTalk删除失败！" + str(e)

    def delete_case(self, case_id):
        # session.query(TestCase).filter_by(id=case_id).delete()  # 只是这样，删不了，因为有config和stepcase通过外键引用
        # 要想删除testcase, 先删除config和teststep
        # 同理，要想删除config，先删除parameters和variables
        # 要想删除teststep，先删除api(这个不合适)、validate和extract
        config_obj = session.query(Config).filter(Config.testcase_id == case_id).join(TestCase).first()
        config_id = config_obj.id
        self.delete_config(config_id)
        teststeps_obj = session.query(StepCase).filter(StepCase.testcase_id == case_id).join(TestCase).all()
        [self.delete_setp(teststep.id) for teststep in teststeps_obj]
        session.query(TestCase).filter_by(id=case_id).delete()
        session.commit()

    def delete_config(self, config_id):
        config_obj = session.query(Config).filter(Config.id == config_id).first()
        parameters_obj = session.query(Parameters). \
            filter(Parameters.config_id == config_obj.id).join(Config, isouter=True).all()
        [self.delete_parameter(parameter.id) for parameter in parameters_obj]
        variables_obj = session.query(VariablesGlobal). \
            filter(VariablesGlobal.config_id == config_obj.id).join(Config, isouter=True).all()
        [self.delete_variable_global(variable.id) for variable in variables_obj]
        session.query(Config).filter_by(id=config_id).delete()
        session.commit()

    def delete_parameter(self, parameter_id):
        try:
            session.query(Parameters).filter_by(id=parameter_id).delete()
            session.commit()
            return True, "Parameter删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Parameter删除成功！" + str(e)

    def delete_variable_global(self, variable_id):
        try:
            session.query(VariablesGlobal).filter_by(id=variable_id).delete()
            session.commit()
            return True, "全局变量删除成功！"
        except Exception as e:
            session.rollback()
            return False, "全局变量删除失败！" + str(e)

    def delete_variable_local(self, variable_id):
        try:
            session.query(VariablesLocal).filter_by(id=variable_id).delete()
            session.commit()
            return True, "局部变量删除成功！"
        except Exception as e:
            session.rollback()
            return False, "局部变量删除失败！" + str(e)

    def delete_variable_env(self, variable_id):
        try:
            session.query(VariablesEnv).filter_by(id=variable_id).delete()
            session.commit()
            return True, "环境变量删除成功！"
        except Exception as e:
            session.rollback()
            return False, "环境变量删除失败！" + str(e)

    def delete_setp(self, step_id):
        step_obj = session.query(StepCase).filter(StepCase.id == step_id).first()

        variables_obj = session.query(VariablesLocal). \
            filter(VariablesLocal.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
        [self.delete_variable_local(variable.id) for variable in variables_obj]

        validates_obj = session.query(Validate). \
            filter(Validate.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
        [self.delete_validate(validate.id) for validate in validates_obj]

        extracts_obj = session.query(Extract). \
            filter(Extract.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
        [self.delete_extract(extract.id) for extract in extracts_obj]

        session.query(StepCase).filter_by(id=step_id).delete()
        session.commit()

    def delete_validate(self, validate_id):
        try:
            session.query(Validate).filter_by(id=validate_id).delete()
            session.commit()
            return True, "Validate删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Validate删除失败！" + str(e)

    def delete_extract(self, extract_id):
        try:
            session.query(Extract).filter_by(id=extract_id).delete()
            session.commit()
            return True, "Extract删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Extract删除失败！" + str(e)

    def delete_api(self, api_id):
        session.query(API).filter_by(id=api_id).delete()
        session.commit()

    # update testcase:
    #       update config:
    #              add_parameter、update_parameter、delelte_parameter
    #              add_variable、update_variable、delelte_variable
    #       update teststep:
    #              add_validate、update_validate、delete_validate
    #              add_extract、update_extract、delete_extract
    def update_project(self, project_id, project):
        try:
            project_obj = session.query(Project).filter(Project.id == project_id).first()
            project_obj.name = project['name']
            project_obj.desc = project["desc"]
            session.add(project_obj)
            session.commit()
            return True, "Project更新成功！"
        except Exception as e:
            session.rollback()
            return False, "Project更新失败！" + str(e)

    def update_config(self, config):
        try:
            id = config['id']
            name = config['name']
            config_obj = session.query(Config).filter(Config.id == id).first()
            config_obj.name = name
            body = json.loads(config_obj.body)
            body["config"]["name"] = name
            config_obj.body = json.dumps(body)
            session.add(config_obj)
            session.commit()
            return True, "用例名称更新成功！"
        except Exception as e:
            session.rollback()
            return False, "用例名称更新失败！" + str(e)

    def update_report(self, report):
        try:
            id = report['id']
            description = report['description']
            report_obj = session.query(Report).filter(Report.id == id).first()
            report_obj.description = description
            session.add(report_obj)
            session.commit()
            return True, "报告更新成功！"
        except Exception as e:
            session.rollback()
            return False, "报告更新失败！" + str(e)

    def update_step(self, step):
        try:
            id = step['id']
            api_name = step['step_name']
            step_obj = session.query(StepCase).filter(StepCase.id == id).first()
            body = json.loads(step_obj.body)
            body["test"]["api"] = api_name
            step_obj.body = json.dumps(body)
            session.add(step_obj)
            session.commit()
            return True, "API调用名称更新成功！"
        except Exception as e:
            session.rollback()
            return False, "API调用名称更新失败！" + str(e)

    def update_parameter(self, parameter):
        try:
            id = parameter['id']
            key = parameter['key']
            value = parameter["value"]
            parameter_obj = session.query(Parameters).filter(Parameters.id == id).first()
            parameter_obj.key = key
            parameter_obj.value = value
            session.add(parameter_obj)
            session.commit()
            return True, "更新parameter成功！"
        except Exception as e:
            session.rollback()
            return False, "更新parameter失败！" + str(e)

    def update_variable_global(self, variable):
        try:
            variable_obj = session.query(VariablesGlobal).filter(VariablesGlobal.id == variable['id']).first()
            variable_obj.key = variable['key']
            variable_obj.value = variable["value"]
            session.add(variable_obj)
            session.commit()
            return True, "全局变量更新成功！"
        except Exception as e:
            session.rollback()
            return False, "全局变量更新失败" + str(e)

    def update_variable_local(self, variable):
        try:
            variable_obj = session.query(VariablesLocal).filter(VariablesLocal.id == variable['id']).first()
            variable_obj.key = variable['key']
            variable_obj.value = variable["value"]
            session.add(variable_obj)
            session.commit()
            return True, "局部变量更新成功！"
        except Exception as e:
            session.rollback()
            return False, "局部变量更新失败" + str(e)

    def update_variable_env(self, variable):
        try:
            variable_obj = session.query(VariablesEnv).filter(VariablesEnv.id == variable['id']).first()
            variable_obj.key = variable['key']
            variable_obj.value = variable["value"]
            session.add(variable_obj)
            session.commit()
            return True, "环境变量更新成功！"
        except Exception as e:
            session.rollback()
            return False, "环境变量更新失败" + str(e)

    def update_validate(self, validate):
        try:
            id = validate['id']
            comparator = validate['comparator']
            check = validate["check"]
            expected = validate["expected"]
            expected_type = validate["expected_type"]
            validate_obj = session.query(Validate).filter(Validate.id == id).first()
            validate_obj.comparator = comparator
            validate_obj.check = check
            validate_obj.expected = expected
            validate_obj.expected_type = expected_type
            session.add(validate_obj)
            session.commit()
            return True, "Validate更新成功！"
        except Exception as e:
            session.rollback()
            return False, "Validate更新失败" + str(e)

    def update_extract(self, extract):
        try:
            id = extract['id']
            key = extract['key']
            value = extract["value"]
            extract_obj = session.query(Extract).filter(Extract.id == id).first()
            extract_obj.key = key
            extract_obj.value = value
            session.add(extract_obj)
            session.commit()
            return True, "Extract更新成功！"
        except Exception as e:
            session.rollback()
            return False, "Extract更新失败" + str(e)

    def retrieve_parameter(self, parameter_id):
        '''
        配合parameter元素的update和delete
        先查出来，获取id，然后进行update或delete
        :param parameter_id:
        :return:
        '''
        parameter = session.query(Parameters).filter_by(id=parameter_id).first()
        element = {
            "id": parameter.id,
            "key": parameter.key,
            "value": parameter.value,
            "config_id": parameter.config_id
        }
        return element

    def retrieve_variable_global(self, variable_id):
        '''
        配合variable元素的update和delete
        :param variable_id:
        :return:
        '''
        variable = session.query(VariablesGlobal).filter_by(id=variable_id).first()
        element = {
            "id": variable.id,
            "key": variable.key,
            "value": json.loads(variable.value),
            "config_id": variable.config_id
        }
        return element

    def retrieve_variable_local(self, variable_id):
        '''
        配合variable元素的update和delete
        :param variable_id:
        :return:
        '''
        variable = session.query(VariablesLocal).filter_by(id=variable_id).first()
        element = {
            "id": variable.id,
            "key": variable.key,
            "value": json.loads(variable.value),
            "stepcase_id": variable.stepcase_id
        }
        return element

    def retrieve_variable_env(self, variable_id):
        '''
        配合variable元素的update和delete
        :param variable_id:
        :return:
        '''
        variable = session.query(VariablesEnv).filter_by(id=variable_id).first()
        element = {
            "id": variable.id,
            "key": variable.key,
            "value": json.loads(variable.value),
            "project_id": variable.project_id
        }
        return element

    def retrieve_validate(self, validate_id):
        '''
        配合parameter元素的update和delete
        :param validate_id:
        :return:
        '''
        validate = session.query(Validate).filter_by(id=validate_id).first()
        element = {
            "id": validate.id,
            "comparator": validate.comparator,
            "check": validate.check,
            "expected": validate.expected,
            "stepcase_id": validate.stepcase_id
        }
        return element

    def retrieve_extract(self, extract_id):
        '''
        配合parameter元素的update和delete
        :param extract_id:
        :return:
        '''
        extract = session.query(Extract).filter_by(id=extract_id).first()
        element = {
            "id": extract.id,
            "key": extract.key,
            "value": json.loads(extract.value),
            "stepcase_id": extract.stepcase_id
        }
        return element

    # TODO：待拆分
    def retrieve_part_cases(self, case_ids):
        '''
        从数据库中查询并组装好某个project中某些测试用例用于测试执行
        :param pro_name:
        :param case_ids:
        :return:
        '''
        test_cases = session.query(TestCase).filter(TestCase.id.in_(case_ids)).all()
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
            variables_obj = session.query(VariablesGlobal). \
                filter(VariablesGlobal.config_id == config_obj.id).join(Config, isouter=True).all()
            print("variablesGlobal: ", variables_obj)
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
                case_id = step_obj.testcase_id
                case_obj = session.query(TestCase).filter_by(id=case_id).first()
                project_id = case_obj.project_id
                step_name = step["test"]["name"]
                names = [test_api["api"]["name"] for test_api in testapis]
                if step_name not in names:
                    api_obj = session.query(API).filter(API.name == step_name and project_id == project_id).first()
                    api = json.loads(api_obj.body)  # api的主体信息
                    testapis.append(api)

                # variables of teststep
                variables_obj = session.query(VariablesLocal). \
                    filter(VariablesLocal.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                print("VariablesLocal: ", variables_obj)
                variable_list = []
                for item in variables_obj:
                    element = {item.key: json.loads(item.value)}
                    variable_list.append(element)
                step["test"].update({"variables": variable_list})

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
                    expected_type = item.expected_type
                    if expected in ["200", "404", "500", "401"]:
                        expected = int(expected)
                    if expected_type == "int":
                        expected = int(expected)
                    element = {comparator: [check, expected]}
                    validate_list.append(element)
                step["test"].update({"validate": validate_list})  # teststep中的validate可能会add\update\delete，所以要update

                # extract of teststep
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

        return case_ids, testapis, testcases

    def retrieve_one_case(self, case_id):
        case_ids, testapis, testcases = self.retrieve_part_cases([case_id])
        return case_id, testcases[0]

    def retrive_project_cases(self, project_id):
        project_obj = session.query(Project).filter(Project.id == project_id).first()
        testcases_obj = session.query(TestCase).filter(TestCase.project_id == project_obj.id).join(Project).all()
        case_id_names = [(case.id, case.name) for case in testcases_obj]
        return case_id_names

    def retrieve_part_cases_ui(self, case_ids):
        '''
        从数据库中查询并组装好某个project中某些测试用例用于测试执行
        :param pro_name:
        :param case_ids:
        :return:
        '''
        test_cases = session.query(TestCase).filter(TestCase.id.in_(case_ids)).all()
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
                element = {"id": item.id, "config_id": config_obj.id, "key": item.key, "value": item.value}
                parameter_list.append(element)
            case_config["config"].update({"parameters": parameter_list})

            # variables of config
            variables_obj = session.query(VariablesGlobal). \
                filter(VariablesGlobal.config_id == config_obj.id).join(Config, isouter=True).all()
            print("VariablesGlobal: ", variables_obj)
            variable_list = []
            for item in variables_obj:
                if not isinstance(item.value, str):
                    value = json.loads(item.value)
                else:
                    value = item.value

                element = {"id": item.id, "config_id": config_obj.id, "key": item.key, "value": value}
                variable_list.append(element)
            case_config["config"].update({"variables": variable_list})
            case_config.update({"config_id": config_obj.id})
            case_config.update({"case_id": case_obj.id})
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
                case_id = step_obj.testcase_id
                case_obj = session.query(TestCase).filter_by(id=case_id).first()
                project_id = case_obj.project_id
                step_name = step["test"]["name"]
                names = [test_api["api"]["name"] for test_api in testapis]
                if step_name not in names:
                    api_obj = session.query(API).filter(API.name == step_name and project_id == project_id).first()
                    api = json.loads(api_obj.body)  # api的主体信息
                    testapis.append(api)

                # variables of teststep
                variables_obj = session.query(VariablesLocal). \
                    filter(VariablesLocal.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                print("VariablesLocal: ", variables_obj)
                variable_list = []
                for item in variables_obj:
                    if not isinstance(item.value, str):
                        value = json.loads(item.value)
                    else:
                        value = item.value

                    element = {"id": item.id, "config_id": config_obj.id, "key": item.key, "value": value}
                    variable_list.append(element)
                step["test"].update({"variables": variable_list})

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
                    expected_type = item.expected_type
                    if expected in ["200", "404", "500", "401"]:
                        expected = int(expected)
                    if expected_type == "int":
                        expected = int(expected)
                    element = {"id": item.id, "step_id": step_obj.id, "comparator": comparator, "check": check,
                               "expected": expected}
                    validate_list.append(element)
                step["test"].update({"validate": validate_list})  # teststep中的validate可能会add\update\delete，所以要update

                # validate of teststep
                extracts_obj = session.query(Extract). \
                    filter(Extract.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                print("extracts: ", extracts_obj)
                extract_list = []
                for item in extracts_obj:
                    element = {"id": item.id, "step_id": step_obj.id, "key": item.key, "value": item.value}
                    extract_list.append(element)
                step["test"].update({"extract": extract_list})  # teststep中的extract可能会add\update\delete，所以要update
                step.update({"step_id": step_obj.id})
                case_steps.append(step)

            test_case = test_case + case_steps
            testcases.append((case_name, test_case))

        return case_ids, testapis, testcases

    def retrieve_one_case_ui(self, case_id):
        case_ids, testapis, testcases = self.retrieve_part_cases_ui([case_id])
        return case_id, testcases[0]
