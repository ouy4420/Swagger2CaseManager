from sqlalchemy.orm import sessionmaker
from SwaggerToCase.DB_operation.models import Project, TestCase, Config, StepCase, API, Validate, Extract
from sqlalchemy import create_engine
import json

engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8",
                       encoding='utf-8',
                       # echo=True,
                       max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()


class CURD(object):
    def __init__(self):
        pass

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def add_validate(self):
        pass

    def update_validate(self):
        pass

    def delete_validate(self):
        pass

    def add_extract(self):
        pass

    def update_extract(self):
        pass

    def delete_extract(self):
        pass

    def retrieve(self, pro_name, case_ids):
        project_obj = session.query(Project).filter(Project.name == pro_name).first()
        testcases_obj = session.query(TestCase).filter(TestCase.project_id == project_obj.id).join(Project).all()
        test_cases = [case for case in testcases_obj if case.id in case_ids]
        testcases = []
        testapis = []
        for case_obj in test_cases:
            case_name = case_obj.name
            test_case = []  # testcase, include config and teststeps
            print("case : ", case_obj)

            config_obj = session.query(Config).filter(Config.testcase_id == case_obj.id).join(TestCase).first()
            print("config: ", config_obj)
            case_config = json.loads(config_obj.body)
            test_case.append(case_config)

            teststeps_obj = session.query(StepCase).filter(StepCase.testcase_id == case_obj.id).join(TestCase).all()
            print(teststeps_obj)

            case_steps = []  # teststeps
            for step_obj in teststeps_obj:
                print("step: ", step_obj)

                step = json.loads(step_obj.body)

                api_obj = session.query(API).filter(API.stepcase_id == step_obj.id).join(StepCase).first()
                print("api: ", api_obj)
                testapis.append(json.loads(api_obj.body))

                validates_obj = session.query(Validate).filter(Validate.stepcase_id == step_obj.id).join(StepCase).all()
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
                step["test"].update({"validate": validate_list})

                extracts_obj = session.query(Extract).filter(Extract.stepcase_id == step_obj.id).join(StepCase).all()
                print("extracts: ", extracts_obj)
                extract_list = []
                for item in extracts_obj:
                    element = {item.key: item.value}
                    validate_list.append(element)
                step["test"].update({"extract": extract_list})

                case_steps.append(step)

            test_case = test_case + case_steps
            testcases.append((case_name, test_case))
        return testapis, testcases

