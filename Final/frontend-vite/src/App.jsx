import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [responses, setResponses] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setResponses([]);

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

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let result = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        result += decoder.decode(value, { stream: true });
        const lines = result.split("\n\n");
        result = lines.pop();
        lines.forEach(line => {
          console.log("Raw Line:", line);
          if (line) {
            setResponses(prev => [...prev, line]);
          }
        });
      }
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
      {responses.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Server Response:</h3>
          {responses.map((response, index) => (
            <pre key={index}>{response}</pre>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
