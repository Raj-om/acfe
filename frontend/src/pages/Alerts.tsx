import React from 'react';
import GlassCard from '../components/common/GlassCard';

const Alerts = () => {
  return (
    <div className="dashboard-grid">
      <GlassCard className="col-span-12" title="Alert History">
        <p>Full alert history and rules configuration will go here.</p>
      </GlassCard>
    </div>
  );
};

export default Alerts;
