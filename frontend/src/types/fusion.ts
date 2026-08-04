export interface FusionResult {
  timestamp: string;
  confidence: number;
  uncertainty: number;
  method: string;
  sourceWeights: Record<string, number>;
}

export interface ExplainerData {
  sensorId: string;
  shapValue: number;
  feature: string;
  description: string;
}

export interface SystemStatus {
  status: 'active' | 'degraded' | 'offline';
  activeSensors: number;
  totalSensors: number;
  lastFusionTime: string;
  cpuUsage: number;
  memoryUsage: number;
}
