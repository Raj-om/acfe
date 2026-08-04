import React from 'react';
import { motion } from 'framer-motion';

interface FusionGaugeProps {
  confidence: number;
  uncertainty: number;
}

const FusionGauge: React.FC<FusionGaugeProps> = ({ confidence, uncertainty }) => {
  const radius = 80;
  const circumference = radius * Math.PI;
  const strokeDashoffset = circumference - (confidence * circumference);
  
  // Calculate color based on confidence
  let color = '#ef4444'; // Red
  if (confidence > 0.4) color = '#f59e0b'; // Yellow
  if (confidence > 0.75) color = '#10b981'; // Green
  
  const isHighConfidence = confidence > 0.8;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative' }}>
      <svg width="200" height="120" viewBox="0 0 200 120" style={{ filter: isHighConfidence ? `drop-shadow(0 0 10px ${color}88)` : 'none' }}>
        <defs>
          <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ef4444" />
            <stop offset="50%" stopColor="#f59e0b" />
            <stop offset="100%" stopColor="#10b981" />
          </linearGradient>
        </defs>
        
        {/* Background track */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="15"
          strokeLinecap="round"
        />
        
        {/* Fill track */}
        <motion.path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="url(#gaugeGradient)"
          strokeWidth="15"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
        
        {/* Uncertainty band */}
        {uncertainty > 0 && (
          <motion.path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="rgba(255,255,255,0.3)"
            strokeWidth="20"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ 
              strokeDashoffset: circumference - ((confidence + uncertainty) * circumference),
              strokeDasharray: `${circumference * (uncertainty * 2)} ${circumference}`
            }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            style={{ opacity: 0.5 }}
          />
        )}
      </svg>
      
      <div style={{ position: 'absolute', bottom: '10px', textAlign: 'center' }}>
        <motion.div 
          key={confidence}
          initial={{ scale: 1.2, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="text-gradient"
          style={{ fontSize: '2.5rem', fontWeight: 700, lineHeight: 1 }}
        >
          {(confidence * 100).toFixed(1)}%
        </motion.div>
        <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          ±{(uncertainty * 100).toFixed(1)}% Uncertainty
        </div>
      </div>
    </div>
  );
};

export default FusionGauge;
