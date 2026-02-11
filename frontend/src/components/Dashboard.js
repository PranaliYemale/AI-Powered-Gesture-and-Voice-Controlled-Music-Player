import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import VoiceStatus from "./VoiceStatus";
import VoiceHelp from "./VoiceHelp";
import GestureControl from "./GestureControl";

function Dashboard() {
  const [mode, setMode] = useState("local");
  const [status, setStatus] = useState("Stopped");
  const [songs, setSongs] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [backendState, setBackendState] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (mode === "local") {
      fetch("/api/songs")
        .then((res) => res.json())
        .then((data) => setSongs(data.songs || []));
    }
  }, [mode]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("/api/state")
        .then(res => res.json())
        .then(data => {
          setBackendState(data);
          setCurrentIndex(data.current_index);
          setStatus(data.status);
          setMode(data.mode);
        })
        .catch(() => {});
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const playSelectedSong = (index) => {
    fetch("/api/play_index", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ index })
    });
  };

  const btn = (name, api, red=false) => (
    <button
      className={`btn ${red ? "btn-red":""}`}
      onClick={() => fetch(api, {method:"POST"})}
    >
      {name}
    </button>
  );

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div style={{padding:20, position:"relative"}}>

      <div style={{position: "absolute", top: 20, right: 20}}>
        <button className="btn btn-red" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <h1>🎧 Smart Music Player</h1>

      <VoiceStatus/>

      <div className="glass">

        <div>
          <b>Mode:</b> {mode.toUpperCase()}
          <div>
            <button className="btn" onClick={()=>setMode("local")}>
              Local
            </button>

            <button
              className="btn"
              onClick={() =>
                window.location.href="https://your-backend-url/api/spotify/login"
              }
            >
              Spotify
            </button>
          </div>
        </div>

        <div style={{marginTop:10}}>
          <b>Status:</b> {status}
        </div>

        <div style={{marginTop:15}}>
          {btn("▶ Play","/api/play")}
          {btn("⏸ Pause","/api/pause")}
          {btn("⏭ Next","/api/next")}
          {btn("⏮ Prev","/api/prev")}
          {btn("🔊 Vol+","/api/volume_up")}
          {btn("🔉 Vol-","/api/volume_down")}
          {btn("👍 Like","/api/like")}
          {btn("👎 Dislike","/api/dislike")}
        </div>

        {/* 👇 GESTURE CAMERA HERE */}
        <div style={{ marginTop: 25 }}>
          <h3>🖐 Gesture Control</h3>
          <GestureControl />
        </div>

      </div>

      {mode === "local" && (
        <div className="glass" style={{ marginTop: 15 }}>
          <h3>Local Songs</h3>
          <select
            value={currentIndex}
            onChange={(e) => playSelectedSong(Number(e.target.value))}
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "10px",
              background: "#111",
              color: "white",
              border: "1px solid #444"
            }}
          >
            {songs.map((s, i) => (
              <option key={i} value={i}>
                {i === currentIndex ? "▶ " : ""} {s}
              </option>
            ))}
          </select>
        </div>
      )}

      <VoiceHelp/>
    </div>
  );
}

export default Dashboard;
