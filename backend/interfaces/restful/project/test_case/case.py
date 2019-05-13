from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.models import Project, TestCase, Config
from backend.models.curd import TestCaseCURD, session
curd = TestCaseCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=int)



def parse_case_body(case):
    config = session.query(Config).filter_by(testcase_id=case.id).first()
    parsed_case = {
        "name": config.name,
    }
    return parsed_case


def get_page(page):
    all_rets = session.query(TestCase).filter_by(project_id=1).all()
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    page_rets = session.query(TestCase).filter_by(project_id=1).limit(per_page).offset(offset).all()
    return all_rets, page_rets, pages


class CaseListPage(Resource):
    def get(self):
        args = parser.parse_args()
        id, page = args["id"], args["page"]
        case_list = []
        try:
            all_rets, page_rets, pages = get_page(page)
            for case in page_rets:
                parsed_case = parse_case_body(case)
                parsed_case["index"] = all_rets.index(case) + 1
                parsed_case["id"] = case.id
                case_list.append(parsed_case)

            page_previous, page_next = None, None
            if page > 1:
                page_previous = page - 1
            if page + 1 <= pages:
                page_next = page + 1

            project = session.query(Project).filter_by(id=id).first()
            rst = make_response(jsonify({"caseList": case_list,
                                         "projectInfo": {"name": project.name, "desc": project.desc},
                                         "page": {"page_now": page,
                                                  "page_previous": page_previous,
                                                  "page_next": page_next}}))
            return rst
        except Exception as e:
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))

    def delete(self):
        pass

    def patch(self):
        pass

    def post(self):
        pass


class CaseList(Resource):
    def get(self):
        args = parser.parse_args()
        id = args["id"]
        case_list = []
        try:
            all_rets = session.query(TestCase).filter_by(project_id=id).all()
            for case in all_rets:
                parsed_case = parse_case_body(case)
                parsed_case["index"] = all_rets.index(case) + 1
                parsed_case["id"] = case.id
                case_list.append(parsed_case)

            project = session.query(Project).filter_by(id=id).first()
            rst = make_response(jsonify({"caseList": case_list,
                                         "projectInfo": {"name": project.name, "desc": project.desc}
                                         }))
            return rst
        except Exception as e:
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))

    def delete(self):
        pass

    def patch(self):
        pass

    def post(self):
        pass


class CaseItem(Resource):
    def get(self, case_id):
        try:
            case_ids, testapis, testcases = curd.retrieve_part_cases([case_id], flag="UI")
            case = testcases[0][1]  # 默认显示第一个测试用例的信息
            config = case.pop(0)
            teststeps = case
            # 确认最后一个teststep的step_pos
            if len(teststeps) > 0:
                last_step_pos = teststeps[-1]["step_pos"]
            else:
                last_step_pos = 1
            return make_response(jsonify({"success": True,
                                          "msg": "获取Case信息成功！",
                                          "teststeps": teststeps,
                                          "last_step_pos": last_step_pos,
                                          "config": config,
                                          "case_id": case_id}))
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False,
                                          "msg": "获取Case信息失败！" + str(e)}
                                         ))

    def delete(self, case_id):
        pass

    def put(self, case_id):
        pass
