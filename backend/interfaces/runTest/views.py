from flask import request, jsonify
from . import run_test
from backend.interfaces.auth.auth_decrator import login_require
from backend.models.curd import ReportCURD, TestCaseCURD, Session
from backend.models.models import Project, VariablesEnv, DebugTalk

from SwaggerToCase.dumper import DumpFile
from SwaggerToCase.inherit import run

import os
import json
import shutil


class RunTestError(ValueError):
    pass


@run_test.route('/api/waykichain/run_test/', methods=['POST'])
@login_require
def run_test():
    session = Session()
    try:
        # 解析参数
        case_list = request.json.get('case_list')
        project_id = request.json.get('project_id')
        base_url = request.json.get('base_url')

        cwd = os.getcwd()

        testproject_dir = os.path.join(os.path.join(cwd, r"SwaggerToCase"), 'TestProject')
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
        config["env_file"] = os.path.join(testproject_dir, ".env")
        config["code_file"] = os.path.join(testproject_dir, "debugtalk.py")

        case_curd = TestCaseCURD()
        report_curd = ReportCURD()
        case_ids, test_apis, test_cases = case_curd.retrieve_part_cases(case_list)
        dumper = DumpFile(config, test_apis, test_cases)
        dumper.dump_api_file()  # 写入api文件
        dumper.dump_testcases_files()  # 写入testcase文件
        vars_env = session.query(VariablesEnv).filter_by(project_id=project_id).all()
        # env_content = ""
        # for var in vars_env:
        #     key, value = var.key, var.value
        #     env_content += "{}={}\n".format(key, value)
        # dumper.dump_env_file(env_content)  # 写入env文件
        code_content = session.query(DebugTalk).filter_by(project_id=project_id).first().code
        # # import os
        # # username = os.environ["username"]
        # # password = os.environ["password"]
        # # base_url = os.environ["base_url"]
        # apend_content = "\nimport os\n"
        # for var in vars_env:
        #     key, value = var.key, var.value
        #     apend_content += '{} = os.environ["{}"]\n'.format(key, key)
        # dumper.dump_code_file(code_content + apend_content)  # 写入debugtalk文件
        apend_content = "\n\n"
        for var in vars_env:
            key, value = var.key, var.value
            apend_content += '{} = "{}"\n'.format(key, value)
        apend_content += '{} = "{}"\n'.format("base_url", base_url)
        dumper.dump_code_file(code_content + apend_content)  # 写入debugtalk文件

        try:
            report_list = run(testproject_dir, [project_name])
        except Exception as e:
            return jsonify({'success': False, 'msg': '用例执行失败！' + str(e)})
            # raise RunTestError('...')
        for report in report_list:
            file_name, current_time, render_content, result_stastic = report
            report_dict = {
                "project_id": project_id,
                "name": file_name,
                "current_time": current_time,
                "tester": project_obj.owner,
                "description": "",
                "render_content": render_content,
                "result_stastic": json.dumps(result_stastic)
            }
            report_curd.add_report(report_dict)
        file_name, current_time, render_content, result_stastic = report_list[0]
        return jsonify({'success': True, 'msg': '用例执行成功！', "render_content": render_content})
    except Exception as e:
        return jsonify({'success': False, 'msg': '用例执行失败！' + str(e)})
    finally:
        session.close()
