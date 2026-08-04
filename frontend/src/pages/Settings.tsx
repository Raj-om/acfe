import React from 'react';
import GlassCard from '../components/common/GlassCard';

const Settings = () => {
  return (
    <div className="dashboard-grid">
      <GlassCard className="col-span-12" title="System Settings">
        <p>Fusion engine parameters and system configuration will go here.</p>
      </GlassCard>
    </div>
  );
};

export default Settings;
