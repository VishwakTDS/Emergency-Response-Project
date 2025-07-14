import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import "leaflet/dist/leaflet.css"
import './App.css'
import { useEffect } from 'react';

// const RecenterMap = ({newlat, newlon}) => {
//     const map = useMap();

//     useEffect( () => {
//         // map.flyTo([newlat, newlon], map.getZoom());
//         map.setView([newlat, newlon], map.getZoom());
//     })
//     return null;
// }

const Map = ({lat, long}) => {
    
    // let intlat = lat ? 0 : Number(lat);
    // let intlon = long ? 0 : Number(long);
    console.log(typeof lat)
    console.log(typeof long)
    let intlat = lat ? parseFloat(lat) : 33.338;
    let intlon = long ? parseFloat(long) : -111.895;

    // let intlat = lat;
    // let intlon = long;



    console.log("Inside the map component!")
    console.log("Pringing lat and longitude:", lat, long)
    console.log("Pringing ints of lat and longitude:", intlat, intlon)
    return (
        <MapContainer center={[intlat, intlon]} zoom={13} scrollWheelZoom={true} className="mapstyle">
            <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={[intlat, intlon]}>
                <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
            </Marker>
            {/* <RecenterMap newlat={intlat} newlon={intlon} /> */}
        </MapContainer>
    )
}

export default Map;