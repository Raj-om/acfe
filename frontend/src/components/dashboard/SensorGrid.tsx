import React from 'react';
import { motion } from 'framer-motion';

const MOCK_SENSORS = [
  { id: 'cam-1', name: 'Front Camera', type: 'Camera', status: 'online', conf: 0.92, rel: 0.95 },
  { id: 'rad-1', name: 'Long Range Radar', type: 'Radar', status: 'online', conf: 0.88, rel: 0.90 },
  { id: 'lid-1', name: '360 Lidar', type: 'Lidar', status: 'online', conf: 0.95, rel: 0.98 },
  { id: 'th-1', name: 'Thermal Sensor', type: 'Thermal', status: 'degraded', conf: 0.45, rel: 0.60 },
];

const SensorGrid: React.FC = () => {
  return (
    <div className="sensor-grid">
      {MOCK_SENSORS.map((sensor, i) => (
        <motion.div
          key={sensor.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          style={{
            background: 'rgba(255,255,255,0.03)',
            border: '1px solid rgba(255,255,255,0.05)',
            borderRadius: '12px',
            padding: '1rem',
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <h4 style={{ fontWeight: 600 }}>{sensor.name}</h4>
            <div className={`indicator-pulse ${sensor.status === 'online' ? 'pulse-green' : 'pulse-yellow'}`} />
          </div>
          
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            {sensor.type} | ID: {sensor.id}
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.25rem' }}>
                <span>Confidence</span>
                <span>{(sensor.conf * 100).toFixed(0)}%</span>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px' }}>
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${sensor.conf * 100}%` }}
                  style={{ height: '100%', background: 'var(--secondary-color)', borderRadius: '2px' }}
                />
              </div>
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.25rem' }}>
                <span>Reliability</span>
                <span>{(sensor.rel * 100).toFixed(0)}%</span>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px' }}>
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${sensor.rel * 100}%` }}
                  style={{ height: '100%', background: sensor.rel > 0.8 ? 'var(--success)' : 'var(--warning)', borderRadius: '2px' }}
                />
              </div>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default SensorGrid;
