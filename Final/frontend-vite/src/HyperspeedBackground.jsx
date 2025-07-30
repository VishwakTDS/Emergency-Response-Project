import React from 'react';

const HyperspeedBackground = () => (
  <div style={{
    position: 'fixed',
    inset: 0,
    width: '100vw',
    height: '100vh',
    zIndex: 0,
    pointerEvents: 'none',
    overflow: 'hidden',
    background: 'radial-gradient(ellipse at center, #1e293b 0%, #020617 100%)'
  }}>
    <svg
      style={{
        position: 'absolute',
        width: '100vw',
        height: '100vh',
        left: 0,
        top: 0,
        zIndex: 0,
        pointerEvents: 'none'
      }}
      viewBox="0 0 1920 1080"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g>
        {[...Array(60)].map((_, i) => (
          <rect
            key={i}
            x={960}
            y={540}
            width={2}
            height={Math.random() * 800 + 200}
            fill="#38bdf8"
            opacity={0.15 + Math.random() * 0.25}
            rx={1}
            transform={`rotate(${(i * 360) / 60} 960 540)`}
          >
            <animate
              attributeName="y"
              values="540;0"
              dur={`${1 + Math.random() * 1.5}s`}
              repeatCount="indefinite"
            />
            <animate
              attributeName="height"
              values="200;1000;200"
              dur={`${1 + Math.random() * 1.5}s`}
              repeatCount="indefinite"
            />
          </rect>
        ))}
      </g>
    </svg>
  </div>
);

export default HyperspeedBackground;

