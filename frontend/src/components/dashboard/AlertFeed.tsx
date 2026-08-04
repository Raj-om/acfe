import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAlerts } from '../../hooks/useAlerts';
import { AlertCircle, AlertTriangle, Info, CheckCircle } from 'lucide-react';

const AlertFeed: React.FC = () => {
  const { alerts, handleAcknowledge } = useAlerts();

  const getIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <AlertCircle size={18} color="var(--danger)" />;
      case 'high': return <AlertTriangle size={18} color="var(--warning)" />;
      case 'medium': return <Info size={18} color="var(--info)" />;
      case 'low': return <CheckCircle size={18} color="var(--success)" />;
      default: return <Info size={18} />;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', height: '400px', overflowY: 'auto', paddingRight: '0.5rem' }}>
      <AnimatePresence>
        {alerts.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
            No recent alerts
          </div>
        ) : (
          alerts.map(alert => (
            <motion.div
              key={alert.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className={`alert-item ${alert.severity}`}
              onClick={() => handleAcknowledge(alert.id)}
              style={{ cursor: alert.acknowledged ? 'default' : 'pointer', opacity: alert.acknowledged ? 0.6 : 1 }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  {getIcon(alert.severity)}
                  <span style={{ fontWeight: 600, fontSize: '0.875rem' }}>{alert.source}</span>
                </div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p style={{ fontSize: '0.875rem', margin: 0, color: 'var(--text-primary)' }}>{alert.message}</p>
            </motion.div>
          ))
        )}
      </AnimatePresence>
    </div>
  );
};

export default AlertFeed;
