from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import InternalError, InterfaceError
from SwaggerToCase.DB_operation.models import Project, \
    TestCase, Config, StepCase, API, Validate, Extract, \
    Parameters, Variables
from SwaggerToCase.DB_operation.curd import CURD, session

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
            rst = make_response(jsonify({"len_apis": len(test_apis),
                                         "len_cases": len(test_cases),
                                         "len_envir": 0,
                                         "len_report": 0,
                                         "name": project.name,
                                         "desc": project.desc
                                         }))
            return rst
        except InternalError as e:
            print('InternalError:', e)
            session.rollback()
        except InterfaceError as e:
            print('InterfaceError:', e)
            session.rollback()

            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!"}))

    def delete(self, project_id):
        pass

    def put(self, project_id):
        pass


class ProjectList(Resource):
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
            project_list.append({"id": pro.id, "name": pro.name, "desc": pro.desc, "responsible": pro.owner, "mode": pro.mode})
        rst = make_response(jsonify({"results": project_list}))
        return rst

    def delete(self):
        args = parser.parse_args()
        project_id = int(args["id"])
        status, msg = curd.delete_project(project_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        project_id = int(args["id"])
        args["owner"] = args["responsible"]
        status, msg = curd.update_project(project_id, args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    # def post(self):
    #     args = parser.parse_args()
    #     args["owner"] = args["responsible"]
    #     status = curd.add_project(args)
    #     if status:
    #         rst = make_response(jsonify({"success": True, "msg": "项目创建成功"}))
    #     else:
    #         rst = make_response(jsonify({"success": False, "msg": "项目创建失败"}))
    #     return rst

    def post(self):
        args = parser.parse_args()
        args["owner"] = args["responsible"]
        if args["url"] == "" and args["file"] == {}:
            status, msg = curd.add_project(args)
        else:
            status, msg = execute(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
