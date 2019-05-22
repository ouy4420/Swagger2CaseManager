from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.models import BaseURL
from backend.models.curd import BaseURLCURD, Session

curd = BaseURLCURD()
parser = reqparse.RequestParser()
parser.add_argument('project_id', type=int)
parser.add_argument('id', type=int)
parser.add_argument('obj', type=dict)


class BaseUrl(Resource):
    def get(self):
        session = Session()
        try:
            args = parser.parse_args()
            project_id = args["project_id"]
            BaseURLList = []
            all_rets = session.query(BaseURL).filter_by(project_id=project_id).all()
            for index, base_url in enumerate(all_rets):
                BaseURLList.append(
                    {"index": index + 1,
                     "id": base_url.id,
                     "name": base_url.name,
                     "value": base_url.value})

            rst = make_response(jsonify({
                "success": True,
                "BaseURLList": BaseURLList}))
            return rst
        except Exception as e:
            try:
                session.rollback()
            except Exception as error:
                pass
            rst = make_response(jsonify({"success": False, "msg": str(e)}))
            return rst
        finally:
            session.close()

    def post(self):
        args = parser.parse_args()
        var_form = args["obj"]
        status, msg = curd.add_base_url(var_form["project_id"], var_form)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        var_form = args["obj"]
        status, msg = curd.update_base_url(var_form)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def delete(self):
        args = parser.parse_args()
        status, msg = curd.delete_base_url(args["id"])
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
