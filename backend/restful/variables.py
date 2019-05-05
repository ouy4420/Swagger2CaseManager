from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import InternalError, InterfaceError
from SwaggerToCase.DB_operation.models import Variables
from SwaggerToCase.DB_operation.curd import CURD, session
import json

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
            variable = session.query(Variables).filter_by(id=variable_id).first()
            rst = make_response(jsonify({"success": True,
                                         "id": variable.id,
                                         "config_id": variable.config_id,
                                         "key": variable.key,
                                         "value": variable.value
                                         }))
            return rst
        except InternalError as e:
            print('InternalError:', e)
            session.rollback()
        except InterfaceError as e:
            print('InterfaceError:', e)
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!"}))

    def delete(self):
        args = parser.parse_args()
        variable_id = int(args["id"])
        status = curd.delete_variable(variable_id)
        if status:
            rst = make_response(jsonify({"success": True, "msg": "Variable删除成功"}))
        else:
            rst = make_response(jsonify({"success": False, "msg": "Variable删除失败"}))
        return rst

    def patch(self):
        args = parser.parse_args()
        status = curd.update_variable(args)
        if status:
            rst = make_response(jsonify({"success": True, "msg": "Variable更新成功"}))
        else:
            rst = make_response(jsonify({"success": False, "msg": "Variable更新失败"}))
        return rst

    def post(self):
        args = parser.parse_args()
        config_id = int(args["config_id"])
        variable = {"key": args["key"], "value": args["value"]}
        status = curd.add_variable(config_id, variable)
        if status:
            rst = make_response(jsonify({"success": True, "msg": "Variable新增成功"}))
        else:
            rst = make_response(jsonify({"success": False, "msg": "Variable新增失败"}))
        return rst
