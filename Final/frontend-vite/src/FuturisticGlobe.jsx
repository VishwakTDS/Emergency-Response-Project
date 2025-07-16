import React, { useEffect, useState, useMemo } from 'react';
import Globe from 'react-globe.gl';


export default function FuturisticGlobe({ lat, lon }) {
  const [countries, setCountries] = useState([]);
  const [usStates, setUsStates] = useState([]);

  // Load GeoJSON for country borders
  //US States
  useEffect(() => {
    fetch('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson')
      .then(res => res.json())
      .then(data => setCountries(data.features));
  }, []);

  // Fetch US states
  useEffect(() => {
    fetch('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
      .then(res => res.json())
      .then(data => setUsStates(data.features));
  }, []);


  // combine the polygons 
  const polygons = useMemo(() => [...(countries || []), ...(usStates || [])], [countries, usStates]);


  // Pin/ring data
  const pinData = useMemo(() => {
    if (!lat || !lon) return [];
    return [{
      lat: parseFloat(lat),
      lng: parseFloat(lon),
      color: '#00FFFF',
      altitude: 0.01 // <-- This puts the ring above the polygons
    }];
  }, [lat, lon]);

  return (
    <div style={{ width: 1000, height: 1000}}>
      <Globe
        width={1000}
        height={1000}
        backgroundColor="rgb(0,0,0,0)"
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        //globeImageUrl={null} // No earth texture
        polygonsData={[...(countries || []), ...(usStates || [])]}
        polygonCapColor={() => 'rgba(0, 0, 0, 0.28)'} // Transparent fill
        polygonSideColor={() => 'rgb(50, 206, 254)'}      // Neon cyan sides
        polygonStrokeColor={() => 'rgb(138, 231, 252)'}    // Neon cyan outline
        polygonLabel={({ properties: d }) => d.name}
        polygonAltitude={() => 0.005}
        polygonStrokeWidth={0.5}
        ringsData={pinData}
        ringColor={() => 'red'}
        ringMaxRadius={() => 4}
        ringPropagationSpeed={() => 2}
        ringRepeatPeriod={() => 1000}
        showAtmosphere={false}
        ringAltitude={d => d.altitude || 0.01} // Use the altitude from your data
      />
    </div>
  );
}