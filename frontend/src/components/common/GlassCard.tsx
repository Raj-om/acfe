import React from 'react';
import { motion } from 'framer-motion';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  delay?: number;
}

const GlassCard: React.FC<GlassCardProps> = ({ children, className = '', title, delay = 0 }) => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className={`glass-panel ${className}`}
      style={{ padding: '1.5rem' }}
    >
      {title && (
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-primary)' }}>
          {title}
        </h3>
      )}
      {children}
    </motion.div>
  );
};

export default GlassCard;
