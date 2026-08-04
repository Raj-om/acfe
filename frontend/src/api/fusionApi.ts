import { apiClient } from './client';
import { FusionResult } from '../types/fusion';

export const triggerManualFusion = async (): Promise<FusionResult> => {
  // Simulate API call for now
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        timestamp: new Date().toISOString(),
        confidence: 0.85 + Math.random() * 0.1,
        uncertainty: 0.05,
        method: 'Dempster-Shafer',
        sourceWeights: {
          'sensor-1': 0.4,
          'sensor-2': 0.35,
          'sensor-3': 0.25
        }
      });
    }, 800);
  });
};
