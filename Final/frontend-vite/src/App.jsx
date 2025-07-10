import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function App() {
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");

  const [causeText,  setCauseText]  = useState("");
  const [insights,   setInsights]   = useState(null);
  const [alertText,  setAlertText]  = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setCauseText(""); setInsights(null); setAlertText(null);

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

      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        let nl;
        while ((nl = buffer.indexOf("\n")) !== -1) {
          const line = buffer.slice(0, nl).trim();
          buffer = buffer.slice(nl + 1);

          if (!line) continue;

          let obj;
          try        { obj = JSON.parse(line); } 
          catch (e)  { console.error("Bad JSON line:", line); continue; }

          switch (obj.type) {
            case "cause_prediction":
              setCauseText(prev => prev + obj.data);
              break;
            case "insights":
              setInsights(obj.data);
              break;
            case "alert":
              setAlertText(obj.data);
              break;
            default:
              console.warn("Unknown chunk type:", obj.type);
          }
        }
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
      {causeText && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Cause prediction</h3>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{causeText}</ReactMarkdown>
        </div>
      )}

      {insights && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Insights</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {JSON.stringify(insights, null, 2)}
          </pre>
        </div>
      )}

      {alertText && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Alert</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {JSON.stringify(alertText, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
