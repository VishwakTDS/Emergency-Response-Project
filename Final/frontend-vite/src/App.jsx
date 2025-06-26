import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file || !lat || !lon) {
      alert("Please fill out all fields.");
      return;
    }

    const formData = new FormData();
    formData.append("input_media", file, file.name);
    formData.append("latitude", lat);
    formData.append("longitude", lon);

    try {
      const res = await fetch("http://127.0.0.1:5000/response/v1", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();
      setResponse(result);
      console.log(result);
    } catch (err) {
      console.error("Error submitting form", err);
      setResponse({ error: "Submission failed." });

    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "500px", margin: "auto" }}>
      <h2>Emergency Incident Upload</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <br /><br />
        <input
          type="text"
          placeholder="Latitude"
          value={lat}
          onChange={(e) => setLat(e.target.value)}
        />
        <br /><br />
        <input
          type="text"
          placeholder="Longitude"
          value={lon}
          onChange={(e) => setLon(e.target.value)}
        />
        <br /><br />
        <button type="submit">Submit</button>
      </form>
      {response && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Server Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
