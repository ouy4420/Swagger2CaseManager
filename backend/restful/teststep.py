from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from SwaggerToCase.DB_operation.curd import CURD

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('name', type=str)


class StepItem(Resource):
    def get(self):
        pass

    def delete(self):
        pass

    def patch(self):
        args = parser.parse_args()
        status, msg = curd.update_step(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        pass
