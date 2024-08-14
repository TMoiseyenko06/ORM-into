from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from flask import request, jsonify

# Task 1:

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:Czmpdrdv123!@localhost/fitness_center_db"
)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)


class WorkoutSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(255), nullable=False)


class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta:
        fields = ("name", "age")


class SessionSchema(ma.Schema):
    member_id = fields.Integer(required=True)
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("member_id", "date", "time", "activity")


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

with app.app_context():
    db.create_all()

# Task 2: CRUD for members


@app.route("/members", methods=["GET"])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)


@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"error": f"{e}"}), 400

    new_member = Member(name=member_data["name"], age=member_data["age"])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "member added"}), 201


@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"error": f"{e}"}), 400

    member = Member.query.get_or_404(id)
    member.name = member_data["name"]
    member.age = member_data["age"]
    db.session.commit()
    return jsonify({"message": "member updated"}), 200


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "member deleted"})


# Task 3: workout session CRUD
@app.route("/sessions/member/<int:id>", methods=["GET"])
def get_session_from_member(id):
    sessions = WorkoutSessions.query.filter_by(member_id=id).all()
    return sessions_schema.jsonify(sessions)


@app.route("/sessions", methods=["POST"])
def add_session():
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"error": f"{e}"}), 400

    new_session = WorkoutSessions(
        member_id=session_data["member_id"],
        session_date=session_data["date"],
        session_time=session_data["time"],
        activity=session_data["activity"],
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"message": "session added"}), 201

@app.route('/sessions/<int:id>',methods=["DELETE"])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message":"member deleted"})