from flask import request, jsonify
from . import run_test
from backend.interfaces.auth.auth_decrator import login_require
from backend.models.curd import ReportCURD, TestCaseCURD, session
from backend.models.models import Project

from SwaggerToCase.dumper import DumpFile
from SwaggerToCase.inherit import run

import os
import shutil


class RunTestError(ValueError):
    pass


@run_test.route('/api/waykichain/run_test/', methods=['POST'])
@login_require
def run_test():
    try:
        # 解析参数
        case_list = request.json.get('case_list')
        project_id = request.json.get('project_id')

        cwd = os.getcwd()

        testproject_dir = os.path.join(cwd, r"SwaggerToCase\TestProject")
        testcases_dir = os.path.join(testproject_dir, r"testcases")
        testapi_dir = os.path.join(testproject_dir, r"api")
        # 清空testcases_dir和testapi_dir
        shutil.rmtree(testcases_dir)
        shutil.rmtree(testapi_dir)
        os.mkdir(testcases_dir)
        os.mkdir(testapi_dir)

        project_obj = session.query(Project).filter_by(id=project_id).first()
        project_name = project_obj.name
        config = {}
        config["testcase_dir"] = os.path.join(testcases_dir, project_name)
        config["api_file"] = os.path.join(testapi_dir, project_name)
        config["file_type"] = "YAML"

        case_curd = TestCaseCURD()
        report_curd = ReportCURD()
        case_ids, test_apis, test_cases = case_curd.retrieve_part_cases(case_list)
        dumper = DumpFile(config, test_apis, test_cases)
        dumper.dump_api_file()  # 写入api文件
        dumper.dump_testcases_files()  # 写入testcase文件
        try:
            report_list = run(testproject_dir, [project_name])
        except Exception as e:
            return jsonify({'success': False, 'msg': '用例执行失败！' + str(e)})
            # raise RunTestError('...')
        for report in report_list:
            file_name, current_time, render_content = report
            report_dict = {
                "project_id": project_id,
                "name": file_name,
                "current_time": current_time,
                "tester": project_obj.owner,
                "description": "",
                "render_content": render_content
            }
            report_curd.add_report(report_dict)
        file_name, current_time, render_content = report_list[0]
        return jsonify({'success': True, 'msg': '用例执行成功！', "render_content": render_content})
    except Exception as e:
        return jsonify({'success': False, 'msg': '用例执行失败！' + str(e)})
