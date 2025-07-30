import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './App.css'
import GlobeComponent from './GlobeComponent';
import FuturisticGlobe from './FuturisticGlobe';
import HyperspeedBackground from './HyperspeedBackground';
import Map from './Map'

function App({setCauseText, setInsights, setAlertText, setWeather, setIsLoading, setFile, setLat, setLon, file, lat, lon}) {
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
    <div
      style={{
        width: '100vw',
        height: '100vh',
        overflow: 'hidden',
        position: 'relative',
        margin: 0,
        padding: 0,
        boxSizing: 'border-box',
        // Remove any minHeight or minWidth!
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
        <div
          style={{
            position: 'absolute',
            bottom: 10,
            left: 80,
            height: '100vh',
            zIndex: 10,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',   // <-- vertical centering
            alignItems: 'flex-start',   // <-- keep left-aligned
            gap: 24,
            background: 'none',
            boxShadow: 'none',
            padding: 0
          }}
        >
          <h2
            style={{
              color: '#f5e9d7',
              fontWeight: 700,
              fontSize: '2.2rem',
              marginBottom: 24,
              letterSpacing: '0.01em',
              lineHeight: 1.1
            }}
          >
            Emergency Incident<br />Upload
          </h2>
          <label style={{ color: '#f5e9d7', fontSize: '1.1rem', marginBottom: 8 }}>
            <input
              type="file"
              style={{
                background: 'none',
                color: '#f5e9d7',
                border: 'none',
                fontSize: '1rem',
                marginBottom: 4 // much smaller space
              }}
            />
          </label>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', width: 220 }}>
  {/* Latitude */}
  <label
    htmlFor="latitude"
    style={{
      color: '#f5e9d7',
      fontSize: '1.1rem',
      marginBottom: 4,
      marginTop: 4, // much smaller space
      fontWeight: 500,
      letterSpacing: '0.01em'
    }}
  >
    Latitude
  </label>
  <input
    id="latitude"
    type="text"
    value={lat}
    onChange={e => setLat(e.target.value)}
    placeholder="****"
    style={{
      background: 'rgba(0, 0, 0, 0.35)',
      border: 'none',
      borderBottom: '2px solid #f5e9d7',
      color: '#f5e9d7',
      fontSize: '1.2rem',
      marginBottom: 16,
      outline: 'none',
      width: '100%',
      padding: '4px 0'
    }}
  />

  {/* Longitude */}
  <label
    htmlFor="longitude"
    style={{
      color: '#f5e9d7',
      fontSize: '1.1rem',
      marginBottom: 4,
      marginTop: 8,
      fontWeight: 500,
      letterSpacing: '0.01em'
    }}
  >
    Longitude
  </label>
  <input
    id="longitude"
    type="text"
    value={lon}
    onChange={e => setLon(e.target.value)}
    placeholder="****"
    style={{
      background: 'rgba(0, 0, 0, 0.36)',
      border: 'none',
      borderBottom: '2px solid #f5e9d7',
      color: '#f5e9d7',
      fontSize: '1.2rem',
      marginBottom: 24,
      outline: 'none',
      width: '100%',
      padding: '4px 0'
    }}
  />
</div>
          <button
            style={{
              background: 'rgba(0,0,0,0.6)',
              color: '#f5e9d7',
              border: '1px solid #f5e9d7',
              borderRadius: 24,
              padding: '10px 32px',
              fontSize: '1.1rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'background 0.2s'
            }}
          >
            Submit
          </button>
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
        
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            zIndex: 1, // Make sure this is below your form if needed 
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <FuturisticGlobe lat={lat} lon={lon} />
        </div>
      </div>
      <HyperspeedBackground />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: '50%',
          transform: 'translateX(-50%)',
          color: 'white',
          fontSize: '3rem',
          fontWeight: 800,
          letterSpacing: '0.04em',
          zIndex: 2,
          textShadow: '0 4px 32px #0ea5e9, 0 2px 8px #000'
        }}
      >
      </div>
    </div>
  );
}
export default App;

