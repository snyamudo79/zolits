import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await api.post("/auth/login/", { username, password });
      localStorage.setItem("authToken", res.data.token);
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="centered">
      <form className="card" onSubmit={handleSubmit}>
        <h1>Sign in to ZOLITS</h1>
        {error && <div className="error">{error}</div>}
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit" className="primary">
          Sign in
        </button>
      </form>
    </div>
  );
}

