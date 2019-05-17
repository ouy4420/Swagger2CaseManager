from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.models import VariablesEnv, Project
from backend.models.curd import VarEnvCURD, session

curd = VarEnvCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('var_id', type=int)
parser.add_argument('page', type=int)
parser.add_argument('var_obj', type=dict)


def get_page(page, project_id):
    all_rets = session.query(VariablesEnv).filter_by(project_id=project_id).all()
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    # page_rets = session.query(VariablesEnv).filter_by(project_id=project_id).limit(per_page).offset(offset).all()
    page_rets = all_rets[offset:offset+per_page]
    return all_rets, page_rets, pages


class VarEnv(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            print("args: ", args)
            id, page = args["id"], args["page"]
            var_envList = []
            all_rets, page_rets, pages = get_page(page, id)
            for var_env in page_rets:
                index = all_rets.index(var_env) + 1
                var_envList.append(
                    {"index": index,
                     "id": var_env.id,
                     "key": var_env.key,
                     "value": var_env.value})
            page_previous, page_next = None, None
            if page > 1:
                page_previous = page - 1
            if page + 1 <= pages:
                page_next = page + 1
            project = session.query(Project).filter_by(id=id).first()
            rst = make_response(jsonify({
                "success": True,
                "var_envList": var_envList,
                "projectInfo": {"name": project.name, "desc": project.desc},
                "page": {"page_now": page,
                         "page_previous": page_previous,
                         "page_next": page_next}}))
            return rst
        except Exception as e:
            rst = make_response(jsonify({"success": False, "msg": e}))
            return rst

    def post(self):
        args = parser.parse_args()
        var_form = args["var_obj"]
        status, msg = curd.add_variable_env(var_form["project_id"], var_form)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        var_form = args["var_obj"]
        status, msg = curd.update_variable_env(var_form)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def delete(self):
        args = parser.parse_args()
        status, msg = curd.delete_variable_env(args["id"])
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
