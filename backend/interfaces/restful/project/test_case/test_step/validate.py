from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from backend.models.models import Validate
from backend.models.curd import ValidateCURD, Session

curd = ValidateCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('validateForm', type=dict)


class ValidateItem(Resource):
    def get(self):
        args = parser.parse_args()
        validate_id = int(args["id"])
        session = Session()
        try:
            validate = session.query(Validate).filter_by(id=validate_id).first()
            rst = make_response(jsonify({"success": True,
                                         "id": validate.id,
                                         "config_id": validate.step_id,
                                         "key": validate.key,
                                         "value": validate.value
                                         }))
            return rst
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))
        finally:
            session.close()

    def delete(self):
        args = parser.parse_args()
        validate_id = int(args["id"])
        status, msg = curd.delete_validate(validate_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        validateForm = args["validateForm"]
        if validateForm["expected_type"] == 'int':
            try:
                validateForm["expected"] = int(validateForm["expected"])
            except ValueError as e:
                status, msg = False, "期望值-请选择正确的类型"
                rst = make_response(jsonify({"success": status, "msg": msg}))
                return rst
        status, msg = curd.update_validate(validateForm)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        validateForm = args["validateForm"]
        if validateForm["expected_type"] == 'int':
            try:
                validateForm["expected"] = int(validateForm["expected"])
            except ValueError as e:
                status, msg = False, "期望值-请选择正确的类型"
                rst = make_response(jsonify({"success": status, "msg": msg}))
                return rst
        step_id = int(validateForm["step_id"])
        status, msg = curd.add_validate(step_id, validateForm)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
