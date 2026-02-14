from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.models import db, User, Song
from backend.spotify_control import SpotifyController
from backend.voice_control import start_voice, stop_voice
import os

# ---------------- DATABASE ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
FRONTEND_BUILD = os.path.join(BASE_DIR, "..", "frontend", "build")

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_BUILD, "static"),
    template_folder=FRONTEND_BUILD
)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- MUSIC FOLDER ----------------
MUSIC_FOLDER = os.path.join(BASE_DIR, "music")
os.makedirs(MUSIC_FOLDER, exist_ok=True)

local_songs = [
    os.path.join(MUSIC_FOLDER, f)
    for f in os.listdir(MUSIC_FOLDER)
    if f.endswith(".mp3")
]

# ---------------- SPOTIFY ----------------
spotify_ctrl = SpotifyController(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

# ---------------- PLAYER ----------------
class DummyPlayer:
    def __init__(self, local_songs=None):
        self.local_songs = local_songs or []
        self.current_index = 0
        self.volume = 50

    def play(self):
        return "playing"

    def pause(self):
        return "paused"

    def next_song(self):
        if self.local_songs:
            self.current_index = (self.current_index + 1) % len(self.local_songs)

    def prev_song(self):
        if self.local_songs:
            self.current_index = (self.current_index - 1) % len(self.local_songs)

    def volume_up(self):
        self.volume = min(100, self.volume + 10)

    def volume_down(self):
        self.volume = max(0, self.volume - 10)

player = DummyPlayer(local_songs)

player_state = {
    "status": "stopped",
    "volume": 50,
}

voice_status = {"active": False}
gesture_status = {"active": False}

# ---------------- REACT SERVE ----------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.template_folder, "index.html")

# ---------------- PLAYER ----------------
@app.route("/api/play", methods=["POST"])
def play():
    player_state["status"] = player.play()
    return jsonify(player_state)

@app.route("/api/pause", methods=["POST"])
def pause():
    player_state["status"] = player.pause()
    return jsonify(player_state)

@app.route("/api/next", methods=["POST"])
def next_song():
    player.next_song()
    return jsonify({"index": player.current_index})

@app.route("/api/prev", methods=["POST"])
def prev_song():
    player.prev_song()
    return jsonify({"index": player.current_index})

@app.route("/api/volume_up", methods=["POST"])
def volume_up():
    player.volume_up()
    player_state["volume"] = player.volume
    return jsonify(player_state)

@app.route("/api/volume_down", methods=["POST"])
def volume_down():
    player.volume_down()
    player_state["volume"] = player.volume
    return jsonify(player_state)

# ---------------- SONG LIST ----------------
@app.route("/api/songs", methods=["GET"])
def get_local_songs():
    files = os.listdir(MUSIC_FOLDER)
    songs = [f for f in files if f.endswith(".mp3")]
    return jsonify({"songs": songs})

# ---------------- AUTH ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"], password=data["password"])
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

    if not user or user.password != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"token": str(user.id)})

# ---------------- VOICE ----------------
@app.route("/api/voice/start", methods=["POST"])
def voice_start_route():
    start_voice()
    voice_status["active"] = True
    return {"status": "voice started"}

@app.route("/api/voice/stop", methods=["POST"])
def voice_stop_route():
    stop_voice()
    voice_status["active"] = False
    return {"status": "voice stopped"}

@app.route("/api/voice_status")
def get_voice_status():
    return voice_status

# ---------------- GESTURE ----------------
@app.route("/api/gesture/start", methods=["POST"])
def start_gesture():
    gesture_status["active"] = True
    return {"status": "gesture started"}

@app.route("/api/gesture/stop", methods=["POST"])
def stop_gesture():
    gesture_status["active"] = False
    return {"status": "gesture stopped"}

@app.route("/api/gesture_status")
def get_gesture_status():
    return gesture_status

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)