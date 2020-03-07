import os

from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import datetime
import json


app = Flask(__name__)
app.config.update({
    'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


class ProbeUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.DateTime)
    host = db.Column(db.Text)
    data = db.Column(db.JSON)

    def __init__(self, upload_date, host, data):
        self.upload_date = upload_date
        self.data = data
        self.host = host

class Upload(Resource):

    def post(self, host):
        # Get the current time
        now = datetime.datetime.utcnow()
        # Get the token in the header
        if not request.headers.has_key("Authorization"):
            return "No Token", 401
        token = request.headers.get("Authorization")
        token = token.split()[1]
        if token != os.environ['TOKEN']:
            return "Not authorized", 403

        # Process the uploaded data
        new_doc = {}
        received_doc = json.loads(request.json)
        for key in received_doc.keys():
            new_doc[key] = {
                'size': received_doc[key]['total']['store']['size_in_bytes'],
                'doc_count': received_doc[key]['primaries']['docs']['count']
            }

        upload = ProbeUpload(now, host, new_doc)
        db.session.add(upload)
        db.session.commit()
        Upload.delete_expired()
        return 'created'

    @classmethod
    def delete_expired(cls):
        expiration_days = 181
        limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
        cls.query.filter(cls.upload_date <= limit).delete()
        db.session.commit()

class Download(Resource):
    def get(self, host):
        # Get the latest for a single host
        uploaded_data = ProbeUpload.query.filter(ProbeUpload.host == host).order_by(ProbeUpload.upload_date.desc())[0]
        return uploaded_data.data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

api.add_resource(Upload, '/upload/<host>/')
api.add_resource(Download, '/download/<host>/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)