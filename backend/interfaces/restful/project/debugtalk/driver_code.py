from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.interfaces.restful.project.debugtalk.execute_code import DebugCode
from backend.models.curd import DebugTalkCURD

curd = DebugTalkCURD
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('project_id', type=int)
parser.add_argument('code', type=str)
import os


class DriverCode(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            id, code = curd.retrieve_debugtalk(args["project_id"])
            rst = make_response(jsonify({"success": False, "msg": "", "code": code, "id": id}))
            return rst
        except Exception as e:
            rst = make_response(jsonify({"success": False, "msg": str(e)}))
            return rst

    def post(self):
        """
        用作在线调试
        :return:
        """
        args = parser.parse_args()
        code = args["code"].strip()
        cwd = os.getcwd()
        testproject_dir = os.path.join(os.path.join(cwd, "SwaggerToCase"), "TestProject")
        debugtalk_file = os.path.join(testproject_dir, r'debugtalk.py')
        try:
            debug = DebugCode(code=code, file_path=debugtalk_file)
            debug.run()
            rst = make_response(jsonify({"success": True, "msg": "代码执行成功", "resp": debug.resp}))
        except Exception as e:
            rst = make_response(jsonify({"success": False, "msg": "在线调试出错" + str(e),  "resp": ""}))
        return rst

    def patch(self):
        args = parser.parse_args()
        project_id = args["project_id"]
        code = args["code"]
        status, msg = curd.update_debugtalk(project_id, code)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def delete(self):
        pass
