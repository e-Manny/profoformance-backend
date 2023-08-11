from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from config import ApplicationConfig
from models import db, User

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
  db.create_all()

@app.route("/@me")
def get_current_user():
  user_id = session.get("user_id")

  if not user_id:
    return jsonify({"error":"Unauthorized"}), 401
  
  user = User.query.filter_by(id=user_id).first()

  return jsonify({
     "id": user.id,
     "email": user.email
  })

@app.route("/register", methods=["POST"])
def register_user():
  email = request.json["email"]
  password = request.json["password"]

  user_exists = User.query.filter_by(email = email).first() is not None
  if user_exists:
    return jsonify({"error": "User already exists"}), 409

  hashed_password = bcrypt.generate_password_hash(password)
  new_user = User(email=email, password=hashed_password)
  db.session.add(new_user)
  db.session.commit()
  return jsonify({
     "id": new_user.id,
     "email": new_user.email
  })

@app.route("/login", methods=["POST"])
def login_user():
  email = request.json["email"]
  password = request.json["password"]

  user = User.query.filter_by(email = email).first()
  if user is None:
    return jsonify({"error":"no username exists"}), 401
  if not bcrypt.check_password_hash(user.password, password):
    return jsonify({"error":"wrong password"}), 401
  session["user_id"] = user.id
  print(session)
  return jsonify({
     "id": user.id,
     "email": user.email
  }), 200

@app.route("/logout", methods=["POST"])
def logout_user():
    if "user_id" in session:
        session.pop("user_id")
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": "Not logged in"}), 401

if __name__ == "__main__":
    app.run(debug=True)