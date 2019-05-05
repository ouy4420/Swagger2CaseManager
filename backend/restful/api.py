from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from SwaggerToCase.DB_operation.models import API
from SwaggerToCase.DB_operation.curd import CURD, session
import json

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=int)


def parse_api_body(api):
    parsed_api = {
        "name": api["api"]["name"],
        "url": api["api"]["request"]["url"],
        "method": api["api"]["request"]["method"],
        "headers": api["api"]["request"]["headers"],
        "params": json.dumps(api["api"]["request"]["params"]),
        "jsondata": api["api"]["request"]["json"],
        "defname": api["api"]["def"],
    }
    return parsed_api


def get_page(page):
    all_rets = session.query(API).filter_by(project_id=1).all()
    length = len(all_rets)
    per_page = 5
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    page_rets = session.query(API).filter_by(project_id=1).limit(per_page).offset(offset).all()
    return all_rets, page_rets, pages


class APILIst(Resource):
    def get(self):
        args = parser.parse_args()
        print("args: ", args)
        id, page = args["id"], args["page"]
        api_list = []
        all_rets, page_rets, pages = get_page(page)
        for api in page_rets:
            api_body = json.loads(api.body)
            request = api_body["api"]["request"]
            if "params" not in request:
                request["params"] = {}
            if "headers" not in request:
                request["headers"] = {}
            if "json" not in request:
                request["json"] = ""
            parsed_api = parse_api_body(api_body)
            parsed_api["index"] = all_rets.index(api) + 1
            api_list.append(parsed_api)

        page_previous, page_next = None, None
        if page > 1:
            page_previous = page - 1
        if page + 1 <= pages:
            page_next = page + 1

        rst = make_response(jsonify({"apiList": api_list, "page": {"page_now": page,
                                                                   "page_previous": page_previous,
                                                                   "page_next": page_next}}))
        return rst

    def delete(self):
        pass

    def patch(self):
        pass

    def post(self):
        pass
