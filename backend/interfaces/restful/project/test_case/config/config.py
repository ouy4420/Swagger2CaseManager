from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.curd import CURD

curd = CURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('name', type=str)


class ConfigItem(Resource):
    def get(self):
        pass

    def delete(self):
        pass

    def patch(self):
        args = parser.parse_args()
        status, msg = curd.update_config(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        pass
