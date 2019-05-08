from SwaggerToCase.inherit import run
from SwaggerToCase.core import Swagger2Case
import os
import logging


def log_init():
    log_level = getattr(logging, 'debug'.upper())
    logging.basicConfig(level=log_level)


def gen_api_case(config):
    s2case = Swagger2Case(config)
    s2case.execute()


def main(swagger_name, file_type, url_or_file, project, specified_cases):
    log_init()

    cwd = os.getcwd()
    # test_pro_path = os.path.join(cwd, 'TestProject')
    test_pro_path = os.path.join(cwd, 'SwaggerToCase\\TestProject')
    apifilepath = os.path.join(test_pro_path, 'api')
    testcase_dir = os.path.join(test_pro_path, 'testcases\\{}'.format(swagger_name))
    api_file = r"{}\{}".format(apifilepath, swagger_name)
    config = {
        "file_or_url": url_or_file,
        "testcase_dir": testcase_dir,
        "api_file": api_file,
        "file_type": file_type,
        "project": project
    }
    gen_api_case(config)
    print(test_pro_path, url_or_file, swagger_name, file_type)

    run(test_pro_path, specified_cases)


def execute(project=None):
    print("project: ", project)
    try:
        swagger_name = project["name"]
        file_type = "YAML"
        if project["url"]:
            url_or_file = project["url"]
        else:
            url_or_file = project["file"]
        # url_or_file = r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\aa.json'
        # url_or_file = 'https://baas-test.wiccdev.org/v2/api/v2/api-docs'
        # specified_cases = ["aa\\getBlockHashUsingPOST.yml"]
        specified_cases = [swagger_name]
        main(swagger_name, file_type, url_or_file, project, specified_cases)
        return True, "Project创建成功！"
    except Exception as e:
        return False, "Project创建失败！" + str(e)


if __name__ == '__main__':
    project = {
        "name": 'ddd',
        "url": 'https://baas-test.wiccdev.org/v2/api/v2/api-docs',
        "owner": "Tiger"
    }
    execute(project)
