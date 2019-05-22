from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from backend.models.models import Extract
from backend.models.curd import ExtractCURD, Session


curd = ExtractCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=str)
parser.add_argument('step_id', type=str)
parser.add_argument('key', type=str)
parser.add_argument('value', type=str)


class ExtractItem(Resource):
    def get(self):
        args = parser.parse_args()
        extract_id = int(args["id"])
        session = Session()
        try:
            extract = session.query(Extract).filter_by(id=extract_id).first()
            rst = make_response(jsonify({"success": True,
                                         "id": extract.id,
                                         "config_id": extract.step_id,
                                         "key": extract.key,
                                         "value": extract.value
                                         }))
            return rst
        except Exception as e:
            try:
                session.rollback()
            except Exception as error:
                pass
            return make_response(jsonify({"success": False, "msg": str(e)}))
        finally:
            session.close()

    def delete(self):
        args = parser.parse_args()
        extract_id = int(args["id"])
        status, msg = curd.delete_extract(extract_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self):
        args = parser.parse_args()
        status, msg = curd.update_extract(args)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def post(self):
        args = parser.parse_args()
        step_id = int(args["step_id"])
        extract = {"key": args["key"], "value": args["value"]}
        status, msg = curd.add_extract(step_id, extract)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst
