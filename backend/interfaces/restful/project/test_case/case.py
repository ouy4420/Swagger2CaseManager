# ----------------------------------------------------------------------------------------------------------------------
import traceback
import logging
mylogger = logging.getLogger("Swagger2CaseManager")

# ----------------------------------------------------------------------------------------------------------------------
from flask import make_response, jsonify
from flask_restful import Resource, reqparse

# ----------------------------------------------------------------------------------------------------------------------
from backend.models.models import Project, TestCase, Config
from backend.models.curd import TestCaseCURD

curd = TestCaseCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=int)
parser.add_argument('project_id', type=str)
parser.add_argument('case_name', type=str)
parser.add_argument('case_id', type=str)

# ----------------------------------------------------------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8",
                       encoding='utf-8',
                       # echo=True,
                       isolation_level='AUTOCOMMIT',  # 加上这句解决查询数据库不更新的情况
                       max_overflow=5,
                       pool_size=4,
                       pool_recycle=60 * 60 * 2,  # 设置pool_recycle参数在超时设定的时间(秒)后自动重新建立连接, 每过两小时建立一个新连接
                       )

Session = sessionmaker(bind=engine)
session_in_case = Session()


def parse_case_body(case):
    config = session_in_case.query(Config).filter_by(testcase_id=case.id).first()
    parsed_case = {
        "name": config.name,
    }
    return parsed_case


def get_page(page):
    all_rets = session_in_case.query(TestCase).filter_by(project_id=1).all()
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    page_rets = session_in_case.query(TestCase).filter_by(project_id=1).limit(per_page).offset(offset).all()
    return all_rets, page_rets, pages


class CaseListPage(Resource):
    def get(self):
        try:
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
            except Exception as e:
                try:
                    session_in_case.rollback()
                except Exception as e:
                    pass
                error_decription = "获取case数据失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e
            page_previous, page_next = None, None
            if page > 1:
                page_previous = page - 1
            if page + 1 <= pages:
                page_next = page + 1
            project = session_in_case.query(Project).filter_by(id=id).first()
            rst = make_response(jsonify({"success": True, "msg": "", "caseList": case_list,
                                         "projectInfo": {"name": project.name, "desc": project.desc},
                                         "page": {"page_now": page,
                                                  "page_previous": page_previous,
                                                  "page_next": page_next}}))
            return rst
        except Exception as e:
            try:
                session_in_case.rollback()
            except Exception as error:
                pass
            mylogger.error("获取CASE分页数据失败！\n")
            rst = make_response(jsonify({"success": False, "msg": "获取CASE分页数据失败！" + str(e)}))
            return rst

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
            try:
                all_rets = session_in_case.query(TestCase).filter_by(project_id=id).all()
            except Exception as e:
                error_decription = "获取case_list数据失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e
            for case in all_rets:
                parsed_case = parse_case_body(case)
                parsed_case["index"] = all_rets.index(case) + 1
                parsed_case["id"] = case.id
                case_list.append(parsed_case)

            project = session_in_case.query(Project).filter_by(id=id).first()
            rst = make_response(jsonify({"success": True, "msg": "", "caseList": case_list,
                                         "projectInfo": {"name": project.name, "desc": project.desc}
                                         }))
            return rst
        except Exception as e:
            try:
                session_in_case.rollback()
            except Exception as error:
                pass
            mylogger.error("获取CASEList失败！\n")
            rst = make_response(jsonify({"success": False, "msg": "获取CASEList失败！" + str(e)}))
            return rst

    def delete(self):
        args = parser.parse_args()
        status, msg = curd.delete_case(args["case_id"])
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        pass

    def post(self):
        args = parser.parse_args()
        status, msg = curd.add_case(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst


class CaseItem(Resource):
    def get(self, case_id):
        try:
            try:
                case_ids, testapis, testcases = curd.retrieve_part_cases([case_id], flag="UI")
            except Exception as e:
                error_decription = "获取case数据失败！\n"
                error_location = traceback.format_exc()
                mylogger.error(error_decription + error_location)
                raise e

            case = testcases[0][1]  # 默认显示第一个测试用例的信息
            config = case.pop(0)
            teststeps = case
            # 确认最后一个teststep的step_pos
            if len(teststeps) > 0:
                last_step_pos = teststeps[-1]["step_pos"]
            else:
                last_step_pos = 0
            return make_response(jsonify({"success": True,
                                          "msg": "获取Case信息成功！",
                                          "teststeps": teststeps,
                                          "last_step_pos": last_step_pos,
                                          "config": config,
                                          "case_id": case_id}))
        except Exception as e:
            try:
                session_in_case.rollback()
            except Exception as error:
                pass
            mylogger.error("获取CaseItem失败！\n")
            rst = make_response(jsonify({"success": False, "msg": "操作过于频繁，请稍后重试！！"}))
            return rst

    def delete(self, case_id):
        pass

    def put(self, case_id):
        pass


