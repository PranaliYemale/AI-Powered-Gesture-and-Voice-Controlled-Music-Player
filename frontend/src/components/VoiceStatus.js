import { useEffect, useState } from "react";

export default function VoiceStatus() {

  const API = process.env.REACT_APP_API_URL || "";

  const [active, setActive] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {

      fetch(`${API}/api/voice_status`)
        .then(res => res.json())
        .then(data => setActive(data.active))
        .catch(() => {});

    }, 1500);

    return () => clearInterval(interval);

  }, [API]);

  return (
    <div style={{
      padding: "12px",
      borderRadius: "8px",
      background: active ? "#e6fffa" : "#f5f5f5",
      border: "1px solid #ccc",
      marginBottom: "10px"
    }}>
      <b>
        🎤 Voice Status:
        <span style={{ color: active ? "green" : "red", marginLeft: 6 }}>
          {active ? "ACTIVE" : "INACTIVE"}
        </span>
      </b>
    </div>
  );
}