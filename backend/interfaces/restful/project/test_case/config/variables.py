from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.models import VariablesGlobal
from backend.models.curd import CURD, session

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('config_id', type=str)
parser.add_argument('key', type=str)
parser.add_argument('value', type=str)


class VariableItem(Resource):
    def get(self):
        args = parser.parse_args()
        variable_id = int(args["id"])
        try:
            variable = session.query(VariablesGlobal).filter_by(id=variable_id).first()
            rst = make_response(jsonify({"success": True,
                                         "id": variable.id,
                                         "config_id": variable.config_id,
                                         "key": variable.key,
                                         "value": variable.value
                                         }))
            return rst
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))

    def delete(self):
        args = parser.parse_args()
        variable_id = int(args["id"])
        status, msg = curd.delete_variable_global(variable_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        status, msg = curd.update_variable_global(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        config_id = int(args["config_id"])
        variable = {"key": args["key"], "value": args["value"]}
        status, msg = curd.add_variable_global(config_id, variable)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
