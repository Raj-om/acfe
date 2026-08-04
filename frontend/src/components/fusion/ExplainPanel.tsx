import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const ExplainPanel: React.FC = () => {
  // Mock SHAP values
  const data = [
    { name: 'Front Cam', value: 0.45 },
    { name: 'Radar L', value: 0.2 },
    { name: 'Lidar', value: 0.15 },
    { name: 'Thermal', value: -0.1 },
    { name: 'Ultrasonic', value: -0.05 },
  ];

  return (
    <div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
        <strong>Explainable AI Analysis:</strong> Front camera provided the strongest positive contribution to the current confidence score, while Thermal sensors introduced minor conflicting data due to environmental noise.
      </p>
      
      <div style={{ height: '200px', width: '100%' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
            <XAxis type="number" hide />
            <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
            <Tooltip 
              cursor={{ fill: 'rgba(255,255,255,0.05)' }} 
              contentStyle={{ background: 'var(--surface-color)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.value > 0 ? 'var(--primary-color)' : 'var(--danger)'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ExplainPanel;
