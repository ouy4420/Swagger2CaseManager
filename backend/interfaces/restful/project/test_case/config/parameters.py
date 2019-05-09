from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from backend.models.models import Parameters
from backend.models.curd import ParametersCURD, session

import json

curd = ParametersCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('config_id', type=str)
parser.add_argument('key', type=str)
parser.add_argument('value', type=str)
parser.add_argument('value_type', type=str)


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
                                         "value": parameter.value,
                                         "value_type": parameter.value_type
                                         }))
            return rst
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))

    def delete(self):
        args = parser.parse_args()
        parameter_id = int(args["id"])
        status, msg = curd.delete_parameter(parameter_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        value, value_type = args["value"], args["value_type"]
        if value_type == "json_list":
            try:
                json.loads(value)
            except Exception as e:
                status, msg = False, "请选择正确的parameter类型" + str(e)
                rst = make_response(jsonify({"success": status, "msg": msg}))
                return rst
        status, msg = curd.update_parameter(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        config_id = int(args["config_id"])
        value, value_type = args["value"], args["value_type"]
        if value_type == "json_list":
            try:
                json.loads(value)
            except Exception as e:
                status, msg = False, "请选择正确的parameter类型" + str(e)
                rst = make_response(jsonify({"success": status, "msg": msg}))
                return rst
        status, msg = curd.add_parameter(config_id, args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
