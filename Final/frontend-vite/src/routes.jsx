import { useState } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import App from "./App";
import LLM_Output from "./llm_output";
import Home from "./Home";

function Routing() {
    // const [causeText,  setCauseText]  = useState("");
    const [causeText,  setCauseText]  = useState(null);
    const [insights,   setInsights]   = useState(null);
    const [alertText,  setAlertText]  = useState(null);
    const [weather,  setWeather]  = useState(null);

    const [isLoading, setIsLoading] = useState(false);

    const [file, setFile] = useState(null);
    const [lat, setLat] = useState("");
    const [lon, setLon] = useState("");

    return (
        <Router>
            <Routes>
                <Route 
                    path="/" 
                    element={<Home />} 
                />
                <Route 
                    path="/globe" 
                    element={
                        <App
                            setCauseText={setCauseText}
                            setInsights={setInsights}
                            setAlertText={setAlertText}
                            setWeather={setWeather}
                            setIsLoading={setIsLoading}
                            setFile={setFile}
                            setLat={setLat}
                            setLon={setLon}
                            file={file}
                            lat={lat}
                            lon={lon}
                        />
                    } 
                />
                <Route 
                    path="/output" 
                    element={
                        <LLM_Output 
                            causeText={causeText}
                            insights={insights}
                            alertText={alertText}
                            weather={weather}
                            isLoading={isLoading}
                            file={file}
                            lat={lat}
                            lon={lon}
                        />
                    } 
                />
            </Routes>
        </Router>
    );
}

export default Routing;
