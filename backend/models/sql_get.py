# ret = session.query(TestCase).filter(TestCase.project_id == 1).join(Project)
# print("testcases: ", ret.all())
# case = ret.all()[1]
# print("case 2: ", case)
# config = session.query(Config).filter(Config.testcase_id == case.id).join(TestCase).first()
# print("config: ", config)
#
# test_steps = session.query(StepCase).filter(StepCase.testcase_id == case.id).join(TestCase).all()
# print(test_steps)
# step = test_steps[0]
# print("step1: ", step)
# test_api = session.query(API).filter(API.stepcase_id == step.id).join(StepCase).first()
# print("test_api: ", test_api)
# validates = session.query(Validate).filter(Validate.stepcase_id == step.id).join(StepCase).all()
# print("validates: ", validates)
# extracts = session.query(Extract).filter(Extract.stepcase_id == step.id).join(StepCase).all()
# print("extracts： ", extracts)
#
# test_case = []
#
# case_config = json.loads(config.body)
# test_case.append(case_config)
#
# case_steps = []
# step1 = json.loads(step.body)
# validate_list = []
# for item in validates:
#     comparator = item.comparator
#     check = item.check
#     expected = item.expected
#     if expected in ["200", "404", "500", "401"]:
#         expected = int(expected)
#     element = {comparator: [check, expected]}
#     validate_list.append(element)
# step1["test"].update({"validate": validate_list})
#
# extract_list = []
# for item in extracts:
#     element = {item.key: item.value}
#     validate_list.append(element)
# step1["test"].update({"extract": extract_list})
# case_steps.append(step1)
# test_case = test_case + case_steps
#
# test_api = json.loads(test_api.body)
# test_apis = [test_api]
# test_cases = [(case.name, test_case)]
# print(test_apis)
# print(test_cases)


# step = session.query(StepCase).filter(StepCase.id == 11).first()
# print(step)
# name = step.name
# step_name = step.step_name
# body = step.body
# step_obj = StepCase(name=name,
#                     step=2,
#                     step_name=step_name,
#                     body=body,
#                     testcase_id=3)
# session.add(step_obj)
# session.commit()


from SwaggerToCase.dumper import DumpFile
from backend.models.curd import CURD

config = {}
config["testcase_dir"] = r"C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject\testcases\\aaa"
config["api_file"] = r"C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject\api\aaa"
config["file_type"] = "YAML"
curd = CURD()

case_ids, test_apis, test_cases = curd.retrieve_part_cases([30, 31, 33])
dumper = DumpFile(config, test_apis, test_cases)
dumper.dump_api_file()  # 写入api文件
dumper.dump_testcases_files()  # 写入testcase文件

# print(curd.retrive_project_cases(1))
# print(curd.retrieve_one_case(1))

from SwaggerToCase.inherit import run

ret = run(r"C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject",
          ["aaa\\signDayGoldUsingGET.yml"])
print(ret)
