from flask import request, jsonify
from . import run_test
from SwaggerToCase.inherit import run

from SwaggerToCase.DB_operation.curd import CURD
from SwaggerToCase.dumper import DumpFile


@run_test.route('/api/waykichain/run_test/', methods=['POST'])
def run_test():
    case_list = request.json.get('case_list')
    project_id = request.json.get('project_id')
    curd = CURD()
    config = {}
    config[
        "testcase_dir"] = r"C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject\testcases\\aaa"
    config["api_file"] = r"C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject\api\aaa"
    config["file_type"] = "YAML"
    case_ids, test_apis, test_cases = curd.retrieve_part_cases(case_list)
    dumper = DumpFile(config, test_apis, test_cases)
    dumper.dump_api_file()  # 写入api文件
    dumper.dump_testcases_files()  # 写入testcase文件
    report_list = run(r"C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject", ["aaa"])
    for report in report_list:
        file_name, current_time, render_content = report
        report_dict = {
            "project_id": project_id,
            "name": file_name,
            "current_time": current_time,
            "render_content": render_content
        }
        curd.add_report(report_dict)
    file_name, current_time, render_content = report_list[0]
    return jsonify({'success': True, 'msg': '用例执行成功！', "render_content": render_content})
