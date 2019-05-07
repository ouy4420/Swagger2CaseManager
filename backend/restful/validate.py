from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from SwaggerToCase.DB_operation.models import Validate
from SwaggerToCase.DB_operation.curd import CURD, session


curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('config_id', type=str)
parser.add_argument('key', type=str)
parser.add_argument('value', type=str)


class ValidateItem(Resource):
    def get(self):
        args = parser.parse_args()
        validate_id = int(args["id"])
        try:
            validate = session.query(Validate).filter_by(id=validate_id).first()
            rst = make_response(jsonify({"success": True,
                                         "id": validate.id,
                                         "config_id": validate.config_id,
                                         "key": validate.key,
                                         "value": validate.value
                                         }))
            return rst
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))

    def delete(self):
        args = parser.parse_args()
        validate_id = int(args["id"])
        status, msg = curd.delete_validate(validate_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        status, msg = curd.update_validate(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        config_id = int(args["config_id"])
        variable = {"key": args["key"], "value": args["value"]}
        status, msg = curd.add_validate(config_id, variable)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
