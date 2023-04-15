from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    def __repr__(self):
        returnJson = {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }
        return json.dumps(returnJson)


@app.route('/')
def index():
    return 'Hello World!'

@app.route("/notes/all", methods=["GET"])
def get_all_tasks():
    tasks = Note.query.all()
    print("tasks")
    retList = []
    for i in tasks:
        retDict = {}
        retDict["id"] = i.id
        retDict["title"] = i.title
        retDict["content"] = i.content
        retList.append(retDict)
    return json.dumps(retList)

@app.route("/notes/<int:id>", methods=["PATCH"])
def update_task(id):
    task = Note.query.get(id)
    task.title = request.json["title"]
    task.content = request.json["content"]
    db.session.commit()
    retDict = {}
    retDict["id"] = task.id
    retDict["title"] = task.title
    retDict["content"] = task.content
    return json.dumps(retDict)

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Note.query.get(id)
    db.session.delete(task)
    db.session.commit()
    retDict = {}
    retDict["id"] = task.id
    retDict["title"] = task.title
    retDict["content"] = task.content
    return json.dumps(retDict)

@app.route("/notes/add", methods=["POST"])
def create_task():
    task = Note(title=request.json["title"], content=request.json["content"])
    db.session.add(task)
    db.session.commit()
    retDict = {}
    retDict["id"] = task.id
    retDict["title"] = task.title
    retDict["content"] = task.content
    return json.dumps(retDict)

with app.app_context():
    db.create_all()

if (__name__ == '__main__'):
    app.run(debug=True)