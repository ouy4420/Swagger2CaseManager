from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from backend.models.models import Project, TestCase,  API, Report
from backend.models.curd import CURD, session

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('name', type=str)
parser.add_argument('url', type=str)
parser.add_argument('file', type=dict)
parser.add_argument('desc', type=str)
parser.add_argument('responsible', type=str)


from SwaggerToCase.run import execute


class ProjectItem(Resource):
    def get(self, project_id):
        try:
            project = session.query(Project).filter_by(id=project_id).first()
            test_apis = session.query(API).filter_by(project_id=project_id).all()
            test_cases = session.query(TestCase).filter_by(project_id=project_id).all()
            test_reports = session.query(Report).filter_by(project_id=project_id).all()
            rst = make_response(jsonify({"success": True,
                                         "msg": "",
                                         "len_apis": len(test_apis),
                                         "len_cases": len(test_cases),
                                         "len_envir": 0,
                                         "len_report": len(test_reports),
                                         "name": project.name,
                                         "desc": project.desc
                                         }))
            return rst
        except Exception as e:
            print('InternalError:', e)
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!"}))

    def delete(self, project_id):
        args = parser.parse_args()
        project_id = int(args["id"])
        status, msg = curd.delete_project(project_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self, project_id):
        args = parser.parse_args()
        project_id = int(args["id"])
        args["owner"] = args["responsible"]
        status, msg = curd.update_project(project_id, args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst


class ProjectList(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('owner', type=str)
            args = parser.parse_args()
            print("args: ", args)
            owner = args["owner"]
            project_list = []
            projects_obj = session.query(Project).filter_by(owner=owner).all()
            for pro in projects_obj:
                project_list.append(
                    {"id": pro.id, "name": pro.name, "desc": pro.desc, "responsible": pro.owner, "mode": pro.mode})
            rst = make_response(jsonify({"success": True, "msg": "projectList获取成功！", "results": project_list}))
            return rst
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "projectList获取失败！" + str(e)}))

    def post(self):
        args = parser.parse_args()
        args["owner"] = args["responsible"]
        if args["url"] == "" and args["file"] == {}:
            status, msg = curd.add_project(args)
        else:
            status, msg = execute(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

