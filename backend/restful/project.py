from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from SwaggerToCase.DB_operation.models import Project
from SwaggerToCase.DB_operation.curd import CURD, session

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('name', type=str)
parser.add_argument('desc', type=str)
parser.add_argument('responsible', type=str)


class PROJECT(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('owner', type=str)
        args = parser.parse_args()
        print("args: ", args)
        owner = args["owner"]
        project_list = []
        # session.flush()
        projects_obj = session.query(Project).filter_by(owner=owner).all()
        for pro in projects_obj:
            project_list.append({"id": pro.id, "name": pro.name, "desc": pro.desc, "responsible": pro.owner})
        rst = make_response(jsonify({"results": project_list}))
        return rst

    def delete(self):
        args = parser.parse_args()
        project_id = int(args["id"])
        status = curd.delete_project(project_id)
        if status:
            rst = make_response(jsonify({"success": True, "msg": "项目删除成功"}))
        else:
            rst = make_response(jsonify({"success": False, "msg": "项目更删除失败"}))
        return rst

    def patch(self):
        args = parser.parse_args()
        project_id = int(args["id"])
        args["owner"] = args["responsible"]
        status = curd.update_project(project_id, args)
        if status:
            rst = make_response(jsonify({"success": True, "msg": "项目更新成功"}))
        else:
            rst = make_response(jsonify({"success": False, "msg": "项目更新失败"}))
        return rst

    def post(self):
        args = parser.parse_args()
        args["owner"] = args["responsible"]
        status = curd.add_project(args)
        if status:
            rst = make_response(jsonify({"success": True, "msg": "项目创建成功"}))
        else:
            rst = make_response(jsonify({"success": False, "msg": "项目创建失败"}))
        return rst
