import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './App.css'
import Map from './Map'


function App({setCauseText, setInsights, setAlertText, setWeather, setIsLoading, setLat, setLon, lat, lon}) {
  const [file, setFile] = useState(null);
  // const [lat, setLat] = useState("");
  // const [lon, setLon] = useState("");

  
  const navigate = useNavigate();

  // let newLat = 33.338;
  // let newLon = -111.895;

  const handleSubmit = async (e) => {
    e.preventDefault();

    setCauseText(""); setInsights(null); setAlertText(null);

    if (!file || !lat || !lon) {
      alert("Please fill out all fields.");
      return;
    }

    navigate("/output");

    const formData = new FormData();
    formData.append("input_media", file, file.name);
    formData.append("latitude", lat);
    formData.append("longitude", lon);


    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/response/v1", {
        method: "POST",
        body: formData,
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = "";
      let gotFirstChunk = false;

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
              if (!gotFirstChunk) {
                gotFirstChunk = true;
                setIsLoading(false);
              }
              setCauseText(prev => prev + obj.data);
              break;
            case "insights":
              setInsights(obj.data);
              break;
            case "alert":
              setAlertText(obj.data);
              break;
            case "weather":
              setWeather(obj.data);
            default:
              console.warn("Unknown chunk type:", obj.type);
          }
        }
      }
    } catch (err) {
      console.error("Error submitting form", err);
      setIsLoading(false);
    }
  };
// style={{ padding: "2rem", maxWidth: "500px", margin: "auto" }}
  return (
    <>
      <div className="parentdiv">

        <div className="inputform-map">

          <div className="onlyform">
            <h2>Emergency Incident Upload</h2>
            <form onSubmit={handleSubmit}>
              <label htmlFor="formId">
                <input id="formId" type="file" onChange={(e) => setFile(e.target.files[0])} />
              </label>
              <br /><br />
              <input
                type="text"
                placeholder="Latitude"
                className="input-field"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
              />
              <br /><br />
              <input
                type="text"
                placeholder="Longitude"
                className="input-field"
                value={lon}
                onChange={(e) => setLon(e.target.value)}
              />
              <br /><br />
              <button type="submit" className="submit-button">Submit</button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
