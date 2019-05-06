from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import InternalError, InterfaceError
from SwaggerToCase.DB_operation.models import Parameters
from SwaggerToCase.DB_operation.curd import CURD, session
import json

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('config_id', type=str)
parser.add_argument('key', type=str)
parser.add_argument('value', type=str)


class ParameterItem(Resource):
    def get(self):
        args = parser.parse_args()
        parameter_id = int(args["id"])
        try:
            parameter = session.query(Parameters).filter_by(id=parameter_id).first()
            rst = make_response(jsonify({"success": True,
                                         "id": parameter.id,
                                         "config_id": parameter.config_id,
                                         "key": parameter.key,
                                         "value": parameter.value
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
        parameter_id = int(args["id"])
        status, msg = curd.delete_parameter(parameter_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        status, msg = curd.update_parameter(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        config_id = int(args["config_id"])
        variable = {"key": args["key"], "value": args["value"]}
        status, msg = curd.add_variable(config_id, variable)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
