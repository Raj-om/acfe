import React from 'react';
import GlassCard from '../components/common/GlassCard';
import FusionGauge from '../components/dashboard/FusionGauge';
import SensorGrid from '../components/dashboard/SensorGrid';
import ConfidenceChart from '../components/dashboard/ConfidenceChart';
import AlertFeed from '../components/dashboard/AlertFeed';
import RiskHeatmap from '../components/dashboard/RiskHeatmap';
import ExplainPanel from '../components/fusion/ExplainPanel';
import { useFusion } from '../hooks/useFusion';
import { Zap } from 'lucide-react';

const Dashboard: React.FC = () => {
  const { currentFusion, runFusion, isFusing } = useFusion();
  
  const confidence = currentFusion?.confidence || 0.85;
  const uncertainty = currentFusion?.uncertainty || 0.05;

  return (
    <div className="dashboard-grid">
      {/* Top Row */}
      <GlassCard className="col-span-4" delay={0.1}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Fusion Engine</h3>
          <button 
            className="btn btn-primary" 
            onClick={runFusion} 
            disabled={isFusing}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Zap size={16} />
            {isFusing ? 'Fusing...' : 'Trigger'}
          </button>
        </div>
        <FusionGauge confidence={confidence} uncertainty={uncertainty} />
        <div style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Method: <strong style={{ color: 'var(--text-primary)' }}>{currentFusion?.method || 'Dempster-Shafer'}</strong>
        </div>
      </GlassCard>

      <GlassCard className="col-span-8" title="Confidence Trend" delay={0.2}>
        <ConfidenceChart />
      </GlassCard>

      {/* Middle Row */}
      <GlassCard className="col-span-8" title="Sensor Array Status" delay={0.3}>
        <SensorGrid />
      </GlassCard>

      <GlassCard className="col-span-4" title="System Alerts" delay={0.4}>
        <AlertFeed />
      </GlassCard>
      
      {/* Bottom Row */}
      <GlassCard className="col-span-6" title="Spatial Risk Heatmap" delay={0.5}>
        <RiskHeatmap />
      </GlassCard>
      
      <GlassCard className="col-span-6" title="XAI Explanation" delay={0.6}>
        <ExplainPanel />
      </GlassCard>
    </div>
  );
};

export default Dashboard;
