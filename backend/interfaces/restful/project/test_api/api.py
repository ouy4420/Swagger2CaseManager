import json
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
import re
# ----------------------------------------------------------------------------------------------------------------------
from backend.models.models import API, Project
from backend.models.curd import APICURD, Session

curd = APICURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=int)
parser.add_argument('api_obj', type=dict)
parser.add_argument('api_id', type=str)

# ----------------------------------------------------------------------------------------------------------------------
import traceback
import logging

mylogger = logging.getLogger("Swagger2CaseManager")


def parse_api_body(api):
    parsed_api = {
        "name": api["api"]["name"],
        "url": api["api"]["request"]["url"],
        "method": api["api"]["request"]["method"],
        "headers": api["api"]["request"]["headers"],
        "params": api["api"]["request"]["params"],
        "json": api["api"]["request"]["json"],
        "data": api["api"]["request"]["data"],
        "defname": api["api"]["def"],
    }
    return parsed_api


def get_page(page, project_id, session):
    all_rets = session.query(API).filter_by(project_id=project_id).all()
    all_rets_reverse = all_rets[::-1]
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    page_rets = all_rets_reverse[offset:offset + per_page]
    return all_rets_reverse, page_rets, pages


def make_format(apiForm):
    headers, params = apiForm["headers"], apiForm["params"]
    if isinstance(headers, list):
        temp = {}
        for item in headers:
            temp.update({item["key"]: item["value"]})
        apiForm["headers"] = temp
    elif isinstance(headers, dict):
        apiForm["headers"] = headers

    if isinstance(params, list):
        temp = {}
        for item in params:
            if item["key"] and item["value"]:
                temp.update({item["key"]: item["value"]})
        apiForm["params"] = temp
    elif isinstance(params, dict):
        apiForm["params"] = params

    api = {
        "api":
            {"request": {"method": apiForm["method"],
                         "url": apiForm["url"],
                         "headers": apiForm["headers"],
                         "params": apiForm["params"],
                         "json": "",
                         "data": ""},
             "name": apiForm["name"],
             "def": apiForm["def"]}
    }
    if apiForm["body_type"] == "Json":
        api["api"]["request"]["json"] = "$data"
    elif apiForm["body_type"] == "Null":
        pass
    else:
        api["api"]["request"]["data"] = "$data"

    return api


class APILIst(Resource):
    def get(self):
        session = Session()
        try:
            args = parser.parse_args()
            if args["page"] is not None:
                id, page = args["id"], args["page"]
                api_list = []
                try:
                    all_rets_reverse, page_rets, pages = get_page(page, id, session)
                except Exception as e:
                    # 需要中间记录一下错误，可以按照下列做法
                    error_decription = "获取API分页数据失败！\n"
                    error_location = traceback.format_exc()
                    mylogger.error(error_decription + error_location)
                    raise e
                for api in page_rets:
                    api_body = json.loads(api.body)
                    request = api_body["api"]["request"]
                    if "params" not in request:
                        request["params"] = {}
                    if "headers" not in request:
                        request["headers"] = {}
                    if "json" not in request:
                        request["json"] = ""
                    if "data" not in request:
                        request["data"] = ""
                    parsed_api = parse_api_body(api_body)
                    parsed_api["index"] = all_rets_reverse.index(api) + 1
                    parsed_api["id"] = api.id
                    if parsed_api["json"]:
                        parsed_api["body_type"] = "Json"
                    elif parsed_api["data"]:
                        parsed_api["body_type"] = "Form"
                    else:
                        parsed_api["body_type"] = "Null"
                    api_list.append(parsed_api)

                page_previous, page_next = None, None
                if page > 1:
                    page_previous = page - 1
                if page + 1 <= pages:
                    page_next = page + 1
                project = session.query(Project).filter_by(id=id).first()
                rst = make_response(jsonify({"success": True, "msg": "",
                                             "apiList": api_list,
                                             "projectInfo": {"name": project.name, "desc": project.desc},
                                             "page": {"page_now": page,
                                                      "page_previous": page_previous,
                                                      "page_next": page_next}}))
                return rst
            else:
                project_id = args["id"]
                try:
                    apis_obj = session.query(API).filter_by(project_id=project_id).all()
                except Exception as e:
                    # 需要中间记录一下错误，可以按照下列做法
                    error_decription = "获取APIL所有数据失败！\n"
                    error_location = traceback.format_exc()
                    mylogger.error(error_decription + error_location)
                    raise e
                api_list = []
                for api in apis_obj:
                    api_list.append(api.api_func)
                rst = make_response(jsonify({"success": True, "msg": "", "api_list": api_list}))
                return rst
        except Exception as e:
            # 捕捉上面出错继续上抛的异常（做好log记录，便于异常时候排查）和其它可能的异常
            # 出错时，及时回滚数据库
            try:
                session.rollback()  # 这里的Exception不一定时数据库错误，盲目执行会报错
            except Exception as error:
                pass
            mylogger.error("获取APIList失败！\n")
            rst = make_response(jsonify({"success": False, "msg": "获取APIList失败！" + str(e)}))
            return rst
        finally:
            session.close()

    def delete(self):
        args = parser.parse_args()
        status, msg = curd.delete_api(args["api_id"])  # 这句会涉及数据库操作，但session是curd中的，对应出错时在那边进行回滚
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        apiForm = args["api_obj"]
        api = make_format(apiForm)
        status, msg = curd.update_api(apiForm["id"], api)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        apiForm = args["api_obj"]
        api_func, project_id = apiForm["def"], apiForm["project_id"]
        if re.match(r'^\w+(?:\(\)|\(\$data\))$', api_func) is None:
            rst = make_response(jsonify({"success": False, "msg": "API调用格式不正确，请重新编辑"}))
            return rst
        session = Session()
        try:
            obj = session.query(API).filter(API.api_func == api_func and API.project_id == project_id).first()
        except Exception as e:
            session.rollback()
            rst = make_response(jsonify({"success": False, "msg": "API新增失败！"}))
            return rst
        finally:
            session.close()
        if obj is not None:
            rst = make_response(jsonify({"success": False, "msg": "该项目中已存在同名API调用！！！"}))
            return rst
        api = make_format(apiForm)
        status, msg = curd.add_api(apiForm["project_id"], api)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
