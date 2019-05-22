import json
import traceback
import logging
from backend.models.compress import dump_report
mylogger = logging.getLogger("Swagger2CaseManager")

from backend.models.models import Project, \
    TestCase, Config, StepCase, API, Validate, Extract, \
    Parameters, VariablesGlobal, Report, VariablesLocal, VariablesEnv, DebugTalk, BaseURL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8",
#                        # echo=True,
#                        isolation_level='AUTOCOMMIT',  # 加上这句解决查询数据库不更新的情况
#                        pool_size=8,
#                        max_overflow=10,
#                        pool_timeout=30,
#                        pool_pre_ping=True)
engine = create_engine("mysql+pymysql://root:ate.sqa@192.168.72.128:3306/swagger?charset=utf8",
                       # echo=True,
                       isolation_level='AUTOCOMMIT',  # 加上这句解决查询数据库不更新的情况
                       pool_size=8,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_pre_ping=True)
Session = sessionmaker(bind=engine)



class ProjectCURD:
    def __init__(self):
        self.api = APICURD()
        self.case = TestCaseCURD()
        self.env = VarEnvCURD()
        self.debugtalk = DebugTalkCURD()
        self.report = ReportCURD()
        self.base_url = BaseURLCURD

    def add_project(self, project):
        session = Session()
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
            self.debugtalk.add_debugtalk(project_obj.id)
            return True, "Project创建成功！"
        except Exception as e:
            session.rollback()
            return False, "Project创建失败！" + str(e)
        finally:
            session.close()

    def add_project_by_url(self):
        pass

    def add_project_by_file(self):
        pass

    def delete_project(self, project_id):
        session = Session()
        try:
            testcases_obj = session.query(TestCase).filter(TestCase.project_id == project_id).join(Project).all()
            [self.case.delete_case(test_case.id) for test_case in testcases_obj]

            apis_obj = session.query(API).filter(API.project_id == project_id).join(Project).all()
            [self.api.delete_api(test_api.id) for test_api in apis_obj]

            envs_obj = session.query(VariablesEnv).filter(VariablesEnv.project_id == project_id).join(Project).all()
            [self.env.delete_variable_env(var_env.id) for var_env in envs_obj]

            base_urls_obj = session.query(BaseURL).filter(BaseURL.project_id == project_id).join(Project).all()
            [self.base_url.delete_base_url(base_url.id) for base_url in base_urls_obj]

            reports_obj = session.query(Report).filter(Report.project_id == project_id).join(Project).all()
            [self.report.delete_report(test_report.id) for test_report in reports_obj]

            debugtalks_obj = session.query(DebugTalk).filter(DebugTalk.project_id == project_id).join(Project).all()
            [self.debugtalk.delete_debugtalk(debugtalk.id) for debugtalk in debugtalks_obj]

            session.query(Project).filter_by(id=project_id).delete()
            session.commit()
            return True, "Project删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Project删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_project(project_id, project):
        session = Session()
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
        finally:
            session.close()

    def retrieve_project(self):
        pass


class TestCaseCURD:
    def __init__(self):
        self.config = ConfigCURD()
        self.step = StepCURD()

    def add_case(self, args):
        session = Session()
        try:
            try:
                case_obj = TestCase(name=args["case_name"], project_id=args["project_id"])
                session.add(case_obj)
                session.commit()
            except Exception as e:
                error_decription = "空的TestCase创建失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            try:
                config = {
                    "config": {
                        "name": args["case_name"],
                        "request": {
                            "base_url": "$base_url",
                            "headers": {
                                "Content-Type": "application/json;charset=UTF-8"
                            }
                        },
                        "parameters": [],
                        "variables": []
                    }
                }
                name = config["config"]["name"]
                body = json.dumps(config)
                config_obj = Config(name=name, body=body, testcase_id=case_obj.id)
                session.add(config_obj)
                session.commit()
            except Exception as e:
                error_decription = "TestCase添加config失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e
            mylogger.info("TestCase创建过程成功！")
            return True, "TestCase创建过程成功！"
        except Exception as e:
            session.rollback()
            mylogger.error("TestCase创建过程：失败！")
            return False, "TestCase创建过程：失败！" + str(e)
        finally:
            session.close()

    def delete_case(self, case_id):
        # session.query(TestCase).filter_by(id=case_id).delete()  # 只是这样，删不了，因为有config和stepcase通过外键引用
        # 要想删除testcase, 先删除config和teststep
        # 同理，要想删除config，先删除parameters和variables
        # 要想删除teststep，先删除api(这个不合适)、validate和extract
        session = Session()
        try:
            try:
                config_obj = session.query(Config).filter(Config.testcase_id == case_id).join(TestCase).first()
                self.config.delete_config(config_obj.id)
            except Exception as e:
                error_decription = "删除Case过程： 删除config失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            try:
                teststeps_obj = session.query(StepCase).filter(StepCase.testcase_id == case_id).join(TestCase).all()
                [self.step.delete_setp(teststep.id) for teststep in teststeps_obj]
            except Exception as e:
                error_decription = "删除Case过程： 删除teststeps失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            try:
                session.query(TestCase).filter_by(id=case_id).delete()
                session.commit()
            except Exception as e:
                error_decription = "删除Case过程： 删除testcase失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e
            mylogger.info("TestCase删除过程成功！")
            return True, "TestCase删除过程成功！"
        except Exception as e:
            session.rollback()
            mylogger.error("TestCase删除过程：失败！")
            return False, "TestCase删除过程：失败！" + str(e)
        finally:
            session.close()

    def retrieve_part_cases(self, case_ids, flag=None):
        '''
        从数据库中查询并组装好某个project中某些测试用例用于测试执行
        :param pro_name:
        :param case_ids:
        :return:
        '''
        session = Session()
        try:
            test_cases = session.query(TestCase).filter(TestCase.id.in_(case_ids)).all()
            testcases = []  # 要执行的测试用例
            testapis = []  # 测试用例执行相关的api
            for case_obj in test_cases:
                case_name = case_obj.name
                test_case = []  # testcase, include config and teststeps
                # print("case : ", case_obj)

                # ----------------------------测试用例的config数据 ----------------------------
                config_obj = session.query(Config).filter(Config.testcase_id == case_obj.id).join(TestCase).first()
                # print("config: ", config_obj)
                case_config = json.loads(config_obj.body)

                # parameters of config
                parameters_obj = session.query(Parameters). \
                    filter(Parameters.config_id == config_obj.id).join(Config, isouter=True).all()

                # print("parameters: ", parameters_obj)
                parameter_list = []
                for item in parameters_obj:
                    if item.value_type == "json_list":
                        value = json.loads(item.value)
                    else:
                        value = item.value
                    if flag == "UI":
                        element = {"id": item.id,
                                   "config_id": config_obj.id,
                                   "key": item.key,
                                   "value": value,
                                   "value_type": item.value_type
                                   }
                    else:
                        element = {item.key: value}
                    parameter_list.append(element)
                case_config["config"].update({"parameters": parameter_list})

                # variables of config
                variables_obj = session.query(VariablesGlobal). \
                    filter(VariablesGlobal.config_id == config_obj.id).join(Config, isouter=True).all()
                # print("variablesGlobal: ", variables_obj)
                variable_list = []
                for item in variables_obj:
                    value_type = item.value_type
                    if value_type == "int":
                        value = int(item.value)
                    elif value_type == "json":
                        value = json.loads(item.value)
                    else:
                        value = item.value
                    if flag == "UI":
                        element = {"id": item.id,
                                   "config_id": config_obj.id,
                                   "key": item.key,
                                   "value": value,
                                   "value_type": value_type}
                    else:
                        element = {item.key: value}
                    variable_list.append(element)
                case_config["config"].update({"variables": variable_list})
                if flag == "UI":
                    case_config.update({"config_id": config_obj.id})
                    case_config.update({"case_id": case_obj.id})

                test_case.append(case_config)

                # ----------------------------测试用例的teststeps数据 ----------------------------
                teststeps_obj = session.query(StepCase).filter(StepCase.testcase_id == case_obj.id).join(TestCase).all()
                # print(type(teststeps_obj), teststeps_obj)
                case_steps = []  # teststeps
                teststeps_obj = sorted(teststeps_obj, key=lambda x: x.step)
                for step_obj in teststeps_obj:
                    # print("step: ", step_obj)

                    step = {
                        "test": {
                            "name": step_obj.name,
                            "api": step_obj.api_name,
                            "variables": [],
                            "validate": [],
                            "extract": []
                        }
                    }

                    # testcase corresponding api
                    case_id = step_obj.testcase_id
                    case_obj = session.query(TestCase).filter_by(id=case_id).first()
                    project_id = case_obj.project_id
                    step_api_name = step_obj.api_name
                    names = [test_api["api"]["def"] for test_api in testapis]
                    if step_api_name not in names:
                        api_obj = session.query(API).filter(
                            API.api_func == step_api_name and project_id == project_id).first()
                        if api_obj is None:
                            raise ValueError("测试用例中引用的API已不存在，请删除新建")
                        api = json.loads(api_obj.body)  # api的主体信息
                        testapis.append(api)

                    # variables of teststep
                    variables_obj = session.query(VariablesLocal). \
                        filter(VariablesLocal.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                    # print("VariablesLocal: ", variables_obj)
                    variable_list = []
                    for item in variables_obj:
                        value_type = item.value_type
                        if value_type == "int":
                            value = int(item.value)
                        elif value_type == "json":
                            value = json.loads(item.value)
                        else:
                            value = item.value
                        if flag == "UI":
                            element = {"id": item.id,
                                       "step_id": step_obj.id,
                                       "key": item.key,
                                       "value": value,
                                       "value_type": value_type
                                       }
                        else:
                            element = {item.key: value}
                        variable_list.append(element)
                    step["test"].update({"variables": variable_list})

                    # validate of teststep

                    validates_obj = session.query(Validate).filter(Validate.stepcase_id == step_obj.id).join(StepCase,
                                                                                                             isouter=True).all()

                    # if validates_obj is not None:
                    # print("validates: ", validates_obj)
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
                        if flag == "UI":
                            element = {"id": item.id, "step_id": step_obj.id, "comparator": comparator, "check": check,
                                       "expected": expected}
                        else:
                            element = {comparator: [check, expected]}
                        validate_list.append(element)
                    step["test"].update({"validate": validate_list})  # teststep中的validate可能会add\update\delete，所以要update

                    # extract of teststep
                    extracts_obj = session.query(Extract). \
                        filter(Extract.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                    # print("extracts: ", extracts_obj)
                    extract_list = []
                    for item in extracts_obj:
                        if flag == "UI":
                            element = {"id": item.id, "step_id": step_obj.id, "key": item.key, "value": item.value}
                        else:
                            element = {item.key: item.value}
                        extract_list.append(element)
                    step["test"].update({"extract": extract_list})  # teststep中的extract可能会add\update\delete，所以要update
                    if flag == "UI":
                        step.update({"step_id": step_obj.id})
                        step.update({"step_pos": step_obj.step})
                    case_steps.append(step)

                test_case = test_case + case_steps
                testcases.append((case_name, test_case))
        except Exception as e:
            try:
                session.rollback()
            except Exception as error:
                pass
            error_decription = "用例详情获取失败！\n"
            error_location = traceback.format_exc()
            mylogger.error(error_decription + error_location)
            raise e
        finally:
            session.close()

        return case_ids, testapis, testcases


class ConfigCURD:
    def __init__(self):
        self.parameters = ParametersCURD()
        self.var_global = VarGlobalCURD()

    def add_config(self, case_id, config):
        pass

    def delete_config(self, config_id):
        session = Session()
        try:
            config_obj = session.query(Config).filter(Config.id == config_id).first()
            parameters_obj = session.query(Parameters). \
                filter(Parameters.config_id == config_obj.id).join(Config, isouter=True).all()
            [self.parameters.delete_parameter(parameter.id) for parameter in parameters_obj]
            variables_obj = session.query(VariablesGlobal). \
                filter(VariablesGlobal.config_id == config_obj.id).join(Config, isouter=True).all()
            [self.var_global.delete_variable_global(variable.id) for variable in variables_obj]
            session.query(Config).filter_by(id=config_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def update_config(config):
        session = Session()
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
        finally:
            session.close()

    def retrieve_config(self, config_id):
        pass


class ParametersCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_parameter(config_id, parameter):
        session = Session()
        try:
            parameter_obj = Parameters(key=parameter['key'],
                                       value=parameter["value"],
                                       value_type=parameter["value_type"],
                                       config_id=config_id)
            session.add(parameter_obj)
            session.commit()
            return True, "Parameter添加成功!"
        except Exception as e:
            session.rollback()
            return False, "Parameter添加失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_parameter(parameter_id):
        session = Session()
        try:
            session.query(Parameters).filter_by(id=parameter_id).delete()
            session.commit()
            return True, "Parameter删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Parameter删除成功！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_parameter(parameter):
        session = Session()
        try:
            parameter_obj = session.query(Parameters).filter(Parameters.id == parameter['id']).first()
            parameter_obj.key = parameter['key']
            parameter_obj.value = parameter["value"]
            parameter_obj.value_type = parameter["value_type"]
            session.add(parameter_obj)
            session.commit()
            return True, "更新parameter成功！"
        except Exception as e:
            session.rollback()
            return False, "更新parameter失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_parameter(parameter_id):
        session = Session()
        try:
            parameter = session.query(Parameters).filter_by(id=parameter_id).first()
            element = {
                "id": parameter.id,
                "key": parameter.key,
                "value": parameter.value,
                "value_type": parameter.value_type,
                "config_id": parameter.config_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class VarGlobalCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_variable_global(config_id, variable):
        session = Session()
        # 前端根据value_type做好类型校验
        try:
            variable_obj = VariablesGlobal(key=variable['key'],
                                           value=variable["value"],
                                           value_type=variable["value_type"],
                                           config_id=config_id)
            session.add(variable_obj)
            session.commit()
            return True, "全局变量添加成功！"
        except Exception as e:
            session.rollback()
            return False, "全局变量添加失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_variable_global(variable_id):
        session = Session()
        try:
            session.query(VariablesGlobal).filter_by(id=variable_id).delete()
            session.commit()
            return True, "全局变量删除成功！"
        except Exception as e:
            session.rollback()
            return False, "全局变量删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_variable_global(variable):
        session = Session()
        try:
            variable_obj = session.query(VariablesGlobal).filter(VariablesGlobal.id == variable['id']).first()
            variable_obj.key = variable['key']
            variable_obj.value = variable["value"]
            variable_obj.value_type = variable["value_type"]
            session.add(variable_obj)
            session.commit()
            return True, "全局变量更新成功！"
        except Exception as e:
            session.rollback()
            return False, "全局变量更新失败" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_variable_global(variable_id):
        session = Session()
        try:
            variable = session.query(VariablesGlobal).filter_by(id=variable_id).first()
            try:
                value = json.loads(variable.value)
            except Exception as e:
                value = variable.value

            element = {
                "id": variable.id,
                "key": variable.key,
                "value": value,
                "value_type": variable.value_type,
                "config_id": variable.config_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class StepCURD:
    def __init__(self):
        self.var_local = VarLocalCURD()
        self.validate = ValidateCURD()
        self.extract = ExtractCURD()

    def add_step(self, args):
        session = Session()
        try:
            try:
                new_step_obj = StepCase(name=args["name"],
                                        step=args["step_pos"],
                                        api_name=args["api_name"],
                                        testcase_id=args["case_id"])
                session.add(new_step_obj)
                session.commit()
            except Exception as e:
                # log中记录错误信息，方便定位错误
                error_decription = "空的TestStep创建失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                # 继续上抛错误，是作为add_step过程中某一个出错的点
                raise e

            # 获取所有调用api_name的API的TestStep,选用第一个作为模板
            # 若没有step引用这个API，old_step_obj=None
            old_step_obj = session.query(StepCase).filter_by(api_name=args["api_name"]).first()
            if old_step_obj is not None:
                try:
                    var_locals = session.query(VariablesLocal).filter(
                        VariablesLocal.stepcase_id == old_step_obj.id).all()
                    for var_local in var_locals:
                        element = {"key": var_local.key,
                                   "value": var_local.value,
                                   "value_type": var_local.value_type
                                   }
                        self.var_local.add_variable_local(new_step_obj.id, element)
                    mylogger.info("TestStep创建过程： VarLocal添加成功！")
                except Exception as e:
                    error_decription = "TestStep补充VarLocal数据失败！\n"
                    error_location = traceback.format_exc()
                    mylogger.error(error_decription + error_location)
                    raise e

                try:
                    validates = session.query(Validate).filter(Validate.stepcase_id == old_step_obj.id).all()
                    for validate in validates:
                        element = {"comparator": validate.comparator,
                                   "check": validate.check,
                                   "expected": validate.expected,
                                   "expected_type": validate.expected_type}
                        self.validate.add_validate(new_step_obj.id, element)
                    mylogger.info("TestStep创建过程： Validate添加成功！")
                except Exception as e:
                    error_decription = "TestStep创建过程：添加Validate数据失败！\n"
                    error_location = traceback.format_exc()
                    mylogger.error(error_decription + error_location)
                    raise e

                try:
                    extracts = session.query(Extract).filter(Extract.stepcase_id == old_step_obj.id).all()
                    for extract in extracts:
                        element = {"key": extract.key,
                                   "value": extract.value}
                        self.extract.add_extract(new_step_obj.id, element)
                    mylogger.info("TestStep创建过程： Extract添加成功！")
                except Exception as e:
                    error_decription = "TestStep创建过程：添加Extract数据失败！\n"
                    error_location = traceback.format_exc()
                    mylogger.error(error_decription + error_location)
                    raise e

            mylogger.info("TestStep创建过程成功！")
            return True, "TestStep创建过程成功！"
        except Exception as e:
            session.rollback()
            mylogger.error("TestStep创建过程：失败！")
            return False, "TestStep创建过程：失败！" + str(e)
        finally:
            session.close()

    def delete_setp(self, step_id):
        session = Session()
        try:
            step_obj = session.query(StepCase).filter(StepCase.id == step_id).first()

            try:
                variables_obj = session.query(VariablesLocal). \
                    filter(VariablesLocal.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                [self.var_local.delete_variable_local(variable.id) for variable in variables_obj]
                mylogger.info("TestStep删除过程： VarLocal数据成功！\n")
            except Exception as e:
                error_decription = "TestStep删除过程： VarLocal数据失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            try:
                validates_obj = session.query(Validate). \
                    filter(Validate.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                [self.validate.delete_validate(validate.id) for validate in validates_obj]
                mylogger.info("TestStep删除过程：Validate数据成功！\n")
            except Exception as e:
                error_decription = "TestStep删除过程： Validate数据失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            try:
                extracts_obj = session.query(Extract). \
                    filter(Extract.stepcase_id == step_obj.id).join(StepCase, isouter=True).all()
                [self.extract.delete_extract(extract.id) for extract in extracts_obj]
                mylogger.info("TestStep删除过程：Extract数据删除成功！\n")
            except Exception as e:
                error_decription = "TestStep删除过程：Extract数据删除失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            try:
                session.query(StepCase).filter_by(id=step_id).delete()
                session.commit()
            except Exception as e:
                error_decription = "TestStep删除失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e
            mylogger.info("TestStep删除过程成功！")
            return True, "TestStep删除过程成功！"
        except Exception as e:
            session.rollback()
            mylogger.error("TestStep删除过程失败！")
            return False, "TestStep删除过程失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_step(step):
        session = Session()
        try:
            step_obj = session.query(StepCase).filter(StepCase.id == step['id']).first()
            step_obj.name = step['step_name']
            session.add(step_obj)
            session.commit()
            return True, "Step名称更新成功！"
        except Exception as e:
            session.rollback()
            return False, "Step名称更新失败！" + str(e)
        finally:
            session.close()

    def retrieve_step(self, step_id):
        pass


class VarLocalCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_variable_local(stepcase_id, variable):
        session = Session()
        try:
            # 注意：这里variable是字符串（传进来需要json转换）
            variable_obj = VariablesLocal(key=variable['key'],
                                          value=variable["value"],
                                          value_type=variable["value_type"],
                                          stepcase_id=stepcase_id)
            session.add(variable_obj)
            session.commit()
            return True, "局部变量添加成功！"
        except Exception as e:
            session.rollback()
            return False, "局部变量添加失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_variable_local(variable_id):
        session = Session()
        try:
            session.query(VariablesLocal).filter_by(id=variable_id).delete()
            session.commit()
            return True, "局部变量删除成功！"
        except Exception as e:
            session.rollback()
            return False, "局部变量删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_variable_local(variable):
        session = Session()
        try:
            variable_obj = session.query(VariablesLocal).filter(VariablesLocal.id == variable['id']).first()
            variable_obj.key = variable['key']
            variable_obj.value = variable["value"]
            variable_obj.value_type = variable["value_type"]
            session.add(variable_obj)
            session.commit()
            return True, "局部变量更新成功！"
        except Exception as e:
            session.rollback()
            return False, "局部变量更新失败" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_variable_local(variable_id):
        """
        这个函数没用上！
        :param variable_id:
        :return:
        """
        session = Session()
        try:
            variable = session.query(VariablesLocal).filter_by(id=variable_id).first()
            element = {
                "id": variable.id,
                "key": variable.key,
                "value": json.loads(variable.value),
                "value_type": json.loads(variable.value),
                "stepcase_id": variable.stepcase_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class ValidateCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_validate(step_id, validate):
        session = Session()
        try:
            validate_obj = Validate(comparator=validate['comparator'],
                                    check=validate["check"],
                                    expected=validate["expected"],
                                    expected_type=validate["expected_type"],
                                    stepcase_id=step_id)
            session.add(validate_obj)
            session.commit()
            return True, "Validate添加成功!"
        except Exception as e:
            session.rollback()
            return False, "Validate添加失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_validate(validate_id):
        session = Session()
        try:
            session.query(Validate).filter_by(id=validate_id).delete()
            session.commit()
            return True, "Validate删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Validate删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_validate(validate):
        session = Session()
        try:
            validate_obj = session.query(Validate).filter(Validate.id == validate['id']).first()
            validate_obj.comparator = validate['comparator']
            validate_obj.check = validate["check"]
            validate_obj.expected = validate["expected"]
            validate_obj.expected_type = validate["expected_type"]
            session.add(validate_obj)
            session.commit()
            return True, "Validate更新成功！"
        except Exception as e:
            session.rollback()
            return False, "Validate更新失败" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_validate(validate_id):
        session = Session()
        try:
            validate = session.query(Validate).filter_by(id=validate_id).first()
            element = {
                "id": validate.id,
                "comparator": validate.comparator,
                "check": validate.check,
                "expected": validate.expected,
                "expected_type": validate.expected_type,
                "stepcase_id": validate.stepcase_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class ExtractCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_extract(step_id, extract):
        session = Session()
        try:
            extract_obj = Extract(key=extract['key'],
                                  value=extract["value"],
                                  stepcase_id=step_id)
            session.add(extract_obj)
            session.commit()
            return True, "Extract添加成功!"
        except Exception as e:
            session.rollback()
            return False, "Extract添加失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_extract(extract_id):
        session = Session()
        try:
            session.query(Extract).filter_by(id=extract_id).delete()
            session.commit()
            return True, "Extract删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Extract删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_extract(extract):
        session = Session()
        try:
            extract_obj = session.query(Extract).filter(Extract.id == extract['id']).first()
            extract_obj.key = extract['key']
            extract_obj.value = extract["value"]
            session.add(extract_obj)
            session.commit()
            return True, "Extract更新成功！"
        except Exception as e:
            session.rollback()
            return False, "Extract更新失败" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_extract(extract_id):
        session = Session()
        try:
            extract = session.query(Extract).filter_by(id=extract_id).first()
            element = {
                "id": extract.id,
                "key": extract.key,
                "value": extract.value,
                "stepcase_id": extract.stepcase_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class APICURD:
    def __init__(self):
        pass

    def add_api(self, project_id, api):
        session = Session()
        try:
            test_api = api["api"]
            api_func = test_api["def"]
            request = test_api["request"]
            url = request["url"]
            method = request["method"]
            body = json.dumps(api)
            api_obj = API(api_func=api_func,
                          url=url,
                          method=method,
                          body=body,
                          project_id=project_id)
            session.add(api_obj)
            session.commit()
            return True, "API新增成功！"
        except Exception as e:
            session.rollback()
            return False, "API新增失败！" + str(e)
        finally:
            session.close()

    def delete_api(self, api_id):
        session = Session()
        try:
            session.query(API).filter_by(id=api_id).delete()
            session.commit()
            return True, "API删除成功！"
        except Exception as e:
            session.rollback()
            return False, "API删除失败！" + str(e)
        finally:
            session.close()

    def update_api(self, api_id, api):
        session = Session()
        try:
            api_obj = session.query(API).filter(API.id == api_id).first()
            test_api = api["api"]
            api_obj.api_func = test_api["def"]
            request = test_api["request"]
            api_obj.url = request["url"]
            api_obj.method = request["method"]
            api_obj.body = json.dumps(api)
            session.add(api_obj)
            session.commit()
            return True, "API更新成功！"
        except Exception as e:
            session.rollback()
            return False, "API更新失败！" + str(e)
        finally:
            session.close()


class DebugTalkCURD:
    def __init__(self):
        pass

    def add_debugtalk(self, project_id):
        session = Session()
        try:
            debugtalk_obj = DebugTalk(
                code="# drive code for your project",
                project_id=project_id
            )
            session.add(debugtalk_obj)
            session.commit()
            return True, "debugtalk新增成功！"
        except Exception as e:
            session.rollback()
            return False, "debugtalk新增失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_debugtalk(project_id, code):
        session = Session()
        try:
            obj = session.query(DebugTalk).filter_by(project_id=project_id).first()
            if obj:
                obj.code = code
            else:
                obj = DebugTalk(code=code, project_id=project_id)
            session.add(obj)
            session.commit()
            return True, "DebugTalk保存成功！"
        except Exception as e:
            session.rollback()
            return False, "DebugTalk保存失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_debugtalk(debugtalk_id):
        session = Session()
        try:
            session.query(DebugTalk).filter_by(id=debugtalk_id).delete()
            session.commit()
            return True, "debugtalk删除成功！"
        except Exception as e:
            session.rollback()
            return False, "debugtalk删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_debugtalk(project_id):
        session = Session()
        try:
            obj = session.query(DebugTalk).filter_by(project_id=project_id).first()
            return obj.id, obj.code
        except Exception as e:
            session.rollback()
            error_decription = "获取debugtalk代码失败！\n"
            error_location = traceback.format_exc()
            mylogger.error(error_decription + error_location)
            raise e
        finally:
            session.close()


class VarEnvCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_variable_env(project_id, variable):
        session = Session()
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
        finally:
            session.close()

    @staticmethod
    def delete_variable_env(variable_id):
        session = Session()
        try:
            session.query(VariablesEnv).filter_by(id=variable_id).delete()
            session.commit()
            return True, "环境变量删除成功！"
        except Exception as e:
            session.rollback()
            return False, "环境变量删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_variable_env(variable):
        session = Session()
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
        finally:
            session.close()

    @staticmethod
    def retrieve_variable_env(variable_id):
        '''
        配合variable元素的update和delete
        :param variable_id:
        :return:
        '''
        session = Session()
        try:
            variable = session.query(VariablesEnv).filter_by(id=variable_id).first()
            element = {
                "id": variable.id,
                "key": variable.key,
                "value": json.loads(variable.value),
                "project_id": variable.project_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class ReportCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_report(report):
        session = Session()
        try:
            render_content = dump_report(report["render_content"])
            report_obj = Report(name=report['name'],
                                current_time=report["current_time"],
                                render_content=render_content,
                                result_stastic=report["result_stastic"],
                                tester=report["tester"],
                                description=report["description"],
                                project_id=report["project_id"])
            session.add(report_obj)
            session.commit()
            return True, "Report创建成功！"
        except Exception as e:
            session.rollback()
            return False, "Report创建失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_report(report_id):
        session = Session()
        try:
            session.query(Report).filter_by(id=report_id).delete()
            session.commit()
            return True, "Report删除成功！"
        except Exception as e:
            session.rollback()
            return False, "Report删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_report(report):
        session = Session()
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
        finally:
            session.close()

    @staticmethod
    def retrieve_variable_env(variable_id):
        '''
        配合variable元素的update和delete
        :param variable_id:
        :return:
        '''
        session = Session()
        try:
            variable = session.query(VariablesEnv).filter_by(id=variable_id).first()
            element = {
                "id": variable.id,
                "key": variable.key,
                "value": json.loads(variable.value),
                "project_id": variable.project_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()


class BaseURLCURD:
    def __init__(self):
        pass

    @staticmethod
    def add_base_url(project_id, env_config):
        session = Session()
        try:
            base_url_obj = BaseURL(name=env_config['name'],
                                   value=env_config["value"],
                                   project_id=project_id)
            session.add(base_url_obj)
            session.commit()
            return True, "环境添加成功！"
        except Exception as e:
            session.rollback()
            return False, "环境添加失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def delete_base_url(url_id):
        session = Session()
        try:
            session.query(BaseURL).filter_by(id=url_id).delete()
            session.commit()
            return True, "环境删除成功！"
        except Exception as e:
            session.rollback()
            return False, "环境删除失败！" + str(e)
        finally:
            session.close()

    @staticmethod
    def update_base_url(env_config):
        session = Session()
        try:
            base_url_obj = session.query(BaseURL).filter(BaseURL.id == env_config['id']).first()
            base_url_obj.name = env_config['name']
            base_url_obj.value = env_config["value"]
            session.add(base_url_obj)
            session.commit()
            return True, "环境更新成功！"
        except Exception as e:
            session.rollback()
            return False, "环境更新失败" + str(e)
        finally:
            session.close()

    @staticmethod
    def retrieve_base_url(url_id):
        '''
        配合variable元素的update和delete
        :param variable_id:
        :return:
        '''
        session = Session()
        try:
            base_url_obj = session.query(BaseURL).filter_by(id=url_id).first()
            element = {
                "id": base_url_obj.id,
                "name": base_url_obj.name,
                "value": json.loads(base_url_obj.value),
                "project_id": base_url_obj.project_id
            }
            return element
        except Exception as e:
            session.rollback()
        finally:
            session.close()
