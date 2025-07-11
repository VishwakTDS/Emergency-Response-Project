import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { Link } from 'react-router-dom';
import './llm_output.css'

const prettify = s =>
        s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

function BackButton() {
  return (
    <Link to="/" className="back-btn">
      Back
    </Link>
  );
}

const LLM_Output = ({ causeText, insights, alertText, isLoading }) => {
    return (
        <div className="llm-response-window">
            <div className="responsebox">

                <BackButton /> 

                <div className="textreply">
                    {causeText && (
                        <div className="agent-response">
                            <h3 className="agent-name">Cause prediction</h3>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{causeText}</ReactMarkdown>
                        </div>
                    )}

                    {insights && (
                        <div className="agent-response">
                            <h3 className="agent-name">Insights</h3>
                            {insights.action && (
                                <div className="insights-output-action">
                                    <strong>Action:</strong> {prettify(insights.action)}
                                </div>
                            )}
                            {insights.agency && (
                                <div className="insights-output-agency">
                                    <strong>Agency:</strong> {prettify(insights.agency)}
                                </div>
                            )}
                            {(insights.lat != null && insights.lon != null) && (
                                <div className="insights-output-lat-lon">
                                    <strong>Coordinates:</strong> {insights.lat}, {insights.lon}
                                </div>
                            )}
                            {insights.messages && (
                                <div className="insights-output-messages">
                                    <strong>Messages:</strong> <ReactMarkdown remarkPlugins={[remarkGfm]}>{insights.messages.join('\n\n')}</ReactMarkdown>
                                </div>
                            )}
                        </div>
                    )}

                    {alertText && (
                        <div className="agent-response">
                            <h3 className="agent-name">Alert</h3>
                            <div className="alert-output-responder">
                                <strong>Responder: </strong>
                                <span>
                                    {alertText.alerts.map(alert => (
                                    prettify(alert.responder)
                                    )).join(', ')}
                                </span>
                            </div>
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
        </div>
    );
};

export default LLM_Output;