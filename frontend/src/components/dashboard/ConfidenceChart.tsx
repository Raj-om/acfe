import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useFusion } from '../../hooks/useFusion';

const ConfidenceChart: React.FC = () => {
  const { fusionHistory } = useFusion();
  
  // Format data for chart
  const data = fusionHistory.map((item, i) => {
    const time = new Date(item.timestamp);
    return {
      time: `${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}`,
      confidence: item.confidence * 100,
      upperBound: (item.confidence + item.uncertainty) * 100,
      lowerBound: Math.max(0, (item.confidence - item.uncertainty) * 100),
    };
  });

  if (data.length === 0) {
    return <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Waiting for data...</div>;
  }

  return (
    <div style={{ width: '100%', height: '300px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorConf" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="var(--primary-color)" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="var(--primary-color)" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorBand" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="rgba(255,255,255,0.2)" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="rgba(255,255,255,0.1)" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
          <XAxis dataKey="time" stroke="rgba(255,255,255,0.5)" fontSize={12} tickMargin={10} />
          <YAxis stroke="rgba(255,255,255,0.5)" fontSize={12} domain={[0, 100]} />
          <Tooltip 
            contentStyle={{ backgroundColor: 'var(--surface-color)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
            itemStyle={{ color: 'var(--text-primary)' }}
          />
          
          <Area 
            type="monotone" 
            dataKey="upperBound" 
            stroke="none" 
            fill="url(#colorBand)" 
            isAnimationActive={false}
          />
          <Area 
            type="monotone" 
            dataKey="lowerBound" 
            stroke="none" 
            fill="var(--surface-color)" 
            isAnimationActive={false}
          />
          <Area 
            type="monotone" 
            dataKey="confidence" 
            stroke="var(--primary-color)" 
            strokeWidth={3}
            fill="url(#colorConf)" 
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConfidenceChart;
