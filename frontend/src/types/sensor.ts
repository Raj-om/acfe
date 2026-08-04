export interface Sensor {
  id: string;
  name: string;
  type: 'camera' | 'radar' | 'lidar' | 'ultrasonic' | 'thermal';
  status: 'online' | 'offline' | 'error' | 'calibrating';
  reliabilityScore: number;
  lastReading: number;
  history: number[];
  coordinates?: [number, number];
}

export interface Alert {
  id: string;
  timestamp: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  source: string;
  message: string;
  acknowledged: boolean;
}
