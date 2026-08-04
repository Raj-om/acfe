import React from 'react';
import { NavLink } from 'react-router-dom';
import { Activity, LayoutDashboard, Radio, Bell, BarChart2, Settings, ShieldAlert } from 'lucide-react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/store';

const Sidebar = () => {
  const unreadAlerts = useSelector((state: RootState) => state.alerts.unreadCount);

  return (
    <aside className="sidebar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '3rem' }}>
        <ShieldAlert size={32} color="var(--primary-color)" />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }} className="text-gradient">ACFE</h1>
      </div>
      
      <nav style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
        <NavLink to="/dashboard" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/sensors" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <Radio size={20} />
          <span>Sensors</span>
        </NavLink>
        <NavLink to="/alerts" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <div style={{ display: 'flex', alignItems: 'center', width: '100%', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <Bell size={20} />
              <span>Alerts</span>
            </div>
            {unreadAlerts > 0 && (
              <span style={{ background: 'var(--danger)', color: 'white', padding: '2px 8px', borderRadius: '12px', fontSize: '0.75rem', fontWeight: 'bold' }}>
                {unreadAlerts}
              </span>
            )}
          </div>
        </NavLink>
        <NavLink to="/analytics" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <BarChart2 size={20} />
          <span>Analytics</span>
        </NavLink>
        
        <div style={{ marginTop: 'auto' }}>
          <NavLink to="/settings" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
            <Settings size={20} />
            <span>Settings</span>
          </NavLink>
        </div>
      </nav>
    </aside>
  );
};

export default Sidebar;
