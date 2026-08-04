import React from 'react';
import { useFusion } from '../../hooks/useFusion';
import { Activity, Cpu, HardDrive } from 'lucide-react';

const TopBar = () => {
  const { systemStatus } = useFusion();
  
  return (
    <header className="topbar">
      <div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Command Center</h2>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>System Overview & Status</p>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div className="indicator-pulse pulse-green" />
          <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            Sensors: <strong style={{ color: 'var(--text-primary)' }}>{systemStatus.activeSensors}/{systemStatus.totalSensors}</strong>
          </span>
        </div>
        
        <div style={{ width: '1px', height: '24px', background: 'rgba(255,255,255,0.1)' }} />
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Cpu size={16} color="var(--text-secondary)" />
          <span style={{ fontSize: '0.875rem', color: 'var(--text-primary)' }}>{systemStatus.cpuUsage}%</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <HardDrive size={16} color="var(--text-secondary)" />
          <span style={{ fontSize: '0.875rem', color: 'var(--text-primary)' }}>{systemStatus.memoryUsage}%</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: '1rem' }}>
          <img src="https://i.pravatar.cc/150?img=11" alt="User" style={{ width: '36px', height: '36px', borderRadius: '50%', border: '2px solid var(--primary-color)' }} />
          <div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600 }}>Admin User</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--success)' }}>Online</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
