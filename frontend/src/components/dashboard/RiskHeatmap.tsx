import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for leaflet icon issue in react
import L from 'leaflet';
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const RiskHeatmap: React.FC = () => {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div style={{ height: '300px' }} />;

  const center: [number, number] = [37.7749, -122.4194]; // SF coordinates
  
  const points = [
    { pos: [37.7749, -122.4194] as [number, number], risk: 0.8, id: 1 },
    { pos: [37.7849, -122.4094] as [number, number], risk: 0.3, id: 2 },
    { pos: [37.7649, -122.4294] as [number, number], risk: 0.6, id: 3 },
    { pos: [37.7790, -122.4390] as [number, number], risk: 0.9, id: 4 },
  ];

  return (
    <div style={{ height: '300px', width: '100%', borderRadius: '12px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.1)' }}>
      <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        {points.map(pt => (
          <CircleMarker
            key={pt.id}
            center={pt.pos}
            radius={pt.risk * 20}
            pathOptions={{ 
              color: pt.risk > 0.7 ? '#ef4444' : pt.risk > 0.4 ? '#f59e0b' : '#10b981',
              fillColor: pt.risk > 0.7 ? '#ef4444' : pt.risk > 0.4 ? '#f59e0b' : '#10b981',
              fillOpacity: 0.5 
            }}
          >
            <Popup>
              <div style={{ color: '#000' }}>
                <strong>Risk Factor: {(pt.risk * 100).toFixed(0)}%</strong>
                <br/>Sector Sector-{pt.id}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
};

export default RiskHeatmap;
