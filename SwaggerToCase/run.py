from SwaggerToCase.inherit import run
from SwaggerToCase.core import SwaggerParser
import os
import logging


def start(url_or_file, swagger_name):
    cwd = os.getcwd()
    test_pro_path = os.path.join(cwd, 'TestProject')
    log_level = getattr(logging, 'debug'.upper())
    logging.basicConfig(level=log_level)
    s2case = SwaggerParser(url_or_file)
    apifilepath = os.path.join(test_pro_path, 'api')
    testcase_dir = os.path.join(test_pro_path, 'testcases\\{}'.format(swagger_name))
    api_file = r"{}\{}.yml".format(apifilepath, swagger_name)
    s2case.execute(testcase_dir, api_file, 'yml')
    run(test_pro_path, [swagger_name])


if __name__ == '__main__':
    url_or_file = r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\aa.json'
    # url_or_file = 'http://192.168.1.107:5000/swagger.json'
    swagger_name = 'MyTest'
    start(url_or_file, swagger_name)

