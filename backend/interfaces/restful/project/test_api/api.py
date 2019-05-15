from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.models import API, Project
from backend.models.curd import APICURD, session
import json

curd = APICURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=int)
parser.add_argument('api_obj', type=dict)
parser.add_argument('api_id', type=str)


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


def get_page(page, project_id):
    all_rets = session.query(API).filter_by(project_id=project_id).all()
    all_rets_reverse = all_rets[::-1]
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    # page_rets = session.query(API).filter_by(project_id=project_id).limit(per_page).offset(offset).all()
    page_rets = all_rets_reverse[offset:offset + per_page]
    return all_rets_reverse, page_rets, pages


class APILIst(Resource):
    def get(self):
        args = parser.parse_args()
        print("args: ", args)
        if args["page"] is not None:
            id, page = args["id"], args["page"]
            api_list = []
            all_rets_reverse, page_rets, pages = get_page(page, id)
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
            rst = make_response(jsonify({"apiList": api_list,
                                         "projectInfo": {"name": project.name, "desc": project.desc},
                                         "page": {"page_now": page,
                                                  "page_previous": page_previous,
                                                  "page_next": page_next}}))
            return rst
        else:
            project_id = args["id"]
            apis_obj = session.query(API).filter_by(project_id=project_id).all()
            api_list = []
            for api in apis_obj:
                api_list.append(api.api_func)
            rst = make_response(jsonify({"api_list": api_list}))
            return rst

    def delete(self):
        args = parser.parse_args()
        status, msg = curd.delete_api(args["api_id"])
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        apiForm = args["api_obj"]
        api = {
            "api":
                {"request": {"method": apiForm["method"],
                             "url": apiForm["url"],
                             "headers": json.loads(apiForm["headers"]),
                             "params": json.loads(apiForm["params"]),
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
        status, msg = curd.update_api(apiForm["id"], api)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        apiForm = args["api_obj"]
        api_func, project_id = apiForm["def"], apiForm["project_id"]
        obj = session.query(API).filter(API.api_func == api_func and API.project_id == project_id).first()
        if obj is not None:
            rst = make_response(jsonify({"success": False, "msg": "该项目中已存在同名API调用！！！"}))
            return rst
        api = {
            "api":
                {"request": {"method": apiForm["method"],
                             "url": apiForm["url"],
                             "headers": json.loads(apiForm["headers"]),
                             "params": json.loads(apiForm["params"]),
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
        status, msg = curd.add_api(apiForm["project_id"], api)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
