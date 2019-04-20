from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

a_language = api.model('language', {
    'language': fields.String('TheLanguage'),
    'id': fields.Integer('ID')
})

languages = list()
python = {'language': 'python', 'id': 1}
languages.append(python)


@api.route('/language')
class language(Resource):
    @api.marshal_with(a_language, envelope='data')  # envelope在这里
    def get(self):
        return languages

    @api.expect(a_language)
    def post(self):
        try:
            print(api.payload)
        except Exception as e:
            print(e)
        print(456)
        new_language = api.payload
        new_language['id'] = len(languages) + 1
        languages.append(new_language)
        return {'result': 'language added'}, 201

    @api.expect(a_language)
    def delete(self):
        del_language = api.payload
        languages.remove(del_language)
        return {'result': 'language deleteed'}, 201

    @api.expect(a_language)
    def put(self):
        put_language_id = api.payload["id"]
        put_language_lan = api.payload["language"]
        for index, item in enumerate(languages):
            if put_language_id == item["id"]:
                languages[index]["language"] = put_language_lan
            else:
                return {'result': 'This id is not exist'}, 201
        return {'result': 'language puted'}, 201


if __name__ == '__main__':
    app.run('192.168.1.107')
