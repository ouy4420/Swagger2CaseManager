from flask import Flask, render_template
from flask_cors import CORS
import requests
from backend.restful.project import ProjectList, ProjectItem
from backend.restful.api import APILIst
from backend.restful.case import CaseList, CaseItem
from flask_restful import Api

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from backend.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

api = Api(app)
api.add_resource(ProjectList, '/api/waykichain/project/')
api.add_resource(ProjectItem, '/api/waykichain/project/<int:project_id>/')
api.add_resource(APILIst, '/api/waykichain/api/')
api.add_resource(CaseList, '/api/waykichain/case/')
api.add_resource(CaseItem, '/api/waykichain/case/<int:case_id>/')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8081/{}'.format(path)).text
    return render_template("index.html")


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, host='192.168.161.1')
