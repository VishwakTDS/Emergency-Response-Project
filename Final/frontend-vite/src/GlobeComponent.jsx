import React, { useMemo } from 'react';
import Globe from 'react-globe.gl';

export default function GlobeComponent({ lat, lon }) {
  const pinData = useMemo(() => {
    if (!lat || !lon) return [];
    return [{ lat: parseFloat(lat), lng: parseFloat(lon), color: 'red' }];
  }, [lat, lon]);

  return (
    <div style={{ width: '100%', height: '80vh', marginTop: '2rem' }}>
      <Globe
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        backgroundColor="rgba(0,0,0,0)"
        ringsData={pinData}
        ringColor={() => 'red'}
        ringMaxRadius={() => 4}
        ringPropagationSpeed={() => 2}
        ringRepeatPeriod={() => 1000}
        showAtmosphere={true}
        atmosphereColor="blue"
        atmosphereAltitude={0.2}
      />
    </div>
  );
}