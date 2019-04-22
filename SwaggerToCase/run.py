from SwaggerToCase.inherit import run
from SwaggerToCase.core import SwaggerParser
import os
import logging


def start(file_or_url, swagger_name):
    cwd = os.getcwd()
    test_pro_path = os.path.join(cwd, 'TestProject')
    log_level = getattr(logging, 'debug'.upper())
    logging.basicConfig(level=log_level)

    apifilepath = os.path.join(test_pro_path, 'api')
    testcase_dir = os.path.join(test_pro_path, 'testcases\\{}'.format(swagger_name))
    api_file = r"{}\{}".format(apifilepath, swagger_name)
    config = {
        "file_or_url": file_or_url,
        "testcase_dir": testcase_dir,
        "api_file": api_file,
        "file_type": "YAML"
    }
    s2case = SwaggerParser(config)
    s2case.execute()

    run(test_pro_path, [swagger_name])


if __name__ == '__main__':
    url_or_file = r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\haha.json'
    # url_or_file = 'http://192.168.1.107:5000/swagger.json'
    swagger_name = 'MyTest'
    start(url_or_file, swagger_name)

