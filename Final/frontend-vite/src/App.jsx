import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function App() {
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [responses, setResponses] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setResponses("");

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
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setResponses(prev => prev + chunk);
      }
    } catch (err) {
      console.error("Error submitting form", err);
      setResponses("**Submission failed.**");
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
      {responses && (
        <div style={{ marginTop: "2rem" }}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {responses}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;
