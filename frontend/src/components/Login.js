import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email_or_username, setEmailOrUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email_or_username, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.error);
      return;
    }

    localStorage.setItem("user_id", data.user_id);

    // voice start
    fetch("http://127.0.0.1:5000/api/voice/start", {
      method: "POST",
    });

    navigate("/dashboard");
  };

  return (
    <div className="auth-page">

      {/* 👇 MAIN BOX ADDED */}
      <div className="auth-box">

        <h2>Login</h2>

        <input
          placeholder="Email or Username"
          value={email_or_username}
          onChange={(e) => setEmailOrUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <p>
          New user?{" "} 
          <span
            style={{color:"#6c63ff", cursor:"pointer"}}
            onClick={() => navigate("/signup")}
          >
            Sign Up here
          </span>
        </p>

        <button onClick={handleLogin}>Login</button>

      </div>

    </div>
  );
}

export default Login;
