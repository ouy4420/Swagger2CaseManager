import json

from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from backend.models.models import Report, Project
from backend.models.curd import ReportCURD, Session
from backend.models.compress import load_report

from .send_mail import MailSend
from .mail_check import check_waykichain_mail

curd = ReportCURD()
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=int)
parser.add_argument('current_time', type=str)
parser.add_argument('name', type=str)
parser.add_argument('tester', type=str)
parser.add_argument('description', type=str)
parser.add_argument('mail', type=dict)


class ReportItem(Resource):
    def get(self, report_id):
        session = Session()
        try:
            report = session.query(Report).filter_by(id=report_id).first()
            render_content = load_report(report.render_content)
            rst = make_response(jsonify({"success": True,
                                         "msg": "",
                                         "render_content": render_content
                                         }))
            return rst
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"success": False, "msg": "sql error ==> rollback!" + str(e)}))
        finally:
            session.close()

    def delete(self, report_id):
        status, msg = curd.delete_report(report_id)
        rst = make_response(jsonify({"success": status, "msg": msg}))
        return rst

    def patch(self, report_id):
        try:
            args = parser.parse_args()
            print(args)
            status, msg = curd.update_report(args)
            rst = make_response(jsonify({"success": status, "msg": msg}))
            return rst
        except Exception as e:
            rst = make_response(jsonify({"success": False, "msg": str(e)}))
            return rst

    def post(self, report_id):
        """作为邮件发送"""
        session = Session()
        try:
            args = parser.parse_args()
            mailForm = args["mail"]
            mail_to = mailForm["to"]
            if not check_waykichain_mail(mail_to):
                rst = make_response(jsonify({"success": False, "msg": "发送方邮件格式不正确，请重新编辑！"}))
                return rst
            if mailForm["more"]:
                mail_more = mailForm["more"].split(";")
                for item in mail_more:
                    if not check_waykichain_mail(item):
                        rst = make_response(jsonify({"success": False, "msg": "抄送方存在邮件格式不正确，请重新编辑！"}))
                        return rst
                mail_list = [mail_to] + mail_more
            else:
                mail_list = [mail_to]
            report_obj = session.query(Report).filter(Report.id == mailForm["report_id"]).first()
            config = {
                "mail_from": mailForm["from"],
                "password": mailForm["password"],
                "mail_to": mail_list,
                "render_content": load_report(report_obj.render_content),
                "report_name": "{}_{}.html".format(report_obj.name, report_obj.current_time),
                "description": mailForm["description"]
            }
            mail = MailSend(config)
            mail.send()
            make_response(jsonify({"success": True, "msg": "邮件发送成功！"}))
        except Exception as e:
            rst = make_response(jsonify({"success": False, "msg": "邮件发送失败！" + str(e)}))
            return rst
        finally:
            session.close()


def get_page(page, project_id, session):
    all_rets = session.query(Report).filter_by(project_id=project_id).all()
    length = len(all_rets)
    per_page = 10
    pages = length // per_page
    if length % per_page > 0:
        pages += 1
    offset = per_page * (page - 1)
    page_rets = all_rets[offset:offset + per_page]
    return all_rets, page_rets, pages


class ReportList(Resource):
    def get(self):
        session = Session()
        try:
            args = parser.parse_args()
            print("args: ", args)
            id, page = args["id"], args["page"]
            report_list = []
            all_rets, page_rets, pages = get_page(page, id, session)
            for report in page_rets:
                index = all_rets.index(report) + 1
                item = {"index": index,
                        "id": report.id,
                        "name": report.name,
                        "current_time": report.current_time,
                        "tester": report.tester,
                        "description": report.description}
                item.update(json.loads(report.result_stastic))
                report_list.append(item)
            page_previous, page_next = None, None
            if page > 1:
                page_previous = page - 1
            if page + 1 <= pages:
                page_next = page + 1
            project = session.query(Project).filter_by(id=id).first()
            rst = make_response(jsonify({
                "success": True,
                "reportList": report_list,
                "projectInfo": {"name": project.name, "desc": project.desc},
                "page": {"page_now": page,
                         "page_previous": page_previous,
                         "page_next": page_next}}))
            return rst
        except Exception as e:
            rst = make_response(jsonify({"success": False, "msg": e}))
            return rst
        finally:
            session.close()
