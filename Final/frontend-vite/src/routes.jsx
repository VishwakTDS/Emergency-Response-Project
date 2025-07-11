import { useState } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import App from "./App";
import LLM_Output from "./llm_output";

function Routing() {
    const [causeText,  setCauseText]  = useState("");
    const [insights,   setInsights]   = useState(null);
    const [alertText,  setAlertText]  = useState(null);

    const [isLoading, setIsLoading] = useState(false);

    return (
        <Router>
            <Routes>
                <Route 
                    path="/" 
                    element={
                        <App
                            setCauseText={setCauseText}
                            setInsights={setInsights}
                            setAlertText={setAlertText}
                            setIsLoading={setIsLoading} 
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
                            isLoading={isLoading}
                        />
                    } 
                />
            </Routes>
        </Router>
    );
}

export default Routing;