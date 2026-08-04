import { useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { MockWebSocket } from '../api/websocket';
import { setFusionResult, setSystemStatus } from '../store/fusionSlice';
import { addAlert } from '../store/alertSlice';

export const useWebSocket = () => {
  const dispatch = useDispatch();
  const ws = useRef<MockWebSocket | null>(null);

  useEffect(() => {
    ws.current = new MockWebSocket();
    ws.current.connect();

    ws.current.on('fusion_update', (data: any) => {
      dispatch(setFusionResult(data));
    });

    ws.current.on('alert', (data: any) => {
      dispatch(addAlert(data));
    });
    
    // Initial mock system status
    dispatch(setSystemStatus({
      status: 'active',
      activeSensors: 8,
      totalSensors: 10,
      lastFusionTime: new Date().toISOString(),
      cpuUsage: 45,
      memoryUsage: 60
    }));

    return () => {
      if (ws.current) {
        ws.current.disconnect();
      }
    };
  }, [dispatch]);
};
