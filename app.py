from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    def __repr__(self):
        return '<Note %r>' % self.id


@app.route('/')
def index():
    return 'Hello World!'

@app.route("/tasks/all", methods=["GET"])
def get_all_tasks():
    tasks = Note.query.all()
    return jsonify(tasks)

@app.route("/tasks/<int:id>", methods=["UPDATE"])
def update_task(id):
    task = Note.query.get(id)
    task.title = request.json["title"]
    task.content = request.json["content"]
    db.session.commit()
    return jsonify(task)

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Note.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(task)

@app.route("/tasks", methods=["POST"])
def create_task():
    task = Note(title=request.json["title"], content=request.json["content"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task)

if (__name__ == '__main__'):
    app.run(debug=True)
    db.init_app(app)