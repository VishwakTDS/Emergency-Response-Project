import React from 'react';
import { useNavigate } from 'react-router-dom';
import './components/Hyperspeed/Hyperspeed.css';
import Hyperspeed from './components/Hyperspeed/Hyperspeed';
import { hyperspeedPresets } from './components/Hyperspeed/HyperSpeedPresets';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        height: '100vh',
        width: '100vw',
        position: 'relative',
        overflow: 'hidden',
        backgroundColor: 'rgb(3, 14, 32)', 
      }}
    >
      {/* Hyperspeed animated background */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
        <Hyperspeed effectOptions={hyperspeedPresets.six} />
      </div>

      {/* Foreground text + button */}
      <div
        style={{
          position: 'absolute',
          zIndex: 10,
          width: '100%',
          textAlign: 'center',
          top: '30vh',
          color: 'white',
        }}
      >
        <h1 style={{
          fontSize: '6rem',      // Make this as large as you want, e.g., '5rem', '6rem'
          fontWeight: 900,
          letterSpacing: '0.03em',
          color: 'white',        // Or your preferred color
          marginBottom: '0.5em'
        }}>
          EmergenAI
        </h1>
        <h3>Automated Emergency Response Platform</h3>
        <h4>Powered by TD Synnex</h4>
        <button
          style={{
            fontSize: '2rem',
            padding: '1rem 2.5rem',
            borderRadius: 32,
            border: 'none',
            background: 'rgba(93, 113, 126, 0.57)',
            color: 'white',
            fontWeight: 700,
            cursor: 'pointer',
            boxShadow: '0 4px 24px rgba(213, 213, 213, 0.5)',
            backdropFilter: 'blur(6px)',
            marginTop: '1.5rem',
          }}
          onClick={() => navigate('/globe')}
        >
          Enter
        </button>
      </div>
    </div>
  );
}
