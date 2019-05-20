# ----------------------------------------------------------------------------------------------------------------------
import traceback
import logging

mylogger = logging.getLogger("Swagger2CaseManager")

# ----------------------------------------------------------------------------------------------------------------------
from flask import make_response, jsonify
from flask_restful import Resource, reqparse

# ----------------------------------------------------------------------------------------------------------------------
from backend.models.models import Project, TestCase, API, Report, BaseURL
from backend.models.curd import ProjectCURD, Session

curd = ProjectCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('name', type=str)
parser.add_argument('url', type=str)
parser.add_argument('file', type=dict)
parser.add_argument('desc', type=str)
parser.add_argument('responsible', type=str)


from SwaggerToCase.run import execute

# ----------------------------------------------------------------------------------------------------------------------
session_in_pro = Session()


class ProjectItem(Resource):
    def get(self, project_id):
        try:
            project = session_in_pro.query(Project).filter_by(id=project_id).first()
            test_apis = session_in_pro.query(API).filter_by(project_id=project_id).all()
            test_cases = session_in_pro.query(TestCase).filter_by(project_id=project_id).all()
            test_reports = session_in_pro.query(Report).filter_by(project_id=project_id).all()
            detail = [
                {"length": "{}个接口".format(len(test_apis)), "desc": "接口总数", "routerName": "APIView"},
                {"length": "{}个用例".format(len(test_cases)), "desc": "用例总数", "routerName": "AutoTest"},
                {"length": "{}套环境".format(0), "desc": "环境总数", "routerName": "GlobalEnv"},
                {"length": "{}个报告".format(len(test_reports)), "desc": "报告总数", "routerName": "Reports"}
            ]
            rst = make_response(jsonify({"success": True,
                                         "msg": "",
                                         "detail": detail,
                                         "name": project.name,
                                         "desc": project.desc
                                         }))
            return rst
        except Exception as e:
            try:
                session_in_pro.rollback()
            except Exception as error:
                pass
            return make_response(jsonify({"success": False, "msg": "获取项目详情失败!"}))

    def delete(self, project_id):
        status, msg = curd.delete_project(project_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self, project_id):
        args = parser.parse_args()
        args["owner"] = args["responsible"]
        status, msg = curd.update_project(project_id, args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst


def get_page(page, owner):
    all_rets = session_in_pro.query(Project).filter_by(owner=owner).all()
    all_rets_reverse = all_rets[::-1]
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    page_rets = all_rets_reverse[offset:offset + per_page]
    return all_rets_reverse, page_rets, pages


class ProjectList(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('owner', type=str)
            parser.add_argument('page', type=int)
            args = parser.parse_args()
            owner, page = args["owner"], args["page"]
            project_list = []
            all_rets_reverse, page_rets, pages = get_page(page, owner)
            for pro in page_rets:
                test_apis = session_in_pro.query(API).filter_by(project_id=pro.id).all()
                test_cases = session_in_pro.query(TestCase).filter_by(project_id=pro.id).all()
                test_reports = session_in_pro.query(Report).filter_by(project_id=pro.id).all()
                test_baseurls = session_in_pro.query(BaseURL).filter_by(project_id=pro.id).all()
                index = all_rets_reverse.index(pro) + 1
                project_list.append(
                    {"id": pro.id,
                     "index": index,
                     "name": pro.name,
                     "desc": pro.desc,
                     "responsible": pro.owner,
                     "mode": pro.mode,
                     "len_api": len(test_apis),
                     "len_case": len(test_cases),
                     "len_report": len(test_reports),
                     "len_baseurl": len(test_baseurls),
                     })
            page_previous, page_next = None, None
            if page > 1:
                page_previous = page - 1
            if page + 1 <= pages:
                page_next = page + 1
            rst = make_response(jsonify({"success": True,
                                         "msg": "projectList获取成功！",
                                         "results": project_list,
                                         "page": {"page_now": page,
                                                  "page_previous": page_previous,
                                                  "page_next": page_next}
                                         }))
            return rst
        except Exception as e:
            try:
                session_in_pro.rollback()
            except Exception as error:
                pass
            mylogger.error("projectList获取失败！\n" + str(e))
            return make_response(jsonify({"success": False, "msg": "projectList获取失败，请重新刷新页面！" + str(e)}))

    def post(self):
        args = parser.parse_args()
        args["owner"] = args["responsible"]
        try:
            obj = session_in_pro.query(Project).filter_by(name=args["name"]).first()
        except Exception as e:
            session_in_pro.rollback()
            rst = make_response(jsonify({"success": False, "msg": "项目新增失败！"}))
            return rst
        if obj is not None:
            rst = make_response(jsonify({"success": False, "msg": "项目名称已存在，请重新编辑！"}))
            return rst

        if args["url"] == "" and args["file"] == {}:
            status, msg = curd.add_project(args)
        else:
            status, msg = execute(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
