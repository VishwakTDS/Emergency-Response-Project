import React, { useEffect, useState, useMemo, useRef } from 'react';
import Globe from 'react-globe.gl';
import * as THREE from 'three';

export default function FuturisticGlobe({ lat, lon }) {
  const globeEl = useRef();
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
  function isLatLonInUSA(lat, lon) {
    // Rough bounding box for the contiguous US
    return (
      lat >= 24.5 && lat <= 49.5 &&
      lon >= -125 && lon <= -66
    );
  }
  const showStates = lat && lon && isLatLonInUSA(parseFloat(lat), parseFloat(lon));
  const polygons = useMemo(
    () => [
      ...(countries || []),
      ...(showStates ? usStates || [] : [])
    ],
    [countries, usStates, showStates]
  );


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

  // ✨ GLOW EFFECT AROUND THE GLOBE
  useEffect(() => {
    if (!globeEl.current) return;
    const globeObj = globeEl.current;
    const scene = globeObj.scene();
    if (!scene) return;

    // Remove any existing glow
    const oldGlow = scene.getObjectByName('glow-sphere');
    if (oldGlow) scene.remove(oldGlow);

    // Shader material for glow
    const vertexShader = `
      varying vec3 vNormal;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;
    //Color for Aurora around 
    //gl_FragColor = vec4(0, 0.149, 0.329, 0.69) * intensity; //rgb(0, 56, 80) with alpha
    const fragmentShader = `
      varying vec3 vNormal;
      void main() {
        float intensity = pow(0.7 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 2.0);
        gl_FragColor = vec4(0, 0.149, 0.329, 0.69) * intensity; //rgb(0, 56, 80) with alpha
      }
    `;
    const glowMaterial = new THREE.ShaderMaterial({
      uniforms: {},
      vertexShader,
      fragmentShader,
      side: THREE.BackSide,
      blending: THREE.AdditiveBlending,
      transparent: true,
      depthWrite: false
    });

    // Get globe radius (default is 1)
    const globeRadius = globeObj.getGlobeRadius ? globeObj.getGlobeRadius() : 1;
    const glowGeometry = new THREE.SphereGeometry(globeRadius * 1.3, 75, 75);
    const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
    glowMesh.name = 'glow-sphere';
    scene.add(glowMesh);

    // Clean up on unmount
    return () => {
      if (scene.getObjectByName('glow-sphere')) {
        scene.remove(glowMesh);
      }
    };
  }, [globeEl, countries, usStates]);

  // Start spinning on mount
  useEffect(() => {
    if (globeEl.current) {
      const controls = globeEl.current.controls();
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.3;
    }
  }, []);

  // Move and stop spinning when lat/lon are set
  useEffect(() => {
    if (globeEl.current && lat && lon) {
      const controls = globeEl.current.controls();
      controls.autoRotate = false;
      globeEl.current.pointOfView(
        { lat: parseFloat(lat), lng: parseFloat(lon), altitude: 2.2 },
        1500
      );
    }
  }, [lat, lon]);

  // Reset and resume spinning when lat/lon are cleared
  useEffect(() => {
    if (globeEl.current && (!lat || !lon)) {
      // Reset globe to default view and resume spinning
      const controls = globeEl.current.controls();
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.3;
      globeEl.current.pointOfView(
        { lat: 0, lng: 0, altitude: 2.2 }, // Default view
        1500
      );
    }
  }, [lat, lon]);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'absolute', top: 0, left: 0 }}>
      <Globe
        ref={globeEl}
        width={window.innerWidth}
        height={window.innerHeight}
        backgroundColor="rgb(0,0,0,0)"
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        //globeImageUrl={null} // No earth texture
        polygonsData={polygons}
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