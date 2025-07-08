import React, { useState } from "react";
import IncidentUploadForm from "./components/IncidentUploadForm";
import MapView from "./components/MapView";

function App() {
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [response, setResponse] = useState(null);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  // Validation helpers
  const isValidLat = (value) => !isNaN(value) && value >= -90 && value <= 90;
  const isValidLon = (value) => !isNaN(value) && value >= -180 && value <= 180;

  // Real-time validation
  React.useEffect(() => {
    const newErrors = {};
    if (lat && !isValidLat(Number(lat))) newErrors.lat = "Latitude must be between -90 and 90.";
    if (lon && !isValidLon(Number(lon))) newErrors.lon = "Longitude must be between -180 and 180.";
    setErrors((prev) => ({ ...prev, ...newErrors }));
  }, [lat, lon]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};
    if (!file) newErrors.file = "File is required.";
    if (!lat) newErrors.lat = "Latitude is required.";
    else if (!isValidLat(Number(lat))) newErrors.lat = "Latitude must be between -90 and 90.";
    if (!lon) newErrors.lon = "Longitude is required.";
    else if (!isValidLon(Number(lon))) newErrors.lon = "Longitude must be between -180 and 180.";
    setErrors(newErrors);
    if (Object.keys(newErrors).length > 0) return;
    setLoading(true);
    setResponse(null);
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
    } catch (err) {
      setResponse({ error: "Submission failed." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-4">
      <IncidentUploadForm
        file={file}
        lat={lat}
        lon={lon}
        setFile={setFile}
        setLat={setLat}
        setLon={setLon}
        handleSubmit={handleSubmit}
        response={response}
        errors={errors}
        loading={loading}
      />
      <MapView lat={lat} long={lon} />
    </div>
  );
}

export default App;
