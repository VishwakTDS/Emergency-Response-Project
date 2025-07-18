import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './App.css'
import Spline from '@splinetool/react-spline';
import GlobeComponent from './GlobeComponent';
import FuturisticGlobe from './FuturisticGlobe';

function App({setCauseText, setInsights, setAlertText, setIsLoading}) {
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");

  
  const navigate = useNavigate();

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
          
          if (!gotFirstChunk) {
            gotFirstChunk = true;
            setIsLoading(false);
          }

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
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '400px 1fr', // adjust 400px as needed for your form
        height: '200vh', //  here to change length of the page 
        width: '100vw',
        background: 'rgb(0, 0, 0)',
        margin: 0,
        padding: 0,
        boxSizing: 'border-box'
      }}
    >
      {/* Left panel */}
      <div
        style={{
          position: 'relative',
          zIndex: 10, // <-- Make sure this is higher than the globe
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh'
        }}
      >
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
            <div className="map-style">
              {/* <Map newlat={lat} newlon={lon}/> */}
            </div>
          </div>
        </div>
      </div>
      {/* Right panel */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          zIndex: 1,
          justifyContent: 'center',
          height: '120vh'
        }}
      >
        <div style={{ width: 1000, height: 1000 }}>
          <FuturisticGlobe lat={lat} lon={lon} />
        </div> 
      </div>
    </div>
  );
}
export default App;

