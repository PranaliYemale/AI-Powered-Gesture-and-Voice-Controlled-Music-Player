import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup({ setUserId }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const res = await fetch("api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        alert("Signup failed: " + errorData.error);
        return;
      }

      const data = await res.json();
      console.log("Signup success:", data);

      alert("Signup successful! Please login.");
      navigate("/login");

    } catch (err) {
      console.error("Error connecting to backend:", err);
      alert("Backend server not reachable!");
    }
  };

  return (
  <div className="auth-page">

    <div className="auth-box">

      <h2>Signup</h2>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <p>
        Already have an account?
        <span
          style={{ color: "#6c63ff", cursor: "pointer" }}
          onClick={() => navigate("/login")}
        >
          Login here
        </span>
      </p>

      <button onClick={handleSignup}>Signup</button>

    </div>
  </div>
);

}

export default Signup;
