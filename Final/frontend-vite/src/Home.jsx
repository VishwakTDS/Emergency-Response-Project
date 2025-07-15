import React from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  return (
    <div style={{ height: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <button
        style={{ fontSize: "2rem", padding: "1rem 2rem", cursor: "pointer" }}
        onClick={() => navigate("/upload")}
      >
        Click here
      </button>
    </div>
  );
}