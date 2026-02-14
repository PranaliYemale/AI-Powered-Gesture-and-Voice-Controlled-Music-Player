from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.models import db, User
from backend.voice_control import start_voice, stop_voice
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ---------------- DATABASE ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- MUSIC FOLDER ----------------
MUSIC_FOLDER = os.path.join(BASE_DIR, "music")
os.makedirs(MUSIC_FOLDER, exist_ok=True)

local_songs = [
    f for f in os.listdir(MUSIC_FOLDER)
    if f.endswith(".mp3") or f.endswith(".wav")
]

# ---------------- PLAYER ----------------
class DummyPlayer:
    def __init__(self, songs=None):
        self.songs = songs or []
        self.current_index = 0
        self.volume = 50
        self.status = "stopped"

    def play(self):
        self.status = "playing"

    def pause(self):
        self.status = "paused"

    def next_song(self):
        if self.songs:
            self.current_index = (self.current_index + 1) % len(self.songs)

    def prev_song(self):
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)

    def volume_up(self):
        self.volume = min(100, self.volume + 10)

    def volume_down(self):
        self.volume = max(0, self.volume - 10)

player = DummyPlayer(local_songs)

# ---------------- STATE ----------------
voice_status = {"active": False}
gesture_status = {"active": False}

# ---------------- PLAYER CONTROLS ----------------
@app.route("/api/play", methods=["POST"])
def play():
    player.play()
    return jsonify({"status": player.status})

@app.route("/api/pause", methods=["POST"])
def pause():
    player.pause()
    return jsonify({"status": player.status})

@app.route("/api/next", methods=["POST"])
def next_song():
    player.next_song()
    return jsonify({"current_index": player.current_index})

@app.route("/api/prev", methods=["POST"])
def prev_song():
    player.prev_song()
    return jsonify({"current_index": player.current_index})

@app.route("/api/volume_up", methods=["POST"])
def volume_up():
    player.volume_up()
    return jsonify({"volume": player.volume})

@app.route("/api/volume_down", methods=["POST"])
def volume_down():
    player.volume_down()
    return jsonify({"volume": player.volume})

# ---------------- STATE ROUTE ----------------
@app.route("/api/state")
def get_state():
    return jsonify({
        "mode": "local",
        "status": player.status,
        "current_index": player.current_index,
        "voice": voice_status["active"],
        "gesture": gesture_status["active"]
    })

# ---------------- SONG LIST ----------------
@app.route("/api/songs", methods=["GET"])
def get_songs():
    return jsonify({"songs": local_songs})

# ---------------- AUTH ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if User.query.filter(
        (User.email == data["email"]) |
        (User.username == data["username"])
    ).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter(
        (User.email == data["email_or_username"]) |
        (User.username == data["email_or_username"])
    ).first()

    if not user:
        return jsonify({"error": "User not found"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id
    })

# ---------------- VOICE ----------------
@app.route("/api/voice/start", methods=["POST"])
def voice_start():
    start_voice()
    voice_status["active"] = True
    return {"status": "voice started"}

@app.route("/api/voice/stop", methods=["POST"])
def voice_stop():
    stop_voice()
    voice_status["active"] = False
    return {"status": "voice stopped"}

@app.route("/api/voice_status")
def voice_status_route():
    return jsonify(voice_status)

# ---------------- GESTURE ----------------
@app.route("/api/gesture/start", methods=["POST"])
def gesture_start():
    gesture_status["active"] = True
    return {"status": "gesture started"}

@app.route("/api/gesture/stop", methods=["POST"])
def gesture_stop():
    gesture_status["active"] = False
    return {"status": "gesture stopped"}

@app.route("/api/gesture_status")
def gesture_status_route():
    return jsonify(gesture_status)

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)