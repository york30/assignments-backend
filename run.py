from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.app_context().push()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Wisesteward_5@localhost/db_to_do_list'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ugdrrcd7nbs8tkg9:HWj1DY5Q6QiJH6Y1VycK@bh3uua6gyywscmxtewnp-mysql.services.clever-cloud.com:3306/bh3uua6gyywscmxtewnp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# We are going to create the classes of ORM ### They are also called models

class To_do_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id INT PRIMARY KEY
    description = db.Column(db.String(200), nullable=False)  # description VARCHAR(200) NOT NULL
    stage = db.Column(db.String(100), nullable=False)

    def __init__(self, description, stage):
        self.description = description
        self.stage = stage

db.create_all()

###  Schemas ###
ma = Marshmallow(app)


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'stage')


# We transform the class into a table : Migration
db.create_all()
print("It has just been created the table inside the database")


@app.route('/')
def index():
    context = {
        'status': True,
        'content': 'Active Server'
    }
    return jsonify(context)


@app.route('/task', methods=['POST'])
def setTask():
    description = request.json['description']
    stage = request.json['stage']

    newTask = To_do_list(description, stage)
    db.session.add(newTask)
    db.session.commit()

    data_schema = TaskSchema()

    context = {
        'status': True,
        'content': data_schema.dump(newTask)
    }

    return jsonify(context)


@app.route('/task', methods=['GET'])
def getTask():
    data = To_do_list.query.all()  # select * from task
    print(data)

    data_schema = TaskSchema(many=True)

    context = {
        'status': True,
        'content': data_schema.dump(data)
    }
    return jsonify(context)


# app.run(debug=True)
