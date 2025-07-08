import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import "leaflet/dist/leaflet.css";
import React, { useEffect } from 'react';

const RecenterMap = ({ newlat, newlon }) => {
  const map = useMap();
  useEffect(() => {
    map.flyTo([newlat, newlon], map.getZoom());
  }, [newlat, newlon, map]);
  return null;
};

const MapView = ({ lat = '0', long = '0' }) => {
  let intlat = lat ? parseFloat(lat) : 33.338;
  let intlon = long ? parseFloat(long) : -111.895;

  return (
    <div className="flex justify-center mt-8">
      <MapContainer
        center={[intlat, intlon]}
        zoom={13}
        scrollWheelZoom={true}
        className="rounded-lg shadow-lg w-[600px] h-[400px]"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[intlat, intlon]}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
        <RecenterMap newlat={intlat} newlon={intlon} />
      </MapContainer>
    </div>
  );
};

export default MapView; 