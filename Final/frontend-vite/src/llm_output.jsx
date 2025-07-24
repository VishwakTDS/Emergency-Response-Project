import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { Link } from 'react-router-dom';
import './llm_output.css'
import Map from './Map'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
    faCircleInfo,
    faArrowDownLong,
    faSun,
    faMoon,
    faCloudSun,
    faCloudMoon,
    faCloud,
    faSmog,
    faCloudRain,
    faCloudShowersHeavy,
    faSnowflake,
    faCloudBolt,
 } from '@fortawesome/free-solid-svg-icons';
 import Switch from '@mui/material/Switch';

const prettify = s =>
        s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

function BackButton() {
  return (
    <Link to="/" className="back-btn">
      Back
    </Link>
  );
}

const PopupMessage = ({isAlert, message, moreInfo}) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`popup-message ${isAlert ? "red" : "green"}${expanded ? " expanded" : ""}`}>
        <div className="popup-header">
            <span>{message}</span>
            <FontAwesomeIcon 
                icon={faCircleInfo} 
                className="info-icon"
                onClick={() => setExpanded((e) => !e)}
            />
        </div>
        <div className="popup-more-info">
            <div className="popup-more-info-inner">{moreInfo}</div>
        </div>
    </div>
  );
};

const weatherCodes = {
    0: 'clear',
    1: 'partly-cloudy', 2: 'partly-cloudy', 3: 'cloudy',
    45: 'fog', 48: 'fog',
    51: 'drizzle', 53: 'drizzle', 55: 'drizzle',
    56: 'drizzle', 57: 'drizzle',
    61: 'rain', 63: 'rain', 65: 'rain',
    66: 'rain', 67: 'rain',
    71: 'snow', 73: 'snow', 75: 'snow',
    77: 'snow',
    80: 'rain', 81: 'rain', 82: 'rain',
    85: 'snow', 86: 'snow',
    95:	'thunderstorm',
    96: 'thunderstorm', 99: 'thunderstorm'
};

const LLM_Output = ({ causeText, insights, alertText, weather, isLoading, lat, lon }) => {
    const [isMetric, setIsFarenheit] = useState(false);
    const [weatherIcon,  setWeatherIcon]  = useState("");
    useEffect(() => {
        if (!weather) return;
        let icon = null;

        switch (weatherCodes[weather?.current_weather_code]) {
            case 'clear':
                icon = weather.current_is_day ? faSun : faMoon;
                break;
            case 'partly-cloudy':
                icon = weather.current_is_day ? faCloudSun : faCloudMoon;
                break;
            case 'cloudy':
                icon = faCloud
                break;
            case 'fog':
                icon = faSmog
                break;
            case 'drizzle':
                icon = faCloudRain
                break;
            case 'rain':
                icon = faCloudShowersHeavy
                break;
            case 'snow':
                icon = faSnowflake
                break;
            case 'thunderstorm':
                icon = faCloudBolt
                break;
            default:
                console.warn("Unknown weather code: ", weather?.current_weather_code);
        }

        setWeatherIcon(icon);
    }, [weather])
    
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
                    <div className="top-right">
                        <div className="map-style">
                            <Map lat={lat} long={lon}/>
                        </div>
                        <div className="weather-widget">
                            <FontAwesomeIcon 
                                icon={weatherIcon}
                                className="weather-icon"
                            />

                            <div className={`temperature temp-celsius${isMetric ? "" : " weather-hidden"}`}>
                                {weather?.current_temperature_2m.toFixed(1)} °C
                            </div>

                            <div className={`temperature temp-farenheit${isMetric ? " weather-hidden" : ""}`}>
                                {((weather?.current_temperature_2m * 9) / 5 + 32).toFixed(1)} °F
                            </div>

                            <div className="group">
                                <div className="wind">
                                    <FontAwesomeIcon 
                                        icon={faArrowDownLong} 
                                        className="wind-arrow"
                                        style={{ transform: `rotate(${weather?.current_wind_direction_10m}deg)` }}
                                    />

                                    <div className={`wind-speed-kph${isMetric ? "" : " weather-hidden"}`}>
                                        {weather?.current_wind_speed_10m.toFixed(1)} kph
                                    </div>

                                    <div className={`wind-speed-mph${isMetric ? " weather-hidden" : ""}`}>
                                        {(weather?.current_wind_speed_10m * 0.62137119).toFixed(1)} mph
                                    </div>
                                </div>

                                <div className="humidity">
                                    {weather?.current_relative_humidity_2m.toFixed(1)}%
                                </div>
                            </div>

                            <div className="group">
                                <div className={`precipitation${isMetric ? "" : " weather-hidden"}`}>
                                    {weather?.current_precipitation.toFixed(1)} mm
                                </div>

                                <div className={`precipitation${isMetric ? " weather-hidden" : ""}`}>
                                    {(weather?.current_precipitation / 24.5).toFixed(1)} in
                                </div>

                                <div className={`pressure${isMetric ? "" : " weather-hidden"}`}>
                                    {weather?.current_surface_pressure.toFixed(1)} hPa
                                </div>

                                <div className={`pressure${isMetric ? " weather-hidden" : ""}`}>
                                    {(weather?.current_surface_pressure  * 0.02953).toFixed(1)} Hg
                                </div>
                            </div>

                            <Switch onClick={() => setIsFarenheit((e) => !e)} />
                        </div>
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