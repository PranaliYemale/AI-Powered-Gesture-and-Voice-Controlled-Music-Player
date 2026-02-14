from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from backend.models import db, User
import os

app = Flask(__name__)
CORS(app)

# ✅ SAFE DB PATH FOR RENDER
DB_PATH = os.path.join("/tmp", "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- HEALTH ----------------
@app.route("/")
def home():
    return "Backend running 🚀"

@app.route("/api/health")
def health():
    return {"status": "ok"}

# ---------------- AUTH ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email_or_username = data.get("email_or_username")
    password = data.get("password")

    user = User.query.filter(
        (User.email == email_or_username) |
        (User.username == email_or_username)
    ).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.password != password:
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id
    }), 200


@app.route("/api/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out"}), 200


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)