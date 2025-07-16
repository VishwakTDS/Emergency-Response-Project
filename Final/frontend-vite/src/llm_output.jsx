import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { Link } from 'react-router-dom';
import './llm_output.css'
import Map from './Map'

const prettify = s =>
        s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

function BackButton() {
  return (
    <Link to="/" className="back-btn">
      Back
    </Link>
  );
}

// Simple "i" icon
const InfoIcon = () => (
  <svg
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="none"
  >
    <circle cx="10" cy="10" r="10" fill="#3498db" />
    <text x="10" y="15" textAnchor="middle" fontSize="14" fill="#fff" fontWeight="bold">i</text>
  </svg>
);

const PopupMessage = ({isAlert, message, moreInfo}) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`popup-message ${isAlert ? "red" : "green"}${expanded ? " expanded" : ""}`}>
        <div className="popup-header">
            <span>{message}</span>
            <span
                className="info-icon"
                onClick={() => setExpanded((e) => !e)}
            >
                <InfoIcon />
            </span>
        </div>
        <div className="popup-more-info">
            <div>{moreInfo}</div>
        </div>
    </div>
  );
};

const LLM_Output = ({ causeText, insights, alertText, isLoading, lat, lon }) => {
    console.log("Printing from llm_output.jsx");
    console.log("Pringing lat and longitude inside output.jsx:", lat, lon)
    // console.log("Pringing ints of lat and longitude output.jsx:", intlat, intlon)
    return (
        <div className="llm-response-window">
            <div className="responsebox">
                <div className="back-button">
                    <BackButton /> 
                </div>
                <div className="left-dashboard">
                    <div className="textreply">
                        {causeText && (
                            <div className="agent-response">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>{causeText}</ReactMarkdown>
                            </div>
                        )}

                        <div className="loadingbar">
                            {isLoading && (
                                <Box 
                                sx={{ 
                                    display: 'flex',
                                    justifyContent: "center",
                                    alignItems: "center",
                                    p: 2,
                                    }}
                                    >
                                    <CircularProgress size="3em" />
                                </Box>
                            )}
                        </div>
                    </div>
                </div>

                <div className="right-dashboard">
                    <div className="map-style">
                        <Map lat={lat} long={lon}/>
                    </div>
                    {insights &&
                        <PopupMessage
                            isAlert={!!insights.agency}
                            message={
                                insights?.action && (
                                    <div className="insights-output-action">
                                        <strong>Action:</strong> {prettify(insights.action)}
                                    </div>
                                )
                            }
                            moreInfo={
                                insights?.messages && (
                                    <div className="insights-output-messages">
                                        <strong>Messages:</strong> <ReactMarkdown remarkPlugins={[remarkGfm]}>{insights.messages.join('\n\n')}</ReactMarkdown>
                                    </div>
                                )
                            }
                        />
                    }
                </div>
            </div>
        </div>
    );
};

export default LLM_Output;