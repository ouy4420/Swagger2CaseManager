from flask import Flask, render_template
from flask_cors import CORS
import requests
from backend.interfaces.restful.project.project import ProjectList, ProjectItem
from backend.interfaces.restful.project.test_api.api import APILIst
from backend.interfaces.restful.project.test_case.case import CaseList, CaseItem
from backend.interfaces.restful.project.test_case.config.config import ConfigItem
from backend.interfaces.restful.project.test_case.test_step.teststep import StepItem
from backend.interfaces.restful.project.test_case.config.variables import VariableItem
from backend.interfaces.restful.project.test_case.test_step.variables import VariableLocalItem
from backend.interfaces.restful.project.test_case.config.parameters import ParameterItem
from backend.interfaces.restful.project.test_case.test_step.validate import ValidateItem
from backend.interfaces.restful.project.test_case.test_step.extract import ExtractItem
from backend.interfaces.restful.project.report.report import ReportList, ReportItem

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from backend.interfaces.auth import auth as auth_blueprint
from backend.interfaces.runTest import run_test as runTest_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(runTest_blueprint)

from flask_restful import Api

api = Api(app)
api.add_resource(ProjectList, '/api/waykichain/project/')
api.add_resource(ProjectItem, '/api/waykichain/project/<int:project_id>/')
api.add_resource(APILIst, '/api/waykichain/api/')
api.add_resource(CaseList, '/api/waykichain/case/')
api.add_resource(CaseItem, '/api/waykichain/case/<int:case_id>/')
api.add_resource(ConfigItem, '/api/waykichain/config/')
api.add_resource(StepItem, '/api/waykichain/step/')
api.add_resource(VariableItem, '/api/waykichain/variable/')
api.add_resource(VariableLocalItem, '/api/waykichain/variable_local/')
api.add_resource(ParameterItem, '/api/waykichain/parameter/')
api.add_resource(ValidateItem, '/api/waykichain/validate/')
api.add_resource(ExtractItem, '/api/waykichain/extract/')
api.add_resource(ReportList, '/api/waykichain/report/')
api.add_resource(ReportItem, '/api/waykichain/report/<int:report_id>/')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8081/{}'.format(path)).text
    return render_template("index.html")


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, host='192.168.161.1')
