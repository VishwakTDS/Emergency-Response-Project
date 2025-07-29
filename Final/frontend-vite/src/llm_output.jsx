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
    faArrowsRotate,
} from '@fortawesome/free-solid-svg-icons';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
 import {
  WiDaySunny,
  WiNightClear,
  WiCloudy,
  WiFog,
  WiSprinkle,
  WiSleet,
  WiRain,
  WiRainMix,
  WiShowers,
  WiSnow,
  WiSnowflakeCold,
  WiThunderstorm,
  WiHail,
  WiStrongWind
} from "react-icons/wi";

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

const weatherCodeToIcon = (code, isDay) => {
    code = Number(code);

    if (code === 0)                 return isDay ? <WiDaySunny /> : <WiNightClear />;         // clear
    if ([1, 2, 3].includes(code))   return <WiCloudy />;                                      // mainly clear / cloudy
    if ([45, 48].includes(code))    return <WiFog />;                                         // fog
    if ([51, 53, 55].includes(code))return <WiSprinkle />;                                    // drizzle
    if ([56, 57].includes(code))    return <WiSleet />;                                       // freezing drizzle
    if ([61, 63, 65].includes(code))return <WiRain />;                                        // rain
    if ([66, 67].includes(code))    return <WiRainMix />;                                     // freezing rain
    if ([71, 73, 75].includes(code))return <WiSnow />;                                        // snow
    if (code === 77)                return <WiSnowflakeCold />;                               // snow grains
    if ([80, 81, 82].includes(code))return <WiShowers />;                                     // rain showers
    if ([85, 86].includes(code))    return <WiSnow />;                                        // snow showers
    if (code === 95)                return <WiThunderstorm />;                                // thunderstorm
    if ([96, 99].includes(code))    return <WiHail />;                                        // thunderstorm + hail
    return <WiStrongWind />;                                                                  // fallback
};

const LLM_Output = ({ causeText, insights, alertText, weather, isLoading, file, lat, lon }) => {
    const [isMetric, setIsMetric] = useState(false);
    const [weatherIcon,  setWeatherIcon]  = useState("");
    
    return (
        <div className="dashboard">
            <header>
                <div className="back-button">
                    <BackButton /> 
                </div>
                <h1>Emergency Response Dashboard</h1>
            </header>

            <main className="grid">
                <div className="top">
                    <section className="card weather-card">
                        {weather && (
                            <>
                                <div className="weather-main">
                                    <div className="weather-icon">
                                        {weatherCodeToIcon(
                                            weather.current_weather_code,
                                            weather.current_is_day
                                        )}
                                    </div>
                                    <div className={`weather-temp temp-celsius${isMetric ? "" : " weather-hidden"}`}>
                                        {weather?.current_temperature_2m.toFixed(1)} °C
                                    </div>

                                    <div className={`weather-temp temp-farenheit${isMetric ? " weather-hidden" : ""}`}>
                                        {((weather?.current_temperature_2m * 9) / 5 + 32).toFixed(1)} °F
                                    </div>
                                </div>

                                <div className="weather-details">
                                    <div className="feels-like">
                                        Feels Like
                                        <div className={`feels-like-celsius${isMetric ? "" : " weather-hidden"}`}>
                                            {weather?.current_apparent_temperature.toFixed(1)} °C
                                        </div>

                                        <div className={`feels-like-farenheit${isMetric ? " weather-hidden" : ""}`}>
                                            {((weather?.current_apparent_temperature * 9) / 5 + 32).toFixed(1)} °F
                                        </div>
                                    </div>

                                    <div className="wind">
                                        Wind
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
                                        Humidity
                                        {weather?.current_relative_humidity_2m.toFixed(1)}%
                                    </div>
                                    
                                    <div className="precipitation">
                                        Precipitation
                                        <div className={`precipitation-mm${isMetric ? "" : " weather-hidden"}`}>
                                            {weather?.current_precipitation.toFixed(1)} mm
                                        </div>

                                        <div className={`precipitation-in${isMetric ? " weather-hidden" : ""}`}>
                                            {(weather?.current_precipitation / 24.5).toFixed(1)} in
                                        </div>
                                    </div>

                                    <div className="pressure">
                                        Pressure
                                        <div className={`pressure-hPa${isMetric ? "" : " weather-hidden"}`}>
                                            {weather?.current_pressure_msl .toFixed(1)} hPa
                                        </div>

                                        <div className={`pressure-Hg${isMetric ? " weather-hidden" : ""}`}>
                                            {(weather?.current_pressure_msl   * 0.02953).toFixed(1)} Hg
                                        </div>
                                    </div>

                                    <button
                                        className="unit-toggle"
                                        onClick={() => setIsMetric(e => !e)}
                                        title="Switch units"
                                    >
                                        <FontAwesomeIcon icon={faArrowsRotate} /> {isMetric ? "Imperial" : "Metric"}
                                    </button>
                                </div>
                            </>
                        )}
                    </section>

                    <section className="card map-card">
                        <Map 
                            className="map-style" 
                            lat={lat} long={lon}
                        />
                    </section>

                    <section className="card image-card">
                            {file && <img src={URL.createObjectURL(file)} alt="preview" />}
                    </section>
                </div>

                <div className="bottom">
                    {isLoading ? (
                        <div className="loadingbar">
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
                        </div>
                    ) : (
                        <>
                            {causeText && (
                                <section className="card cause-prediction-card">
                                    <div className="agent-response">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{causeText}</ReactMarkdown>
                                    </div>
                                </section>
                            )}

                            {insights &&
                                <section className="card insights-card">
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
                                </section>
                            }
                            
                            {alertText &&
                                <section className="card alert-card">
                                    <strong>Responder: </strong>
                                    <span>
                                        {alertText.alerts.map(alert => (
                                        prettify(alert.responder)
                                        )).join(', ')}
                                    </span>
                                </section>
                            }
                        </>
                    )}
                </div>
            </main>
        </div>
    );
};

export default LLM_Output;